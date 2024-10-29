from datetime import datetime
from .camel_model import CamelModel
from .song import Song


class Recommendation(Song):
    votes: list[str] = []


class RecommendationList(CamelModel):
    recommendations: list[Recommendation] = []
    creation_date: datetime
