from typing import Optional, List
from pydantic import BaseModel


class Session(BaseModel):
    id: Optional[str] = None
    name: str
    host: Optional[str] = None
    guests: Optional[List[str]] = []
    invite_link: Optional[str] = None
    playlist: Optional[List[str]] = []
