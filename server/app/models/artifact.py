from .camel_model import CamelModel


class AverageFeatures(CamelModel):
    danceability: float
    energy: float
    speechiness: float
    valence: float
    tempo: float


class Artifact(CamelModel):
    songs_played: int
    songs_added_manually: int
    most_songs_added_by: int
    most_votes_by: str
    most_significant_feature_overall: str
    first_recommendation_vote_percentage: float
    average_features: AverageFeatures
    genre_start: list[str]
    genre_end: list[str]
