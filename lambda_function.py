"""Lambda function to get recently played songs from Spotify API."""

from spotify_etl import run_etl

def lambda_handler(event, context):
    run_etl()