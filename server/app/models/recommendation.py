from pydantic import BaseModel

from .song import Song


class Recommendation(Song):
    votes: list[str]


class RecommendationList(BaseModel):
    recommendations: list[Recommendation]
