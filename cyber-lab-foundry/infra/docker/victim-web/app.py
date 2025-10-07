from __future__ import annotations

import os
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for

APP_SECRET = os.environ.get("APP_SECRET", "not-for-production")
DATABASE_PATH = Path("/app/data.sqlite")
LOG_PATH = Path("/var/log/victim-web/app.log")
ENABLE_RISKY = os.environ.get("ENABLE_RISKY", "false").lower() == "true"
UPLOAD_DIR = Path("/tmp/uploads")

app = Flask(__name__)
app.secret_key = APP_SECRET


def init_db() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)"
        )
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("victim", "WeakPass123!"),
        )
    conn.close()


def log_event(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"{datetime.utcnow().isoformat()}Z {message}\n")


@app.route("/", methods=["GET"])
def index() -> str:
    if session.get("user"):
        return render_template("dashboard.html", username=session["user"], risky=ENABLE_RISKY)
    return render_template("login.html", risky=ENABLE_RISKY)


@app.route("/login", methods=["POST"])
def login() -> Response:
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    query = (
        "SELECT username FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )
    conn = sqlite3.connect(DATABASE_PATH)
    log_event(f"LOGIN attempt user={username} query={query}")
    row = conn.execute(query).fetchone()
    conn.close()
    if row:
        session["user"] = row[0]
        log_event(f"LOGIN success user={username}")
        return redirect(url_for("index"))
    flash("Invalid credentials")
    log_event(f"LOGIN failed user={username}")
    return redirect(url_for("index"))


@app.route("/upload", methods=["POST"])
def upload() -> Response:
    if not session.get("user"):
        flash("Authenticate first")
        return redirect(url_for("index"))
    if not ENABLE_RISKY:
        flash("Risky functionality is disabled. Enable via ENABLE_RISKY=true for the scenario.")
        return redirect(url_for("index"))
    file = request.files.get("webshell")
    if file is None or file.filename == "":
        flash("No file provided")
        return redirect(url_for("index"))
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOAD_DIR / file.filename
    file.save(dest)
    log_event(f"UPLOAD stored filename={dest}")
    if dest.suffix in {".py", ".sh"}:
        try:
            output = subprocess.check_output(["/bin/bash", "-c", f"python3 {dest}"])
            log_event(f"UPLOAD executed filename={dest} output={output.decode('utf-8', 'ignore')}")
        except subprocess.CalledProcessError as exc:
            log_event(f"UPLOAD execution failed filename={dest} rc={exc.returncode}")
    flash(f"File {file.filename} uploaded")
    return redirect(url_for("index"))


@app.route("/healthz", methods=["GET"])
def healthcheck() -> tuple[str, int]:
    return "ok", 200


@app.route("/logs", methods=["GET"])
def fetch_logs() -> Response:
    if not session.get("user"):
        return Response("Unauthorized", status=401)
    if not LOG_PATH.exists():
        return Response("No logs yet", mimetype="text/plain")
    return Response(LOG_PATH.read_text(encoding="utf-8"), mimetype="text/plain")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
else:
    init_db()
