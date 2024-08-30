import pandas as pd
import numpy as np
from enum import Enum
from songs_dataset import SongsDataset


class Recommender:
    def __init__(self, dataset: SongsDataset):
        self.dataset = dataset


    def recommend(self, seed_song_ids: list[str], num_songs=3):
        """Template method for recommending songs."""
        raise NotImplementedError("Unimplemented")

    def _construct_features(self, songs: pd.DataFrame = None):
        """Constructs an acoustic feature matrix based on the songs dataframe.
        
        We assume that songs is a subset of a SongsDataset.
        """
        if songs is None:
            songs = self.df
        return songs[self.dataset.ACOUSTIC_FEATURES].to_numpy()

class CosineSimilarityRecommender(Recommender):
    def recommend(self, songs: list[str], num_songs=3):
        # Shape: (N_songs, Features)
        current_songs_features = self._construct_features(self.dataset.get_songs(including=songs))
        all_songs = self.dataset.get_songs(excluding=songs)

        # Shape: (M_songs, Features)
        all_songs_features = self._construct_features(all_songs)
        
        # Shape (M_songs, N_Songs)
        similarity = np.dot(all_songs_features, current_songs_features.T)

        descending_indices = similarity.mean(axis=1).argsort()[::-1][:num_songs]
        return all_songs.iloc[descending_indices]

