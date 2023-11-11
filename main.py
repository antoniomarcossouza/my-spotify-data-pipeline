"""Lambda function to get recently played songs from Spotify API."""

from spotify_etl import run_etl


if __name__ == "__main__":
    run_etl()
