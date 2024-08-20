from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    username: str = ''
    # List of sessions this user hosted
    sessions: List[str] = []


class SpotifyUser(User):
    auth_code: str