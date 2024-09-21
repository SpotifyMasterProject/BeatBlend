from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Song(BaseModel):
    id: Optional[str] = None
    track_name: Optional[str] = None
    album: Optional[str] = None
    album_id: Optional[str] = None
    artists: list[str] = []
    artist_ids: list[str] = []
    danceability: Optional[float] = None
    energy: Optional[float] = None
    speechiness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None
    duration_ms: Optional[int] = None
    release_date: Optional[datetime] = None
    popularity: Optional[float] = None
