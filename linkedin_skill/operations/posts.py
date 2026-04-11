"""Post operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def create_text_post(text, visibility="PUBLIC"):
    """Create a text post on LinkedIn."""
    try:
        client = LinkedInClient()
        result = client.create_post(text, visibility)
        return {"status": "success", "message": "Post published!", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def create_link_post(text, url, title=None, visibility="PUBLIC"):
    """Create a post with a link attachment."""
    try:
        client = LinkedInClient()
        result = client.create_post_with_link(text, url, title, visibility)
        return {"status": "success", "message": "Post with link published!", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def delete_post(post_urn):
    """Delete a post by URN."""
    try:
        client = LinkedInClient()
        result = client.delete_post(post_urn)
        return {"status": "success", "message": "Post deleted.", "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}
