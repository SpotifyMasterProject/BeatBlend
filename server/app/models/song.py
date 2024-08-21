from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Song(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    artists: List[str] = []
    album: Optional[str] = None
    release_date: Optional[datetime] = None
    popularity: Optional[float] = None
    danceability: Optional[float] = None
    energy: Optional[float] = None
    speechiness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None