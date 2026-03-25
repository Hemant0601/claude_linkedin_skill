"""LinkedIn authentication via local browser-based login."""

import http.server
import json
import threading
import urllib.parse
import webbrowser

from linkedin_api import Linkedin

from .config import save_session, load_session, clear_session, is_logged_in

LOGIN_PAGE_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Login - Claude Code Skill</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f3f2ef; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; }
        .card { background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                padding: 40px; width: 400px; }
        h1 { color: #0a66c2; font-size: 24px; margin-bottom: 8px; }
        p { color: #666; font-size: 14px; margin-bottom: 24px; }
        label { display: block; font-size: 14px; font-weight: 600; color: #333; margin-bottom: 4px; }
        input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px;
                font-size: 16px; margin-bottom: 16px; }
        input:focus { outline: none; border-color: #0a66c2; box-shadow: 0 0 0 1px #0a66c2; }
        button { width: 100%; padding: 12px; background: #0a66c2; color: white; border: none;
                 border-radius: 24px; font-size: 16px; font-weight: 600; cursor: pointer; }
        button:hover { background: #004182; }
        .note { font-size: 12px; color: #999; margin-top: 16px; text-align: center; }
        .error { color: #cc1016; font-size: 14px; margin-bottom: 16px; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Sign in to LinkedIn</h1>
        <p>Connect your LinkedIn account to Claude Code</p>
        <div class="error" id="error"></div>
        <form method="POST" action="/login">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" placeholder="your@email.com" required>
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <button type="submit">Sign in</button>
        </form>
        <p class="note">Your credentials are sent directly to LinkedIn.<br>
        They are never stored or logged by this skill.</p>
    </div>
</body>
</html>"""

SUCCESS_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Connected!</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f3f2ef; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; }
        .card { background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                padding: 40px; width: 400px; text-align: center; }
        h1 { color: #057642; font-size: 24px; margin-bottom: 8px; }
        p { color: #666; font-size: 14px; }
        .check { font-size: 48px; margin-bottom: 16px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="check">&#10003;</div>
        <h1>Connected as DISPLAY_NAME</h1>
        <p>You can close this window and return to Claude Code.</p>
    </div>
</body>
</html>"""

ERROR_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Login Failed</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f3f2ef; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; }
        .card { background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                padding: 40px; width: 400px; text-align: center; }
        h1 { color: #cc1016; font-size: 24px; margin-bottom: 8px; }
        p { color: #666; font-size: 14px; }
        a { color: #0a66c2; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Login Failed</h1>
        <p>ERROR_MSG</p>
        <p style="margin-top:16px"><a href="/">Try again</a></p>
    </div>
</body>
</html>"""


def start_login_server(port=8585):
    """Start a local web server for browser-based LinkedIn login.

    Opens the browser to a login page. User enters credentials there.
    Credentials go directly to LinkedIn API — never stored or logged.
    Returns result dict with login status.
    """
    result = {"status": "waiting"}

    class LoginHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(LOGIN_PAGE_HTML.encode())

        def do_POST(self):
            if self.path == "/login":
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode()
                params = urllib.parse.parse_qs(body)
                email = params.get("email", [""])[0]
                password = params.get("password", [""])[0]

                try:
                    api = Linkedin(email, password)
                    profile = api.get_user_profile()
                    display_name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip()

                    save_session(email)

                    result["status"] = "success"
                    result["message"] = f"Logged in as {display_name or email}"
                    result["profile"] = {
                        "name": display_name,
                        "headline": profile.get("headline", ""),
                    }

                    html = SUCCESS_HTML.replace("DISPLAY_NAME", display_name or email)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(html.encode())

                except Exception as e:
                    error_msg = str(e)
                    if "CHALLENGE" in error_msg.upper():
                        error_msg = "LinkedIn requires verification. Please log in at linkedin.com first, then try again."
                    result["status"] = "error"
                    result["message"] = f"Login failed: {error_msg}"

                    html = ERROR_HTML.replace("ERROR_MSG", error_msg)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(html.encode())
                    return  # Don't shut down server — let user retry

                # Signal server to stop after successful login
                threading.Thread(target=self.server.shutdown).start()
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass  # Suppress server logs

    server = http.server.HTTPServer(("localhost", port), LoginHandler)
    server.timeout = 300  # 5 minute timeout

    login_url = f"http://localhost:{port}"
    result["login_url"] = login_url
    result["message"] = f"Open this URL to sign in:\n\n{login_url}\n\nWaiting for login..."

    # Try to open the browser automatically
    try:
        webbrowser.open(login_url)
    except Exception:
        pass  # Browser open is best-effort

    server.serve_forever()

    if result["status"] == "waiting":
        result["status"] = "timeout"
        result["message"] = "Login timed out. Please try again."

    return result


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
