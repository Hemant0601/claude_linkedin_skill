"""Configuration management for LinkedIn skill - stores session cookies securely."""

import json
import time
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "claude-linkedin-skill"
SESSION_FILE = CONFIG_DIR / "session.json"


def save_session(username, cookies=None):
    """Save LinkedIn session info locally."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "username": username,
        "authenticated_at": int(time.time()),
    }
    if cookies:
        data["cookies"] = cookies
    SESSION_FILE.write_text(json.dumps(data, indent=2))
    SESSION_FILE.chmod(0o600)


def load_session():
    """Load saved session info."""
    if SESSION_FILE.exists():
        return json.loads(SESSION_FILE.read_text())
    return None


def clear_session():
    """Remove saved session."""
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def is_logged_in():
    """Check if there's an active session."""
    session = load_session()
    return session is not None and "username" in session
