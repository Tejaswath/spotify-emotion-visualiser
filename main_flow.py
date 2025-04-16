# main_flow.py

import os
import pandas as pd
from fetch_tracks_and_lyrics import get_top_tracks_with_lyrics
from analyze_emotions import analyze_emotions as analyze_tracks
from generate_summary_openrouter import generate_vibe_summary
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read"
    )

def get_spotify_client_with_refresh(token_info):
    sp_oauth = create_spotify_oauth()

    if sp_oauth.is_token_expired(token_info):
        print("🔄 Access token expired. Refreshing...")
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    access_token = token_info["access_token"]
    return spotipy.Spotify(auth=access_token), token_info

def run_emotion_pipeline(token_info):
    """
    Main pipeline: fetch Spotify tracks → fetch lyrics (AudD) → analyze emotions → generate vibe summary.
    """
    sp, token_info = get_spotify_client_with_refresh(token_info)

    print("[1/4] Fetching top tracks and lyrics...")
    tracks_df = get_top_tracks_with_lyrics(sp)

    if tracks_df.empty:
        return {"error": "No lyrics found for top tracks."}

    print("[2/4] Analyzing emotional tone...")
    analyzed_df = analyze_tracks(tracks_df)

    print("[3/4] Generating LLM-based vibe summary...")
    vibe_summary = generate_vibe_summary(analyzed_df)

    print("[4/4] Done.")
    return {
        "tracks": analyzed_df,
        "summary": vibe_summary
    }