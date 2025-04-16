# fetch_tracks_and_lyrics.py

import os
import pandas as pd
from lyricsgenius import Genius

genius = Genius(os.getenv("GENIUS_API_TOKEN"), timeout=15, retries=3)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]


def get_top_tracks_with_lyrics(sp):
    """
    Gets user's top 20 tracks from Spotify and fetches lyrics using Genius API.
    Returns a DataFrame with track name, artist, and lyrics.
    """
    results = sp.current_user_top_tracks(limit=20, time_range='medium_term')
    tracks = []

    for item in results["items"]:
        track_name = item["name"]
        artist_name = item["artists"][0]["name"]

        # Try fetching lyrics
        lyrics = None
        try:
            song = genius.search_song(track_name, artist_name)
            if song:
                lyrics = song.lyrics
        except Exception as e:
            print(f"Could not fetch lyrics for {track_name} by {artist_name}: {e}")

        tracks.append({
            "track_name": track_name,
            "artist_name": artist_name,
            "lyrics": lyrics
        })

    # Filter out tracks with no lyrics
    df = pd.DataFrame(tracks)
    df = df.dropna(subset=["lyrics"]).reset_index(drop=True)
    return df