from pydantic import BaseModel

from .song import Song


class Recommendation(Song):
    votes: int

class RecommendationList(BaseModel):
    recommendations: list[Recommendation]