from pydantic import BaseModel
from typing import Optional, List

class Song(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    artists: List[str] = []
    album: Optional[str] = None
    danceability: Optional[float] = None
    energy: Optional[float] = None
    speechiness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None
    release_date: Optional[str] = None
    popularity: Optional[float] = None

