import base64
import jwt
import os
import requests

from datetime import timedelta, datetime, timezone
from fastapi import FastAPI
from models.guest import Guest
from models.token import Token
from models.user import User
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

spotify_token = ""


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.post("/auth-codes")
def spotify_login(user: User) -> Token:
    global spotify_token
    spotify_token = exchange_code_for_token(user.auth_code)
    return generate_token(user.username)


@app.post("/token")
def guest_access(guest: Guest) -> Token:
    return generate_token(guest.username)


def generate_token(username: str) -> Token:
    jwt_expire_minutes = os.getenv("JWT_EXPIRE_MINUTES", 30)
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