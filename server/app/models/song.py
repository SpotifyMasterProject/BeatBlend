from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

# Approximate values for maximum and minimum values of tempo.
MAX_TEMPO = 200
MIN_TEMPO = 60

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
    # Scaled tempo between [0, 1].
    scaled_tempo: Optional[float] = None
    duration_ms: Optional[int] = None
    release_date: Optional[datetime] = None
    popularity: Optional[float] = None

    @model_validator(mode='after')
    def set_scaled_tempo(self) -> 'Song':
        scaled_tempo = (self.tempo - MIN_TEMPO) * 2 / (MAX_TEMPO - MIN_TEMPO) - 1
        # Clamp between -1 and 1
        self.scaled_tempo = max(-1, min(scaled_tempo, 1))

        return self