"""Lambda function to get recently played songs from Spotify API and store them in a SQLite database."""
import pandas as pd
from sqlalchemy import create_engine

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



if __name__ == "__main__":
    recently_played = extract()
