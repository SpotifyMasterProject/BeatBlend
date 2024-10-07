from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from .song import Playlist
from .recommendation import Recommendation


class SessionOut(BaseModel):
    id: Optional[str] = None
    name: str
    host_id: Optional[str] = None
    host_name: Optional[str] = None
    guests: list[str] = []
    invite_link: Optional[str] = None
    creation_date: Optional[datetime] = None
    # is_running: bool = False


class Session(SessionOut):
    playlist: Optional[Playlist] = None
    recommendations: list[Recommendation] = []