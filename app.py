# app.py

from flask import Flask, render_template, request, redirect, session
from auth import get_auth_url, get_token
from main_flow import run_emotion_pipeline
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
    if "token_info" not in session:
        return render_template("index.html", auth_url=get_auth_url(), authorized=False)
    return render_template("index.html", authorized=True)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if code:
        token_info = get_token(code)
        if token_info and "access_token" in token_info:
            session["token_info"] = token_info
    return redirect("/")

@app.route("/scan")
def scan():
    if "token_info" not in session:
        return redirect("/")

    try:
        token_info = session.get("token_info")
        access_token = token_info["access_token"]

        # Refresh token if expired
        from spotipy.oauth2 import SpotifyOAuth
        sp_oauth = SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-top-read"
        )
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            session["token_info"] = token_info
            access_token = token_info["access_token"]

        results = run_emotion_pipeline(access_token)

        if "error" in results:
            return render_template("index.html", error=results["error"], authorized=True)

        return render_template(
            "index.html",
            results=results["tracks"].to_dict(orient="records"),
            summary=results["summary"],
            authorized=True
        )

    except Exception as e:
        return render_template("index.html", error=str(e), authorized=True)

# ✅ Render-compatible block
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port, debug=True)