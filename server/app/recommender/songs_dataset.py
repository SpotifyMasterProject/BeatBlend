import pandas as pd
import numpy as np
import functools
from ast import literal_eval

class SongsDataset:
    """Dataset of songs.
    
    The dataset is expected to have the following columns:

    id: str - Unique id identifying the song
    name: str - Name of the song
    album: str - Name of the album the song is a part of
    album_id: str - Id of the album the song is a part of
    artists: str[] - Name of the artists for the song
    artist_id: str[] - Ids of the artists
    track_number: int - Number of the track inside the album
    disc_number: int - Disc number of the album
    explicit: bool - Whether the song is explicit or not
    danceability: float - How suitable a track is for dancing. Value in [0, 1].
    energy: float - How intense and active a track is. Value in [0, 1]
    key: integer - The key the track is in. Integers map to pitches using
                   standard Pitch Class notation.
                   E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
                   If no key was detected, the value is -1.
    loudness: float - The overall loudness of a track in decibels (dB).
                      Values usually range in [-60, 0].
    mode: integer - Mode indicates the modality (major or minor) of a track.
                    Major is represented by 1 and minor is 0.
    speechiness: float - Speechiness detects the presence of spoken words
                         in a track. Value in [0, 1].
    acousticness: float - A confidence measure from 0.0 to 1.0 of whether the
                          track is acoustic.
    instrumentalness: float - Predicts whether a track contains no vocals.
                              "Ooh" and "aah" sounds are treated as
                              instrumental in this context. Value in [0, 1].
    liveness: float - Detects the presence of an audience in the recording.
                      Value in [0, 1].
    valence: float - A measure from 0.0 to 1.0 describing the musical
                     positiveness conveyed by a track.
    tempo: float - The overall estimated tempo of a track in beats per minute
                   (BPM)
    duration_ms: int - Duration of sound in ms
    time_signature: int - The time signature ranges from 3 to 7 indicating time
                          signatures of "3/4", to "7/4".
    year: int - Year the song was released in.
    release_date: str - Full release date of the track in YYYY-MM-DD format.
    
    tempo,duration_ms,time_signature,year,release_date
    """

    # Columns to be used for matching.
    ACOUSTIC_FEATURES = ["danceability", "energy", "loudness", "acousticness", "speechiness", "valence"]

    def __init__(self, dataset_path: str):
        self.df = pd.read_csv(dataset_path)
        
        for column in ["artists", "artist_ids"]:
            self.df[column] = self.df[column].apply(literal_eval)

    def get_matching_songs(self, pattern: str, num_songs=10) -> pd.DataFrame:
        """Returns a DataFrame containing just the songs which match the pattern.
        
        The pattern match either the name of the song or the name of one of the
        artists.
        """
        return self.df[self.df["name"].str.contains(pattern) |
                       self.df["artists"].str.join(',').str.contains(pattern)][:num_songs]
    
    def get_songs(self, including: list[str] = None, excluding: list[str] = []) -> pd.DataFrame:
        """Returns a DataFrame containing the included songs and not containing
        the excluding songs.
        
        including - list of ids to include
        excluding - list of ids to exclude
        """
        return self.df[self.df["id"].apply(lambda id: (including is None or id in including) and id not in excluding)]
    