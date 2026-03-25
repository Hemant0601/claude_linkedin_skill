#!/usr/bin/env python3
"""CLI entry point for LinkedIn skill - no developer app needed."""

import sys
import json
from . import auth
from .operations import profile, posts, engagement, connections, messaging, search


def print_json(data):
    print(json.dumps(data, indent=2, default=str))


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    # --- Authentication ---
    if command == "login":
        port = int(_get_flag("--port") or 8585)
        result = auth.start_login_server(port)
        print_json(result)

    elif command == "status":
        result = auth.check_status()
        print_json(result)

    elif command == "logout":
        result = auth.logout()
        print_json(result)

    # --- Profile ---
    elif command == "me":
        result = profile.get_my_profile()
        print_json(result)

    elif command == "profile":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin profile <public_id>"})
            return
        result = profile.view_profile(sys.argv[2])
        print_json(result)

    # --- Search ---
    elif command == "search-people":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin search-people <keywords>"})
            return
        limit = int(_get_flag("--limit") or 10)
        result = search.search_people(sys.argv[2], limit)
        print_json(result)

    elif command == "search-companies":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin search-companies <keywords>"})
            return
        limit = int(_get_flag("--limit") or 10)
        result = search.search_companies(sys.argv[2], limit)
        print_json(result)

    elif command == "search-jobs":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin search-jobs <keywords>"})
            return
        limit = int(_get_flag("--limit") or 10)
        result = search.search_jobs(sys.argv[2], limit)
        print_json(result)

    # --- Posts ---
    elif command == "post":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin post <text> [--visibility PUBLIC|CONNECTIONS]"})
            return
        text = sys.argv[2]
        visibility = _get_flag("--visibility") or "PUBLIC"
        result = posts.create_text_post(text, visibility)
        print_json(result)

    elif command == "post-link":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin post-link <text> <url> [--title T]"})
            return
        title = _get_flag("--title")
        result = posts.create_link_post(sys.argv[2], sys.argv[3], title)
        print_json(result)

    elif command == "delete-post":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin delete-post <post_urn>"})
            return
        result = posts.delete_post(sys.argv[2])
        print_json(result)

    # --- Feed ---
    elif command == "feed":
        limit = int(_get_flag("--limit") or 10)
        result = engagement.get_feed(limit)
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

    # --- Connections ---
    elif command == "connect":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin connect <public_id> [--message M]"})
            return
        msg = _get_flag("--message")
        result = connections.send_connection_request(sys.argv[2], msg)
        print_json(result)

    elif command == "disconnect":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin disconnect <public_id>"})
            return
        result = connections.remove_connection(sys.argv[2])
        print_json(result)

    elif command == "invitations":
        result = connections.get_pending_invitations()
        print_json(result)

    elif command == "accept":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin accept <invitation_id> <shared_secret>"})
            return
        result = connections.accept_invitation(sys.argv[2], sys.argv[3])
        print_json(result)

    # --- Messaging ---
    elif command == "conversations":
        limit = int(_get_flag("--limit") or 20)
        result = messaging.get_conversations(limit)
        print_json(result)

    elif command == "messages":
        if len(sys.argv) < 3:
            print_json({"error": "Usage: linkedin messages <conversation_id>"})
            return
        result = messaging.get_messages(sys.argv[2])
        print_json(result)

    elif command == "send":
        if len(sys.argv) < 4:
            print_json({"error": "Usage: linkedin send <public_id> <message>"})
            return
        result = messaging.send_message(sys.argv[2], sys.argv[3])
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
    print("""LinkedIn Skill CLI - No developer app needed!

Login:
  login                             Opens browser to sign in to LinkedIn
  status                            Check login status
  logout                            Log out

Profile:
  me                                View your own profile
  profile <public_id>               View someone's profile

Search:
  search-people <keywords>          Search for people
  search-companies <keywords>       Search for companies
  search-jobs <keywords>            Search for jobs

Posts:
  post <text>                       Create a text post
  post-link <text> <url>            Post with link
  delete-post <post_urn>            Delete a post
  feed                              View your feed

Engagement:
  react <post_urn> [type]           React to a post
  comment <post_urn> <text>         Comment on a post
  get-comments <post_urn>           Get post comments

Connections:
  connect <public_id> [--message M] Send connection request
  disconnect <public_id>            Remove a connection
  invitations                       View pending invitations
  accept <id> <secret>              Accept an invitation

Messaging:
  conversations                     View recent conversations
  messages <conversation_id>        Read a conversation
  send <public_id> <message>        Send a message
""")


if __name__ == "__main__":
    main()
