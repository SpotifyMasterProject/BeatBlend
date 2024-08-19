from typing import Optional, List
from pydantic import BaseModel
from song import Song


class Session(BaseModel):
    id: Optional[str] = None
    name: str
    host: Optional[str] = None
    guests: Optional[List[str]] = []
    invite_token: Optional[str] = None
    invite_link: Optional[str] = None
    playlist: Optional[List[Song]] = []
