from pydantic import BaseModel
from typing import List
from song import Song


class SongList(BaseModel):
    songs: List[Song]
