from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    username: str


class SpotifyUser(User):
    auth_code: str
