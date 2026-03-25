"""Profile operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def get_my_profile():
    """Get the logged-in user's profile."""
    try:
        client = LinkedInClient()
        profile = client.get_my_profile()
        return {
            "status": "success",
            "profile": {
                "name": f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip(),
                "headline": profile.get("headline", ""),
                "location": profile.get("locationName", ""),
                "industry": profile.get("industryName", ""),
                "summary": profile.get("summary", ""),
            },
        }
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def view_profile(public_id):
    """View any user's profile by their LinkedIn public ID (URL slug)."""
    try:
        client = LinkedInClient()
        profile = client.get_profile(public_id)
        return {
            "status": "success",
            "profile": {
                "name": f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip(),
                "headline": profile.get("headline", ""),
                "location": profile.get("locationName", ""),
                "industry": profile.get("industryName", ""),
                "summary": profile.get("summary", ""),
                "public_id": profile.get("public_id", public_id),
            },
        }
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}
