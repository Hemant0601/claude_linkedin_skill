#!/usr/bin/env python3
"""CLI entry point for LinkedIn skill operations."""

import sys
import json
from . import auth
from .config import load_config, get_access_token
from .operations import profile, posts, engagement, connections


def print_json(data):
    print(json.dumps(data, indent=2))


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    # --- Authentication ---
    if command == "auth":
        result = auth.start_auth_flow()
        print_json(result)

    elif command == "auth-status":
        result = auth.check_auth_status()
        print_json(result)

    elif command == "auth-url":
        url, error = auth.get_authorization_url()
        if error:
            print_json({"error": error})
        else:
            print_json({"auth_url": url})

    elif command == "auth-callback":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin auth-callback <authorization_code>"})
            return
        token, error = auth.exchange_code_for_token(sys.argv[2])
        if error:
            print_json({"error": error})
        else:
            print_json({"status": "authenticated", "message": "Successfully authenticated!"})

    elif command == "logout":
        result = auth.logout()
        print_json(result)

    # --- Profile ---
    elif command == "profile":
        result = profile.get_profile()
        print_json(result)

    # --- Posts ---
    elif command == "post":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin post <text> [--visibility PUBLIC|CONNECTIONS]"})
            return
        text = sys.argv[2]
        visibility = "PUBLIC"
        if "--visibility" in sys.argv:
            idx = sys.argv.index("--visibility")
            if idx + 1 < len(sys.argv):
                visibility = sys.argv[idx + 1]
        result = posts.create_text_post(text, visibility)
        print_json(result)

    elif command == "post-article":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin post-article <text> <url> [--title T] [--desc D]"})
            return
        text, url = sys.argv[2], sys.argv[3]
        title = _get_flag("--title")
        desc = _get_flag("--desc")
        result = posts.create_article_post(text, url, title, desc)
        print_json(result)

    elif command == "post-image":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin post-image <text> <image_url>"})
            return
        result = posts.create_image_post(sys.argv[2], sys.argv[3])
        print_json(result)

    elif command == "delete-post":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin delete-post <post_urn>"})
            return
        result = posts.delete_post(sys.argv[2])
        print_json(result)

    elif command == "org-post":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin org-post <org_id> <text>"})
            return
        result = posts.create_org_post(sys.argv[2], sys.argv[3])
        print_json(result)

    # --- Engagement ---
    elif command == "react":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin react <post_urn> [LIKE|PRAISE|EMPATHY|INTEREST|APPRECIATION]"})
            return
        reaction = sys.argv[3] if len(sys.argv) > 3 else "LIKE"
        result = engagement.react_to_post(sys.argv[2], reaction)
        print_json(result)

    elif command == "comment":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin comment <post_urn> <text>"})
            return
        result = engagement.comment_on_post(sys.argv[2], sys.argv[3])
        print_json(result)

    elif command == "get-comments":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin get-comments <post_urn>"})
            return
        result = engagement.get_comments(sys.argv[2])
        print_json(result)

    elif command == "analytics":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin analytics <post_urn>"})
            return
        result = engagement.get_post_analytics(sys.argv[2])
        print_json(result)

    # --- Connections ---
    elif command == "connect":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin connect <profile_urn> [--message M]"})
            return
        msg = _get_flag("--message")
        result = connections.send_connection_request(sys.argv[2], msg)
        print_json(result)

    elif command == "connections-count":
        result = connections.get_connections_count()
        print_json(result)

    else:
        print(f"Unknown command: {command}")
        print_usage()


def _get_flag(flag):
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return None


def print_usage():
    print("""LinkedIn Skill CLI

Authentication:
  auth              Start OAuth flow (opens browser)
  auth-status       Check authentication status
  auth-url          Get authorization URL only
  auth-callback <code>  Exchange auth code for token
  logout            Clear stored tokens

Profile:
  profile           View your LinkedIn profile

Posts:
  post <text>                       Create a text post
  post-article <text> <url>         Post with article link
  post-image <text> <image_url>     Post with image
  delete-post <post_urn>            Delete a post
  org-post <org_id> <text>          Post as organization

Engagement:
  react <post_urn> [type]           React to a post
  comment <post_urn> <text>         Comment on a post
  get-comments <post_urn>           Get post comments
  analytics <post_urn>              Get post engagement stats

Network:
  connect <profile_urn> [--message M]  Send connection request
  connections-count                     Get connection count
""")


if __name__ == "__main__":
    main()
