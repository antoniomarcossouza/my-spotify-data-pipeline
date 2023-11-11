"""Module with functions used to extract data from the Spotify API."""

import base64
import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv
import pandas as pd
import requests

from exceptions import (
    APIRequestException,
    EmptyDataFrameException,
    NonUniquePrimaryKeyException,
    NullValuesFoundException,
)

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE64_ID_SECRET = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()


def get_yesterday_unix_timestamp() -> int:
    """Get yesterday's Unix timestamp in milliseconds."""

    today = datetime.now()
    yesterday = today - timedelta(hours=2)
    return int(yesterday.timestamp()) * 1000


def get_token() -> str:
    """Get Spotify API token."""

    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {BASE64_ID_SECRET}",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": os.getenv("REFRESH_TOKEN"),
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise APIRequestException(url=url, response=response.json())

    return response.json()["access_token"]


TOKEN = get_token()


def get_recently_played(token: str) -> dict:
    """Get recently played tracks."""

    url = "https://api.spotify.com/v1/me/player/recently-played"
    response = requests.get(
        url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        params={"limit": 50, "after": get_yesterday_unix_timestamp()},
        timeout=60,
    )

    if response.status_code != 200:
        raise APIRequestException(url=url, response=response.json())

    return response.json()


def get_artists_genres(artist_id: str, token: str) -> list:
    """Get artists genres"""

    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )

    if response.status_code != 200:
        raise APIRequestException(url=url, response=response.json())

    return response.json()["genres"]


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


def run_etl():
    """Run the ETL process."""

    recently_played = extract()

    transformed_data = transform(df=recently_played)

    file_path = "./played_tracks.csv"

    if not os.path.isfile(file_path):
        transformed_data.to_csv(file_path, index=False)
        sys.exit()
    transformed_data.to_csv(file_path, mode="a", index=False, header=False)

    df = pd.read_csv(file_path).drop_duplicates()
    df.to_csv(file_path, mode="w", index=False)
