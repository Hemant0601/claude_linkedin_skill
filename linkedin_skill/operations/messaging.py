"""Messaging operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def get_conversations(limit=20):
    """Get recent LinkedIn conversations."""
    try:
        client = LinkedInClient()
        result = client.get_conversations(limit)
        return {"status": "success", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def get_messages(conversation_id, limit=20):
    """Get messages in a conversation."""
    try:
        client = LinkedInClient()
        result = client.get_conversation_messages(conversation_id, limit)
        return {"status": "success", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def send_message(recipients, text):
    """Send a message to one or more LinkedIn users.

    recipients: LinkedIn public ID(s) — the slug from their profile URL.
    """
    try:
        client = LinkedInClient()
        result = client.send_message(recipients, text)
        return {"status": "success", "message": "Message sent.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}
