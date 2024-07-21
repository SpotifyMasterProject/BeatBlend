from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from models.authCode import AuthCode

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.post("/auth-codes")
def store_auth_code(auth_code: AuthCode):
    return {"Test successful": "{}".format(auth_code)}
