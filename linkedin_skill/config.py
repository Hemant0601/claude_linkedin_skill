"""Configuration management for LinkedIn skill."""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

CONFIG_DIR = Path.home() / ".config" / "claude-linkedin-skill"
TOKEN_FILE = CONFIG_DIR / "tokens.json"


def load_config():
    """Load configuration from environment and .env file."""
    load_dotenv()
    return {
        "client_id": os.getenv("LINKEDIN_CLIENT_ID", ""),
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8585/callback"),
    }


def save_tokens(access_token, refresh_token=None, expires_in=None):
    """Save OAuth tokens to local config."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {"access_token": access_token}
    if refresh_token:
        data["refresh_token"] = refresh_token
    if expires_in:
        import time
        data["expires_at"] = int(time.time()) + expires_in
    TOKEN_FILE.write_text(json.dumps(data, indent=2))
    TOKEN_FILE.chmod(0o600)


def load_tokens():
    """Load saved OAuth tokens."""
    if TOKEN_FILE.exists():
        data = json.loads(TOKEN_FILE.read_text())
        return data
    # Fallback to environment variable
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    if token:
        return {"access_token": token}
    return None


def clear_tokens():
    """Remove saved tokens."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()


def get_access_token():
    """Get the current access token or None."""
    tokens = load_tokens()
    if not tokens:
        return None
    import time
    expires_at = tokens.get("expires_at")
    if expires_at and time.time() > expires_at:
        return None
    return tokens.get("access_token")
