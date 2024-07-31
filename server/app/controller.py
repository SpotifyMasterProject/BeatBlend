import asyncio
import base64
import jwt
import os
import requests
import uuid

from contextlib import asynccontextmanager
from datetime import timedelta, datetime, timezone
from fastapi import FastAPI, HTTPException, status, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from models.token import Token
from models.user import User, SpotifyUser
from models.session import Session
from redis.asyncio import Redis
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from websocket_manager import WebsocketManager

manager = WebsocketManager()


@asynccontextmanager
async def lifespan(_: FastAPI):  # idk might need to rename parameter
    asyncio.create_task(test_websocket())
    await manager.connect()
    yield
    await manager.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
redis = Redis(host="redis", port=6379, decode_responses=True)
spotify_token = ""


def generate_token(user: User) -> Token:
    jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", 60))
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")

    to_encode = {"sub": user.id, "username": user.username}
    access_token_expires = timedelta(minutes=jwt_expire_minutes)
    expire = datetime.now(timezone.utc) + (access_token_expires or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm
    )
    return Token(access_token=encoded_jwt, token_type="bearer")


def verify_token(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized!")

    try:
        payload = jwt.decode(token, key=secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise auth_exception
    except InvalidTokenError:
        raise auth_exception
    return user_id


def exchange_code_for_token(auth_code: str) -> str:
    id_secret = f'{os.getenv("SPOTIFY_CLIENT_ID")}:{os.getenv("SPOTIFY_CLIENT_SECRET")}'
    base64_encoded = base64.b64encode(id_secret.encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + base64_encoded,
        },
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        }
    )
    return response.json()["access_token"]


def extract_user_id_from_token(request: Request) -> str:
    """
    Extracts the user ID from the authorization token provided in the request headers.

    :param request: The request object that includes the Authorization header (provided by FastAPI).
    :return: The user ID from the decoded JWT token.
    """
    bearer = request.headers.get("Authorization")
    token = bearer.split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload["sub"]
    return user_id


@app.get("/")
async def read_root(user_id: Annotated[str, Depends(verify_token)]):
    if await redis.exists(user_id) == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized! Invalid user ID.")
    # Add check if userid matches username?
    result = await redis.get(str(user_id))
    user = User.model_validate_json(result)
    return {"Hello World": "User. Your details are:", "user_id": user.id, "username": user.username}


@app.post("/auth-codes")
async def authorize_spotify(user: SpotifyUser) -> Token:
    # TODO: replace the spotify token getting with spotipy
    # global spotify_token
    # spotify_token = exchange_code_for_token(user.auth_code)

    user.id = str(uuid.uuid4())
    await redis.set(user.id, user.model_dump_json())
    return generate_token(user)


@app.post("/token")
async def authorize(user: User) -> Token:
    user.id = str(uuid.uuid4())
    await redis.set(user.id, user.model_dump_json())
    return generate_token(user)


@app.post("/sessions")
async def create_new_session(request: Request, session: Session) -> Session:
    session.id = str(uuid.uuid4())
    session.host = extract_user_id_from_token(request)
    await redis.set(session.id, session.model_dump_json())
    return session



# This WS code is inspired by the encode/broadcaster package.
# If something needs to be fixed or changed, look at their GitHub repo.
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # This endpoint only serves a simplex operation.
    # If the future desires duplex operations, look at the encode/broadcaster example.
    await websocket.accept()

    async with manager.subscribe(channel="test") as subscriber:
        try:
            async for event in subscriber:
                await websocket.send_text(event.message)
        except WebSocketDisconnect:
            pass


async def test_websocket():
    event = asyncio.Event()
    asyncio.create_task(set_websocket_test_task(event))
    await handle_test_event(event)


async def set_websocket_test_task(event):
    while True:
        await asyncio.sleep(2)
        event.set()
        event.clear()


async def handle_test_event(event):
    while True:
        await event.wait()
        await manager.publish(channel="test", message="WEBSOCKET TEST MESSAGE")
