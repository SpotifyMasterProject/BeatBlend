import base64
import jwt
import os
import requests

from datetime import timedelta, datetime, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from models.spotifyUser import SpotifyUser
from models.token import Token
from models.user import User
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

spotify_token = ""


def generate_token(username: str) -> Token:
    jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", 60))
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")

    to_encode = {"sub": username}
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
        username = payload.get("sub")
        if username is None:
            raise auth_exception
    except InvalidTokenError:
        raise auth_exception
    return username


def exchange_code_for_token(auth_code: str) -> str:
    id_secret = f"{os.getenv("SPOTIFY_CLIENT_ID")}:{os.getenv("SPOTIFY_CLIENT_SECRET")}"
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


#TODO: also include id
@app.get("/")
def read_root(username: Annotated[str, Depends(verify_token)]):
    return {"Hello": "World!", "username": username}


@app.post("/auth-codes")
def authorize_spotify(user: SpotifyUser) -> Token:
    global spotify_token
    spotify_token = exchange_code_for_token(user.auth_code)
    return generate_token(user.username)


@app.post("/token")
def authorize(user: User) -> Token:
    return generate_token(user.username)
