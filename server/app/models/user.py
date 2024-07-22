from pydantic import BaseModel


class User(BaseModel):
    auth_code: str
    username: str
