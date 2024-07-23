from typing import Optional
from pydantic import BaseModel


class SpotifyUser(BaseModel):
    id: Optional[str] = None
    username: str
    auth_code: str
