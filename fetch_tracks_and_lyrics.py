# fetch_tracks_and_lyrics.py

import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

AUDD_API_TOKEN = os.getenv("AUDD_API_TOKEN")

def get_top_tracks_with_lyrics(sp):
    """
    Gets user's top 20 tracks from Spotify and fetches lyrics using AudD findLyrics endpoint.
    Returns a DataFrame with track_name, artist_name, lyrics.
    """
    results = sp.current_user_top_tracks(limit=20, time_range="medium_term")
    tracks = []

    for item in results["items"]:
        track_name = item["name"]
        artist_name = item["artists"][0]["name"]
        print(f"🔍 Searching lyrics for: {track_name} by {artist_name}")

        # Build the query from song title + artist name
        query = f"{track_name} {artist_name}"
        lyrics = None

        try:
            # ✅ Use the 'findLyrics' endpoint
            response = requests.post(
                "https://api.audd.io/findLyrics/",  # note the trailing slash
                data={
                    "api_token": AUDD_API_TOKEN,
                    "q": query
                }
            )
            data = response.json()

            # If status=success and result is a list of songs
            if data.get("status") == "success" and isinstance(data.get("result"), list):
                all_matches = data["result"]
                if all_matches:
                    # Just pick the first match
                    best_match = all_matches[0]
                    lyrics = best_match.get("lyrics")
                    print(f"✅ Found lyrics for: {track_name} by {artist_name}")
                else:
                    print(f"⚠️ No lyrics found in AudD result list for: {track_name} by {artist_name}")
            else:
                print(f"⚠️ AudD did not return lyrics for: {track_name} by {artist_name} - {data}")

        except Exception as e:
            print(f"❌ Error fetching lyrics for {track_name} by {artist_name}: {e}")

        tracks.append({
            "track_name": track_name,
            "artist_name": artist_name,
            "lyrics": lyrics
        })

    # Filter out tracks with no lyrics
    df = pd.DataFrame(tracks)
    df = df.dropna(subset=["lyrics"]).reset_index(drop=True)
    print(f"🎯 Found lyrics for {len(df)} out of {len(tracks)} tracks.")
    return df