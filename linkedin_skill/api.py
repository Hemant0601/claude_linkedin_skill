"""LinkedIn API client wrapper."""

import json
import requests

from .config import get_access_token

BASE_URL = "https://api.linkedin.com/v2"
REST_BASE_URL = "https://api.linkedin.com/rest"


class LinkedInAPIError(Exception):
    """Raised when a LinkedIn API call fails."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(f"LinkedIn API error ({status_code}): {message}")


class LinkedInClient:
    """Client for LinkedIn API operations."""

    def __init__(self, access_token=None):
        self.access_token = access_token or get_access_token()
        if not self.access_token:
            raise LinkedInAPIError(401, "Not authenticated. Run `linkedin auth` first.")

    def _headers(self, version="202401"):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        if version:
            headers["LinkedIn-Version"] = version
        return headers

    def _get(self, url, params=None, use_rest=False):
        base = REST_BASE_URL if use_rest else BASE_URL
        full_url = f"{base}{url}" if url.startswith("/") else url
        resp = requests.get(full_url, headers=self._headers(), params=params)
        if resp.status_code != 200:
            raise LinkedInAPIError(resp.status_code, resp.text)
        return resp.json()

    def _post(self, url, data, use_rest=False):
        base = REST_BASE_URL if use_rest else BASE_URL
        full_url = f"{base}{url}" if url.startswith("/") else url
        resp = requests.post(full_url, headers=self._headers(), json=data)
        if resp.status_code not in (200, 201):
            raise LinkedInAPIError(resp.status_code, resp.text)
        return resp.json() if resp.text else {"status": "success"}

    def _delete(self, url, use_rest=False):
        base = REST_BASE_URL if use_rest else BASE_URL
        full_url = f"{base}{url}" if url.startswith("/") else url
        resp = requests.delete(full_url, headers=self._headers())
        if resp.status_code not in (200, 204):
            raise LinkedInAPIError(resp.status_code, resp.text)
        return {"status": "deleted"}

    # --- Profile ---

    def get_my_profile(self):
        """Get the authenticated user's profile via OpenID userinfo."""
        resp = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers=self._headers(version=None),
        )
        if resp.status_code != 200:
            raise LinkedInAPIError(resp.status_code, resp.text)
        return resp.json()

    def get_person_urn(self):
        """Get the authenticated user's person URN (sub claim)."""
        profile = self.get_my_profile()
        return profile.get("sub")

    # --- Posts / Shares ---

    def create_text_post(self, text, visibility="PUBLIC"):
        """Create a text-only post on LinkedIn."""
        person_urn = self.get_person_urn()
        payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }
        return self._post("/ugcPosts", payload)

    def create_article_post(self, text, article_url, title=None, description=None, visibility="PUBLIC"):
        """Create a post with an article/link attachment."""
        person_urn = self.get_person_urn()
        media = {
            "status": "READY",
            "originalUrl": article_url,
        }
        if title:
            media["title"] = {"text": title}
        if description:
            media["description"] = {"text": description}

        payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [media],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }
        return self._post("/ugcPosts", payload)

    def delete_post(self, post_urn):
        """Delete a post by its URN."""
        encoded = post_urn.replace(":", "%3A")
        return self._delete(f"/ugcPosts/{encoded}")

    # --- Reactions ---

    def react_to_post(self, post_urn, reaction_type="LIKE"):
        """React to a post. Types: LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION."""
        person_urn = self.get_person_urn()
        payload = {
            "root": post_urn,
            "reactionType": reaction_type,
        }
        encoded_actor = f"urn%3Ali%3Aperson%3A{person_urn}"
        return self._post(f"/reactions?actor={encoded_actor}", payload)

    # --- Comments ---

    def comment_on_post(self, post_urn, text):
        """Add a comment to a post."""
        person_urn = self.get_person_urn()
        payload = {
            "actor": f"urn:li:person:{person_urn}",
            "message": {"text": text},
        }
        encoded_urn = post_urn.replace(":", "%3A")
        return self._post(f"/socialActions/{encoded_urn}/comments", payload)

    def get_post_comments(self, post_urn, count=10):
        """Get comments on a post."""
        encoded_urn = post_urn.replace(":", "%3A")
        return self._get(f"/socialActions/{encoded_urn}/comments", params={"count": count})

    # --- Network / Connections ---

    def get_connections_count(self):
        """Get the number of first-degree connections."""
        return self._get("/connections?q=viewer&start=0&count=0")

    def send_invitation(self, profile_urn, message=None):
        """Send a connection invitation.

        profile_urn: The target person's URN (e.g., 'urn:li:person:ABC123')
        """
        payload = {
            "invitee": profile_urn,
            "message": {"text": message} if message else None,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._post("/invitations", payload)

    # --- Organization Pages ---

    def get_organization(self, org_id):
        """Get organization details by ID."""
        return self._get(f"/organizations/{org_id}")

    def create_org_post(self, org_id, text, visibility="PUBLIC"):
        """Create a post on behalf of an organization page."""
        payload = {
            "author": f"urn:li:organization:{org_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }
        return self._post("/ugcPosts", payload)

    # --- Analytics ---

    def get_post_analytics(self, post_urn):
        """Get share statistics for a post."""
        encoded = post_urn.replace(":", "%3A")
        return self._get(f"/socialActions/{encoded}")

    # --- Image Post ---

    def create_image_post(self, text, image_url, title=None, visibility="PUBLIC"):
        """Create a post with an image URL.

        Note: For native image uploads, LinkedIn requires a multi-step process
        (register upload -> upload binary -> create post). This simplified method
        uses an image URL instead.
        """
        person_urn = self.get_person_urn()
        media = {
            "status": "READY",
            "originalUrl": image_url,
        }
        if title:
            media["title"] = {"text": title}

        payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "IMAGE",
                    "media": [media],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }
        return self._post("/ugcPosts", payload)
