from typing import Optional, List
from pydantic import BaseModel
from .user import User
from .song import Song
from datetime import datetime


class Session(BaseModel):
    id: Optional[str] = None
    name: str
    host: Optional[str] = None
    guests: List[str] = []
    invite_token: Optional[str] = None
    invite_link: Optional[str] = None
    creation_date: Optional[datetime] = None
    playlist: List[Song] = []
    is_running: bool = False
