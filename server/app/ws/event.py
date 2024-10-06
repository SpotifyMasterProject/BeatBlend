from pydantic import BaseModel

from models.recommendation import RecommendationList
from models.session import Session
from models.song import Song

#TODO: adjust types
MODEL_MAPPING = {
    "session": Session,
    "songs": Song,
    "recommendations": RecommendationList
}


class Event:
    def __init__(self, channel: str, message: BaseModel) -> None:
        self.channel = channel
        for prefix, model in MODEL_MAPPING.items():
            if channel.startswith(prefix):
                self.message = model(**message.model_dump())
                break
        else:
            self.message = message

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Event) and self.channel == other.channel and self.message == other.message

    def __repr__(self) -> str:
        return f"Event(channel={self.channel!r}, message={self.message!r})"
