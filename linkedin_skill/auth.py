"""LinkedIn authentication - direct login, no developer app needed."""

import getpass
from linkedin_api import Linkedin

from .config import save_session, load_session, clear_session, is_logged_in


def login(username=None, password=None):
    """Log in to LinkedIn with email/password.

    The linkedin-api library handles the session/cookies automatically.
    We store the username so future operations can re-authenticate.
    """
    if not username:
        username = input("LinkedIn email: ")
    if not password:
        password = getpass.getpass("LinkedIn password: ")

    try:
        # This authenticates with LinkedIn directly (like a browser would)
        api = Linkedin(username, password)
        profile = api.get_user_profile()
        display_name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip()

        save_session(username)

        return {
            "status": "success",
            "message": f"Logged in as {display_name or username}",
            "profile": {
                "name": display_name,
                "headline": profile.get("headline", ""),
            },
        }
    except Exception as e:
        return {"status": "error", "message": f"Login failed: {str(e)}"}


def check_status():
    """Check if user is logged in."""
    if is_logged_in():
        session = load_session()
        return {
            "authenticated": True,
            "username": session.get("username"),
            "message": f"Logged in as {session['username']}",
        }
    return {
        "authenticated": False,
        "message": "Not logged in. Run: python -m linkedin_skill.cli login",
    }


def logout():
    """Clear stored session."""
    clear_session()
    return {"message": "Logged out. Session cleared."}


def get_client(username=None, password=None):
    """Get an authenticated LinkedIn client.

    If credentials aren't passed, prompts the user.
    """
    session = load_session()
    if not session:
        raise RuntimeError("Not logged in. Run: python -m linkedin_skill.cli login")

    uname = username or session.get("username")
    if not uname:
        raise RuntimeError("No username found. Please log in again.")

    # The user will need to provide password for each new session
    # linkedin-api handles cookie caching internally
    pwd = password or getpass.getpass(f"LinkedIn password for {uname}: ")
    return Linkedin(uname, pwd)
