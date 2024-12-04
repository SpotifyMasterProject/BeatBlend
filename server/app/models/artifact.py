from typing import Optional

from .camel_model import CamelModel


class AverageFeatures(CamelModel):
    danceability: float
    energy: float
    speechiness: float
    valence: float
    scaled_tempo: float


class Artifact(CamelModel):
    songs_played: int
    songs_added_manually: int
    most_songs_added_by: Optional[list[str]]
    most_votes_by: Optional[list[str]]
    most_significant_feature_overall: Optional[str]
    first_recommendation_vote_percentage: float
    average_features: AverageFeatures
    genre_start: Optional[list[str]]
    genre_end: Optional[list[str]]
