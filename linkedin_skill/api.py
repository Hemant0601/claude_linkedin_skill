"""LinkedIn API client wrapper - uses linkedin-api (no developer app needed)."""

import json
from linkedin_api import Linkedin

from .config import load_session


class LinkedInAPIError(Exception):
    """Raised when a LinkedIn API call fails."""
    pass


def get_client():
    """Get an authenticated LinkedIn client from stored credentials.

    The linkedin-api library caches cookies in ~/.linkedin_api/
    so re-authentication is usually seamless after first login.
    """
    session = load_session()
    if not session or "username" not in session:
        raise LinkedInAPIError("Not logged in. Run: python -m linkedin_skill.cli login")

    try:
        # linkedin-api uses cookie-based auth and caches cookies automatically
        api = Linkedin(session["username"], "", refresh_cookies=False)
        return api
    except Exception:
        raise LinkedInAPIError(
            "Session expired. Please log in again: python -m linkedin_skill.cli login"
        )


class LinkedInClient:
    """High-level wrapper around linkedin-api for common operations."""

    def __init__(self):
        self.api = get_client()

    # --- Profile ---

    def get_my_profile(self):
        """Get the authenticated user's profile."""
        return self.api.get_user_profile()

    def get_profile(self, public_id):
        """Get any user's profile by their public LinkedIn ID (the URL slug)."""
        return self.api.get_profile(public_id)

    def get_profile_connections(self):
        """Get the authenticated user's connections."""
        return self.api.get_profile_connections()

    # --- Search ---

    def search_people(self, keywords=None, limit=10, **kwargs):
        """Search for people on LinkedIn."""
        return self.api.search_people(
            keywords=keywords,
            limit=limit,
            **kwargs,
        )

    def search_companies(self, keywords=None, limit=10):
        """Search for companies on LinkedIn."""
        return self.api.search_companies(keywords=keywords, limit=limit)

    def search_jobs(self, keywords=None, limit=10, **kwargs):
        """Search for jobs on LinkedIn."""
        return self.api.search_jobs(keywords=keywords, limit=limit, **kwargs)

    # --- Posts ---

    def create_post(self, text, visibility="PUBLIC"):
        """Create a text post on LinkedIn."""
        vis = visibility.upper()
        return self.api.create_post(text, visibility=vis)

    def create_post_with_link(self, text, url, title=None, visibility="PUBLIC"):
        """Create a post with a link attachment."""
        return self.api.create_post(
            text,
            visibility=visibility.upper(),
            link_url=url,
            link_title=title,
        )

    def delete_post(self, post_urn):
        """Delete a post by URN."""
        return self.api.delete_post(post_urn)

    # --- Engagement ---

    def react_to_post(self, post_urn, reaction_type="LIKE"):
        """React to a post. Types: LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION."""
        return self.api.react_post(post_urn, reaction_type)

    def comment_on_post(self, post_urn, text):
        """Add a comment to a post."""
        return self.api.comment_on_post(post_urn, text)

    def get_post_comments(self, post_urn, count=10):
        """Get comments on a post."""
        return self.api.get_post_comments(post_urn, comment_count=count)

    # --- Feed ---

    def get_feed(self, limit=10):
        """Get posts from your LinkedIn feed."""
        return self.api.get_feed_posts(limit=limit)

    # --- Connections ---

    def send_connection_request(self, public_id, message=None):
        """Send a connection request to a user by public ID."""
        return self.api.add_connection(public_id, message=message)

    def remove_connection(self, public_id):
        """Remove a connection."""
        return self.api.remove_connection(public_id)

    def get_pending_invitations(self):
        """Get pending connection invitations."""
        return self.api.get_invitations()

    def accept_invitation(self, invitation_id, shared_secret):
        """Accept a connection invitation."""
        return self.api.reply_invitation(
            invitation_entity_urn=invitation_id,
            invitation_shared_secret=shared_secret,
            action="accept",
        )

    # --- Messaging ---

    def get_conversations(self, limit=20):
        """Get recent conversations."""
        return self.api.get_conversations(limit=limit)

    def get_conversation_messages(self, conversation_id, limit=20):
        """Get messages in a conversation."""
        return self.api.get_conversation(conversation_id)

    def send_message(self, recipients, text):
        """Send a message to one or more people.

        recipients: list of public_ids (URL slugs)
        """
        if isinstance(recipients, str):
            recipients = [recipients]
        return self.api.send_message(message_body=text, recipients=recipients)

    # --- Company / Organization ---

    def get_company(self, public_id):
        """Get company details by public ID."""
        return self.api.get_company(public_id)

    def get_company_updates(self, public_id, limit=10):
        """Get recent updates from a company page."""
        return self.api.get_company_updates(public_id, max_results=limit)
