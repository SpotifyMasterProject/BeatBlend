import unittest
import pandas as pd
from songs_dataset import SongsDataset
import tempfile

class TestSongsDataset(unittest.TestCase):
    def setUp(self):
        self.dataframe =  pd.DataFrame([{
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
                    "artists": ["Fourth"],
                    "artist_ids": [],
                    "danceability": 0.2,
                    "energy": 0.3,
                    "loudness": 0,
                    "acousticness": 0,
                    "speechiness": 0,
                    "valence": 0
                }
            ])
        self.fp = tempfile.NamedTemporaryFile()
        self.dataframe.to_csv(self.fp.name)


    def test_matching_songs(self):
        dataset = SongsDataset(self.fp.name)
        self.assertEqual(dataset.get_matching_songs("First").index.size, 1)
        self.assertEqual(dataset.get_matching_songs("First")["id"].iloc[0], "a123")

        self.assertEqual(dataset.get_matching_songs("Second").index.size, 2)
        self.assertEqual(dataset.get_matching_songs("Second")["id"].iloc[0], "a123")
        self.assertEqual(dataset.get_matching_songs("Second")["id"].iloc[1], "b234")

    def test_matching_songs_with_limit(self):
        dataset = SongsDataset(self.fp.name)
        self.assertEqual(dataset.get_matching_songs("Second", num_songs=1).index.size, 1)

    def test_get_songs(self):
        dataset = SongsDataset(self.fp.name)
        self.assertEqual(dataset.get_songs(including=["a123"]).index.size, 1)
        self.assertEqual(dataset.get_songs(including=["a123"])["id"].iloc[0], "a123")
        
        self.assertEqual(dataset.get_songs(excluding=["b234"]).index.size, 2)
        self.assertEqual(dataset.get_songs(excluding=["b234"])["id"].iloc[0], "a123")
        self.assertEqual(dataset.get_songs(excluding=["b234"])["id"].iloc[1], "b235")




if __name__ == '__main__':
    unittest.main()