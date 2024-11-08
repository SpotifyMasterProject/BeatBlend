from datetime import datetime
from typing import Optional

from .camel_model import CamelModel
from .song import Song


class Recommendation(Song):
    votes: list[str] = []


class RecommendationList(CamelModel):
    recommendations: list[Recommendation] = []
    voting_start_time: Optional[datetime] = None
