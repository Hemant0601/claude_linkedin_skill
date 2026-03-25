"""Connection/Network operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def send_connection_request(profile_urn, message=None):
    """Send a connection invitation to a LinkedIn user.

    profile_urn: e.g. 'urn:li:person:ABC123'
    message: Optional personalized message
    """
    try:
        client = LinkedInClient()
        result = client.send_invitation(profile_urn, message)
        return {"status": "success", "message": "Connection request sent.", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}


def get_connections_count():
    """Get the authenticated user's connection count."""
    try:
        client = LinkedInClient()
        result = client.get_connections_count()
        return {"status": "success", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}
