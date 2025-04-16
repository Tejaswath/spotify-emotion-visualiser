# analyze_emotions.py

import pandas as pd
from transformers import pipeline

# Load sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_emotions(df_with_lyrics: pd.DataFrame) -> pd.DataFrame:
    df = df_with_lyrics.dropna(subset=["lyrics"]).copy()

    valence_scores = []
    mood_labels = []

    for idx, row in df.iterrows():
        snippet = row["lyrics"][:512]

        try:
            result = sentiment_pipeline(snippet)[0]
            stars = int(result["label"][0])  # "4 stars" → 4
            valence = (stars - 3) / 2        # Normalize to -1 to 1
        except Exception as e:
            print(f"⚠️ Sentiment error on track {row['track_name']}: {e}")
            valence = 0

        valence_scores.append(round(valence, 3))

        if valence > 0.5:
            mood = "euphoric"
        elif valence > 0.1:
            mood = "happy"
        elif valence < -0.5:
            mood = "depressed"
        elif valence < -0.1:
            mood = "melancholy"
        else:
            mood = "neutral"

        mood_labels.append(mood)

    df["valence"] = valence_scores
    df["mood"] = mood_labels

    # 🔐 Fix for vibe summary
    df["track"] = df["track_name"]

    return df