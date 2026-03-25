"""Profile operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def get_profile():
    """Fetch and format the authenticated user's LinkedIn profile."""
    try:
        client = LinkedInClient()
        profile = client.get_my_profile()
        return {
            "status": "success",
            "profile": {
                "name": profile.get("name", "N/A"),
                "email": profile.get("email", "N/A"),
                "picture": profile.get("picture", "N/A"),
                "sub": profile.get("sub", "N/A"),
            },
        }
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}
