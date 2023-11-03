"""API for the Spotify API Authorization Flow"""
import base64
import os
import urllib

from dotenv import load_dotenv
from flask import Flask, redirect, request
import requests

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
BASE_ID_SECRET = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()


app = Flask(__name__)


@app.route("/")
def authorize():
    """Construct the Spotify authorization URL"""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-recently-played",
        "show_dialog": "true",
    }
    auth_redirect_url = (
        f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    )
    return redirect(auth_redirect_url)


@app.route("/callback")
def callback():
    """Handle the callback with the authorization code"""
    auth_code = request.args["code"]

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {BASE_ID_SECRET}",
        },
        data={
            "grant_type": "authorization_code",
            "code": str(auth_code),
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        timeout=60,
    )
    return response.json()


if __name__ == "__main__":
    app.run(port=8000)
