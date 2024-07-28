import unittest
import pandas as pd
import numpy as np
from songs_dataset import SongsDataset
from recommender import CosineSimilarityRecommender
import tempfile

class TestCosineSimilarityRecommender(unittest.TestCase):
    def setUp(self):
        dataframe =  pd.DataFrame([{
                    "id": "a123",
                    "name": "First",
                    "artists": ["Second"],
                    "artist_ids": [],
                    "danceability": 0.3,
                    "energy": 0.1,
                    "loudness": 0,
                    "acousticness": 0,
                    "speechiness": 0,
                    "valence": 0
                },
                {
                    "id": "b234",
                    "name": "Third",
                    "artists": ["Fourth", "Second"],
                    "artist_ids": [],
                    "danceability": 0.2,
                    "energy": 0.3,
                    "loudness": 0,
                    "acousticness": 0,
                    "speechiness": 0,
                    "valence": 0
                },
                {
                    "id": "b235",
                    "name": "Third",
                    "artists": ["Fourth", "Second"],
                    "artist_ids": [],
                    "danceability": 0.2,
                    "energy": 0.3,
                    "loudness": 0,
                    "acousticness": 0,
                    "speechiness": 0,
                    "valence": 0
                }
            ])
        with tempfile.NamedTemporaryFile() as fp:
            dataframe.to_csv(fp.name)
            self.dataset = SongsDataset(fp.name)


    def test_recommend(self):
        recommender = CosineSimilarityRecommender(self.dataset)
        self.assertEqual(recommender.recommend(["b234"], 1).index.size, 1)
        self.assertEqual(recommender.recommend(["b234"], 1)["id"].iloc[0], "b235")
        self.assertEqual(recommender.recommend(["b234"], 2)["id"].iloc[0], "b235")
        self.assertEqual(recommender.recommend(["b234"], 2)["id"].iloc[1], "a123")


if __name__ == '__main__':
    unittest.main()