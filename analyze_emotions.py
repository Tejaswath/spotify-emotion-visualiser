import pandas as pd

def analyze_emotions(df_with_lyrics: pd.DataFrame) -> pd.DataFrame:
    df = df_with_lyrics.dropna(subset=["lyrics"]).copy()

    valence_scores = []
    mood_labels = []

    for idx, row in df.iterrows():
        text = row["lyrics"][:512]
        valence = 0.2 if "love" in text.lower() else -0.2

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

    return df