from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    username: str
    joined_sessions: list[str] = []


class SpotifyUser(User):
    username: Optional[str] = None
    auth_code: str
