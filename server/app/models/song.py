from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Song(BaseModel):
    id: str
    name: Optional[str] = None
    artists: Optional[List[str]] = []
    album: Optional[str] = None
    release_date: Optional[datetime] = None
    popularity: Optional[float] = None
    danceability: Optional[float] = None
    energy: Optional[float] = None
    speechiness: Optional[float] = None
    tempo: Optional[float] = None
    valence: Optional[float] = None
