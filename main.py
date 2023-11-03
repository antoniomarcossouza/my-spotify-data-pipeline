"""Lambda function to get recently played songs from Spotify API."""
import pandas as pd
from sqlalchemy import create_engine

from exceptions import (
    EmptyDataFrameException,
    NonUniquePrimaryKeyException,
    NullValuesFoundException,
)
from spotify_etl import get_token, get_recently_played, get_artists_genres

TOKEN = get_token()


def extract() -> pd.core.frame.DataFrame:
    """Extract recently played songs from Spotify API"""

    songs = []
    albums = []
    artists = []
    artists_ids = []
    date = []
    played_at = []

    for song in get_recently_played(token=TOKEN)["items"]:
        songs.append(song["track"]["name"])
        albums.append(song["track"]["album"]["name"])
        artists.append(song["track"]["album"]["artists"][0]["name"])
        artists_ids.append(song["track"]["album"]["artists"][0]["id"])
        date.append(song["played_at"][0:10])
        played_at.append(song["played_at"])

    return pd.DataFrame(
        {
            "song_name": songs,
            "album_name": albums,
            "artist_name": artists,
            "artist_id": artists_ids,
            "played_at": played_at,
            "date": date,
        }
    )


def check_data_integrity(df: pd.core.frame.DataFrame):
    """Check if dataframe is empty, if primary key is unique and if there are null values."""

    if df.empty:
        raise EmptyDataFrameException()

    if not pd.Series(df["played_at"]).is_unique:
        raise NonUniquePrimaryKeyException(column_name="played_at")

    if df.isnull().values.any():
        raise NullValuesFoundException()


def transform(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Transform recently played songs from Spotify API

    - Add artist genres column to the DataFrame
    """

    check_data_integrity(df=df)

    df["genres"] = df["artist_id"].apply(
        lambda artist_id: get_artists_genres(artist_id, TOKEN)
    )
    df["genres"] = [", ".join(genre) for genre in df["genres"]]

    df["genres"] = df["genres"].replace("", None)
    df = df.dropna(subset=["genres"])

    return df


if __name__ == "__main__":
    recently_played = extract()

    transformed_data = transform(df=recently_played)
