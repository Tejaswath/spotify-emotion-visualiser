# main_flow.py

import os
import spotipy
from fetch_tracks_and_lyrics import get_top_tracks_with_lyrics
from analyze_emotions import analyze_emotions as analyze_tracks
from generate_summary_openrouter import generate_vibe_summary

def create_spotify_client(access_token):
    """
    Returns a spotipy Spotify client using the given access token.
    """
    return spotipy.Spotify(auth=access_token)

def run_emotion_pipeline(access_token):
    """
    Full pipeline: Spotify top tracks → lyrics → emotion analysis → LLM vibe summary
    """
    sp = create_spotify_client(access_token)

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