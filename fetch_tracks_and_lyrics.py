# fetch_tracks_and_lyrics.py

import os
import pandas as pd
import requests

AUDD_API_TOKEN = os.getenv("AUDD_API_TOKEN")
AUDD_API_URL = "https://api.audd.io/"

def get_top_tracks_with_lyrics(sp):
    """
    Gets user's top 20 tracks from Spotify and fetches lyrics using AudD API.
    Returns a DataFrame with track name, artist, and lyrics.
    """
    results = sp.current_user_top_tracks(limit=20, time_range='medium_term')
    tracks = []

    for item in results["items"]:
        track_name = item["name"]
        artist_name = item["artists"][0]["name"]

        print(f"🎤 Searching lyrics for: {track_name} by {artist_name}")

        try:
            response = requests.post(AUDD_API_URL, data={
                "q": f"{track_name} {artist_name}",
                "api_token": AUDD_API_TOKEN,
                "return": "lyrics"
            })

            data = response.json()
            lyrics = None

            if data.get("status") == "success" and data.get("result") and "lyrics" in data["result"]:
                lyrics = data["result"]["lyrics"]
            else:
                print(f"⚠️ No lyrics found for {track_name} by {artist_name} - {data}")

        except Exception as e:
            print(f"❌ Error fetching lyrics for {track_name} by {artist_name}: {e}")
            lyrics = None

        tracks.append({
            "track_name": track_name,
            "artist_name": artist_name,
            "lyrics": lyrics
        })

    df = pd.DataFrame(tracks)
    df = df.dropna(subset=["lyrics"]).reset_index(drop=True)
    print(f"🎯 Total tracks with lyrics: {len(df)}")
    return df