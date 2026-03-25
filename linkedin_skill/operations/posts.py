"""Post/Share operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def create_text_post(text, visibility="PUBLIC"):
    """Create a text-only LinkedIn post."""
    try:
        client = LinkedInClient()
        result = client.create_text_post(text, visibility)
        return {"status": "success", "message": "Post published successfully.", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}


def create_article_post(text, url, title=None, description=None, visibility="PUBLIC"):
    """Create a LinkedIn post with a link/article."""
    try:
        client = LinkedInClient()
        result = client.create_article_post(text, url, title, description, visibility)
        return {"status": "success", "message": "Article post published.", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}


def create_image_post(text, image_url, title=None, visibility="PUBLIC"):
    """Create a LinkedIn post with an image."""
    try:
        client = LinkedInClient()
        result = client.create_image_post(text, image_url, title, visibility)
        return {"status": "success", "message": "Image post published.", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}


def delete_post(post_urn):
    """Delete a LinkedIn post by URN."""
    try:
        client = LinkedInClient()
        result = client.delete_post(post_urn)
        return {"status": "success", "message": "Post deleted.", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}


def create_org_post(org_id, text, visibility="PUBLIC"):
    """Create a post on behalf of a LinkedIn organization page."""
    try:
        client = LinkedInClient()
        result = client.create_org_post(org_id, text, visibility)
        return {"status": "success", "message": "Organization post published.", "data": result}
    except LinkedInAPIError as e:
        return {"status": "error", "message": str(e)}
