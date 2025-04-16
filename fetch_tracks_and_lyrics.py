import os
import pandas as pd
from lyricsgenius import Genius

genius = Genius(
    os.getenv("GENIUS_API_TOKEN"),
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    timeout=15,
    retries=3,
    remove_section_headers=True
)

# Force the use of the old scraping method (unofficial trick)
genius._session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
})

def get_top_tracks_with_lyrics(sp):
    print("🎧 Fetching top tracks from Spotify...")
    results = sp.current_user_top_tracks(limit=20, time_range='medium_term')
    tracks = []

    for item in results["items"]:
        track_name = item["name"]
        artist_name = item["artists"][0]["name"]

        print(f"🎤 Searching lyrics for: {track_name} by {artist_name}")
        lyrics = None
        try:
            song = genius.search_song(track_name, artist_name)
            if song:
                lyrics = song.lyrics
        except Exception as e:
            print(f"⚠️ Could not fetch lyrics for {track_name} by {artist_name}: {e}")

        tracks.append({
            "track_name": track_name,
            "artist_name": artist_name,
            "lyrics": lyrics
        })

    df = pd.DataFrame(tracks)
    df = df.dropna(subset=["lyrics"]).reset_index(drop=True)
    print(f"🎯 Total tracks with lyrics: {len(df)}")
    return df