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


class GuestSession(BaseModel):
    """
        Subset of session available for guest users.
    """
    id: Optional[str] = None
    name: str
    playlist: List[Song] = []
    is_running: bool

class AnonymousSession(BaseModel):
    """
        Subset of session available for anonymous users.
        Useful for obtaining metadata about the session,
        prior to joining. This should contain publicly
        available information.
    """
    name: str
    host_username: Optional[str] = None

def anonymizeSession(session: Session, host: User):
    return AnonymousSession(
        name = session.name,
        host_username = host.username,
    )

def guestSession(session: Session):
    return GuestSession(
        id=session.id,
        name=session.name,
        playlist=session.playlist,
        is_running=session.is_running,
    )