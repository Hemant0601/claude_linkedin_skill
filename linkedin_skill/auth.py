"""LinkedIn OAuth 2.0 authentication flow."""

import json
import urllib.parse
import threading
import http.server
import requests

from .config import load_config, save_tokens, load_tokens, clear_tokens

AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# LinkedIn OAuth scopes
SCOPES = [
    "openid",
    "profile",
    "email",
    "w_member_social",
]


def get_authorization_url():
    """Generate the LinkedIn OAuth authorization URL."""
    config = load_config()
    if not config["client_id"]:
        return None, "LINKEDIN_CLIENT_ID not set. Please configure your .env file."

    params = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "scope": " ".join(SCOPES),
        "state": "claude_linkedin_skill",
    }
    url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    return url, None


def exchange_code_for_token(authorization_code):
    """Exchange an authorization code for an access token."""
    config = load_config()
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config["redirect_uri"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code != 200:
        return None, f"Token exchange failed: {response.status_code} - {response.text}"

    token_data = response.json()
    save_tokens(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
    )
    return token_data["access_token"], None


def start_auth_flow():
    """Start the full OAuth flow with a local callback server.

    Returns a dict with auth_url and waits for the callback.
    """
    url, error = get_authorization_url()
    if error:
        return {"error": error}

    result = {"auth_url": url, "status": "waiting"}
    auth_code_holder = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if "code" in params:
                auth_code_holder["code"] = params["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"<html><body><h2>LinkedIn authentication successful!</h2>"
                    b"<p>You can close this window and return to Claude Code.</p>"
                    b"</body></html>"
                )
            else:
                error_msg = params.get("error_description", ["Unknown error"])[0]
                auth_code_holder["error"] = error_msg
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(f"<html><body><h2>Error: {error_msg}</h2></body></html>".encode())

        def log_message(self, format, *args):
            pass  # Suppress server logs

    config = load_config()
    parsed_uri = urllib.parse.urlparse(config["redirect_uri"])
    port = parsed_uri.port or 8585

    server = http.server.HTTPServer(("localhost", port), CallbackHandler)
    server.timeout = 120  # 2 minute timeout

    result["message"] = (
        f"Open this URL in your browser to authenticate:\n\n{url}\n\n"
        f"Waiting for callback on port {port}..."
    )

    server.handle_request()
    server.server_close()

    if "code" in auth_code_holder:
        token, error = exchange_code_for_token(auth_code_holder["code"])
        if error:
            result["status"] = "error"
            result["error"] = error
        else:
            result["status"] = "authenticated"
            result["message"] = "Successfully authenticated with LinkedIn!"
    elif "error" in auth_code_holder:
        result["status"] = "error"
        result["error"] = auth_code_holder["error"]
    else:
        result["status"] = "timeout"
        result["error"] = "Authentication timed out. Please try again."

    return result


def check_auth_status():
    """Check if user is currently authenticated."""
    tokens = load_tokens()
    if not tokens or not tokens.get("access_token"):
        return {"authenticated": False, "message": "Not authenticated. Run `linkedin auth` to connect."}

    import time
    expires_at = tokens.get("expires_at")
    if expires_at and time.time() > expires_at:
        return {"authenticated": False, "message": "Token expired. Run `linkedin auth` to reconnect."}

    return {"authenticated": True, "message": "Authenticated with LinkedIn."}


def logout():
    """Clear stored tokens."""
    clear_tokens()
    return {"message": "Logged out. Tokens cleared."}
