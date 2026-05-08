from pathlib import Path
import os

from flask import Flask, send_from_directory


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    """Small production-friendly headers for public hosting."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/index.css")
def styles():
    return send_from_directory(BASE_DIR, "index.css", max_age=3600)


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(BASE_DIR / "assets", filename, max_age=86400)


@app.route("/healthz")
def health_check():
    return {"status": "ok"}


# Future idea: add an /uploads route and an upload folder if you want guests
# to submit photos. For now, the site stays fast and static-friendly.


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
