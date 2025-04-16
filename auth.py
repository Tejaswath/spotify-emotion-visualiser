# auth.py

import os
import requests
from urllib.parse import urlencode
from flask import session
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-top-read"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_auth_url():
    """
    Generates Spotify authorization URL with required query params.
    """
    session['state'] = os.urandom(16).hex()
    params = {
        "client_id": SPOTIPY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIPY_REDIRECT_URI,
        "scope": SCOPE,
        "state": session['state'],
        "show_dialog": "true"
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def get_token(code):
    """
    Exchanges authorization code for access token.
    """
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIPY_REDIRECT_URI,
        "client_id": SPOTIPY_CLIENT_ID,
        "client_secret": SPOTIPY_CLIENT_SECRET
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching access token:", e)
        return None