from typing import Optional

from .camel_model import CamelModel


class AverageFeatures(CamelModel):
    danceability: float = 0.0
    energy: float = 0.0
    speechiness: float = 0.0
    valence: float = 0.0
    scaled_tempo: float = 0.0


class Artifact(CamelModel):
    songs_played: int = 0
    songs_added_manually: int = 0
    most_songs_added_by: list[str] = []
    most_votes_by: list[str] = []
    most_significant_feature_overall: Optional[str] = None
    first_recommendation_vote_percentage: float = 0.0
    average_features: AverageFeatures
    genre_start: list[str] = []
    genre_end: list[str] = []
