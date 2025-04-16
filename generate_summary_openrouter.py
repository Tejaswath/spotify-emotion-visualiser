import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def generate_vibe_summary(df_emotions: pd.DataFrame) -> str:
    # Use 'track_name' instead of 'track' because your DataFrame has a column 'track_name'
    track_lines = [
        f"{i+1}. {row['track_name']} — {row['mood']}" for i, row in df_emotions.iterrows()
    ]
    track_summary = "\n".join(track_lines)

    prompt = (
        "Your job is to roast, romanticize, and reflect on someone’s music taste like it’s the last entry in their therapy journal. "
        "They just shared their top 20 songs with emotion tags like ‘depressed’, ‘euphoric’, ‘neutral’, etc. Your mission: write a wildly perceptive, hilariously chaotic one-paragraph reflection "
        "that hits hard emotionally but sounds like a Gen-Z bestie who saw their soul through a playlist.\n\n"
        "What the paragraph MUST include:\n"
        "- Direct references to a few specific song titles in quotes.\n"
        "- Weirdly poetic language mixed with brutal honesty.\n"
        "- Sarcasm, sass, and a ‘main character who’s secretly in a spiral’ tone.\n"
        "- A final mic-drop tweet-style one-liner that makes people laugh, then stare at the wall.\n"
        "- NO hashtags, NO listicles, NO filter.\n\n"
        f"Here’s the top 20 songs and their emotional labels:\n{track_summary}\n\n"
        "Now give me the vibe check:"
    )

    body = {
        "model": "meta-llama/llama-3-8b-instruct:nitro",
        "messages": [
            {"role": "system", "content": "You are an emotionally intelligent Gen-Z AI vibe analyst."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=body)
        data = response.json()

        # DEBUG PRINT
        print("🧠 FULL OpenRouter Response:")
        print(data)

        # ✅ Safe extraction: Check if we have the expected structure.
        if isinstance(data, dict) and "choices" in data:
            first_choice = data["choices"][0]
            if isinstance(first_choice, dict) and "message" in first_choice:
                return first_choice["message"]["content"].strip()

        # Fallback: Return the whole response if the structure is not expected.
        return f"⚠️ Unexpected LLM output format:\n\n{data}"

    except Exception as e:
        print("❌ Error parsing response:", e)
        return "Summary generation failed (LLM parsing error)."

# ------------------------
# ✅ CLI Mode (optional)
# ------------------------
if __name__ == "__main__":
    try:
        df = pd.read_csv("data/top_tracks_emotions.csv")
        # Ensure that the CSV has columns 'track_name' and 'mood'
        df = df.dropna(subset=["track_name", "mood"])
        summary = generate_vibe_summary(df)
        pd.DataFrame([{"vibe_summary": summary}]).to_csv("data/top_tracks_summary.csv", index=False)
        print("✅ Vibe summary saved to: data/top_tracks_summary.csv")
    except FileNotFoundError:
        print("⚠️ Error: Make sure data/top_tracks_emotions.csv exists.")