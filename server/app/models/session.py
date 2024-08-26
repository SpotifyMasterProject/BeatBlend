from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from song import Song


class Session(BaseModel):
    id: Optional[str] = None
    name: str
    host: Optional[str] = None
    host_name: Optional[str] = None
    guests: List[str] = []
    invite_link: Optional[str] = None
    playlist: List[Song] = []
    creation_date: Optional[datetime] = None
    # is_running: bool = False
