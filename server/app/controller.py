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
    # asyncio.create_task(test_websocket())
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


async def validate_user_id(user_id):
    if await redis.exists(get_user_key(user_id)) == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized! Invalid user ID.")


def get_user_key(user_id) -> str:
    return f'user:{user_id}'


def get_session_key(session_id) -> str:
    return f'session:{session_id}'


def get_invite_key(invite_token) -> str:
    return f'invite:{invite_token}'


async def remove_guest(session: Session, guest_id: str) -> None:
    if guest_id in session.guests:
        session.guests.remove(guest_id)
        await redis.set(get_session_key(session.id), session.model_dump_json())
        await manager.publish(channel=get_session_key(session.id), message=f"Guest {guest_id} was removed from session")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not part of session.")

@app.get("/", status_code=status.HTTP_200_OK)
async def read_root(user_id: Annotated[str, Depends(verify_token)]) -> dict:
    await validate_user_id(user_id)
    # Add check if userid matches username?
    result = await redis.get(get_user_key(user_id))
    user = User.model_validate_json(result)
    return {"Hello World": "User. Your details are:", "user_id": user.id, "username": user.username}


@app.post("/auth-codes", status_code=status.HTTP_201_CREATED)
async def authorize_spotify(user: SpotifyUser) -> Token:
    # TODO: replace the spotify token getting with spotipy
    # global spotify_token
    # spotify_token = exchange_code_for_token(user.auth_code)

    user.id = str(uuid.uuid4())
    await redis.set(get_user_key(user.id), user.model_dump_json())
    return generate_token(user)


@app.post("/token", status_code=status.HTTP_201_CREATED)
async def authorize(user: User) -> Token:
    user.id = str(uuid.uuid4())
    await redis.set(get_user_key(user.id), user.model_dump_json())
    return generate_token(user)


@app.post("/sessions", status_code=status.HTTP_201_CREATED, response_model=Session)
async def create_new_session(user_id: Annotated[str, Depends(verify_token)], session: Session) -> Session:
    await validate_user_id(user_id)
    session.id = str(uuid.uuid4())
    session.host = str(user_id)

    session.invite_token = str(uuid.uuid4())
    # TODO: adjust URL
    session.invite_link = f'http://localhost:5173/sessions/join/{session.invite_token}'

    await redis.set(get_session_key(session.id), session.model_dump_json())
    await redis.set(get_invite_key(session.invite_token), session.id)

    await manager.publish(channel=get_session_key(session.id), message="New session created")
    return session


@app.get("/sessions", status_code=status.HTTP_200_OK, response_model=list[Session])
async def get_session() -> list[Session]:
    session_keys = [session_id async for session_id in redis.scan_iter(match='session:*')]

    sessions = []
    for session_key in session_keys:
        result = await redis.get(session_key)
        sessions.append(Session.model_validate_json(result))

    return sessions


# TODO: delete if onboarding using session_ids is not required
# @app.post("/sessions/{session_id}/guests")
# async def add_guest(guest_id: Annotated[str, Depends(verify_token)], session_id: str):
#     if await redis.exists(f'session:{session_id}') == 0:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session ID.")
#     result = await redis.get(f'session:{session_id}')
#     session = Session.model_validate_json(result)
#     session.guests.append(str(guest_id))
#     await redis.set(f'session:{session_id}', session.model_dump_json())


@app.post("/sessions/join/{invite_token}", status_code=status.HTTP_200_OK, response_model=Session)
async def join_session(guest_id: Annotated[str, Depends(verify_token)], invite_token: str) -> Session:
    await validate_user_id(guest_id)
    if await redis.exists(get_invite_key(invite_token)) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invite link.")

    session_id = await redis.get(get_invite_key(invite_token))
    result = await redis.get(get_session_key(session_id))
    session = Session.model_validate_json(result)

    if guest_id not in session.guests:
        session.guests.append(guest_id)
        await redis.set(get_session_key(session.id), session.model_dump_json())
        await manager.publish(channel=get_session_key(session.id), message=f"Guest {guest_id} has joined the session")

    return session


@app.delete("/sessions/{session_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_session(guest_id: Annotated[str, Depends(verify_token)], session_id: str) -> None:
    await validate_user_id(guest_id)
    if await redis.exists(get_session_key(session_id)) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid session ID.")
    result = await redis.get(get_session_key(session_id))
    session = Session.model_validate_json(result)
    await remove_guest(session, guest_id)


@app.delete("/sessions/{session_id}/guests/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_guest(user_id: Annotated[str, Depends(verify_token)], session_id: str, guest_id: str) -> None:
    await validate_user_id(user_id)
    if await redis.exists(get_session_key(session_id)) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid session ID.")
    result = await redis.get(get_session_key(session_id))
    session = Session.model_validate_json(result)
    if session.host != str(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not host of session.")
    await remove_guest(session, guest_id)


@app.websocket("/ws/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    await websocket.accept()
    channel = get_session_key(session_id)

    async with manager.subscribe(channel=channel) as subscriber:
        try:
            async for event in subscriber:
                await websocket.send_text(event.message)
        except WebSocketDisconnect:
            pass


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
