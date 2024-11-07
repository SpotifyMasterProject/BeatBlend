from datetime import datetime
from typing import Optional

from .camel_model import CamelModel
from .user import User
from .recommendation import Recommendation
from .song import Playlist


class SessionCore(CamelModel):
    id: Optional[str] = None
    name: str
    host_id: Optional[str] = None
    host_name: Optional[str] = None
    guests: dict[str, User] = {}
    invite_link: Optional[str] = None
    creation_date: Optional[datetime] = None
    voting_start_date: Optional[datetime] = None
    voting_end_date: Optional[datetime] = None


class Session(SessionCore):
    playlist: Playlist
    recommendations: list[Recommendation] = []
    is_running: bool = True
