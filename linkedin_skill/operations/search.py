"""Search operations for LinkedIn skill."""

from ..api import LinkedInClient, LinkedInAPIError


def search_people(keywords, limit=10, **kwargs):
    """Search for people on LinkedIn."""
    try:
        client = LinkedInClient()
        result = client.search_people(keywords=keywords, limit=limit, **kwargs)
        return {"status": "success", "count": len(result), "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def search_companies(keywords, limit=10):
    """Search for companies on LinkedIn."""
    try:
        client = LinkedInClient()
        result = client.search_companies(keywords=keywords, limit=limit)
        return {"status": "success", "count": len(result), "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}


def search_jobs(keywords, limit=10, **kwargs):
    """Search for jobs on LinkedIn."""
    try:
        client = LinkedInClient()
        result = client.search_jobs(keywords=keywords, limit=limit, **kwargs)
        return {"status": "success", "count": len(result), "data": result}
    except (LinkedInAPIError, Exception) as e:
        return {"status": "error", "message": str(e)}
