from pydantic import BaseModel
from .song import Song


class SongList(BaseModel):
    songs: list[Song]
