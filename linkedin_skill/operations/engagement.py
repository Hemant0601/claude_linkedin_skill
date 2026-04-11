"""Engagement operations (reactions, comments, feed) for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def react_to_post(post_urn, reaction_type="LIKE"):
    """React to a post. Types: LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION."""
    try:
        client = LinkedInClient()
        result = client.react_to_post(post_urn, reaction_type)
        return {"status": "success", "message": f"Reacted with {reaction_type}.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def comment_on_post(post_urn, text):
    """Comment on a post."""
    try:
        client = LinkedInClient()
        result = client.comment_on_post(post_urn, text)
        return {"status": "success", "message": "Comment posted.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def get_comments(post_urn, count=10):
    """Get comments on a post."""
    try:
        client = LinkedInClient()
        result = client.get_post_comments(post_urn, count)
        return {"status": "success", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def get_feed(limit=10):
    """Get posts from your LinkedIn feed."""
    try:
        client = LinkedInClient()
        result = client.get_feed(limit)
        return {"status": "success", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}
