"""Connection/Network operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def send_connection_request(public_id, message=None):
    """Send a connection request by LinkedIn public ID (the URL slug)."""
    try:
        client = LinkedInClient()
        result = client.send_connection_request(public_id, message)
        return {"status": "success", "message": f"Connection request sent to {public_id}.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def remove_connection(public_id):
    """Remove a connection."""
    try:
        client = LinkedInClient()
        result = client.remove_connection(public_id)
        return {"status": "success", "message": f"Removed connection: {public_id}.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def get_pending_invitations():
    """Get pending connection invitations."""
    try:
        client = LinkedInClient()
        result = client.get_pending_invitations()
        return {"status": "success", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def accept_invitation(invitation_id, shared_secret):
    """Accept a pending connection invitation."""
    try:
        client = LinkedInClient()
        result = client.accept_invitation(invitation_id, shared_secret)
        return {"status": "success", "message": "Invitation accepted.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}
