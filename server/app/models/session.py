from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from .recommendation import Recommendation
from .song import Playlist


class SessionCore(BaseModel):
    id: Optional[str] = None
    name: str
    host_id: Optional[str] = None
    host_name: Optional[str] = None
    guests: list[str] = []
    invite_link: Optional[str] = None
    creation_date: Optional[datetime] = None
    # is_running: bool = False


class Session(SessionCore):
    playlist: Playlist
    recommendations: list[Recommendation] = []