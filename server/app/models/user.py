from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    username: str
    sessions: list[str] = []
    last_voted_on: Optional[str] = None


class SpotifyUser(User):
    username: Optional[str] = None
    auth_code: str
