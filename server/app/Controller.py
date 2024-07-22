import base64
import os
import requests

from fastapi import FastAPI
from models.authCode import AuthCode
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
def store_auth_code(code: AuthCode):
    global spotify_token
    spotify_token = exchange_code_for_token(code.auth_code)
    return {"Test successful": "Token received."}


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