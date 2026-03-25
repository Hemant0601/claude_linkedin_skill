# LinkedIn Skill

Automate your LinkedIn account directly from Claude Code. This skill lets you authenticate with your own LinkedIn account and perform operations like posting, engaging, and managing connections — all in auto mode.

## Setup (One-Time)

Before using this skill, the user must:

1. **Create a LinkedIn App** at https://www.linkedin.com/developers/apps
   - Sign in with their LinkedIn account
   - Click "Create App" and fill in app details
   - Under the **Auth** tab, add `http://localhost:8585/callback` as a redirect URL
   - Under the **Products** tab, request access to:
     - "Share on LinkedIn" (for posting)
     - "Sign In with LinkedIn using OpenID Connect" (for auth)
   - Note the **Client ID** and **Client Secret**

2. **Configure credentials** — create a `.env` file in this project root:
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_REDIRECT_URI=http://localhost:8585/callback
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

## Authentication

Run the auth flow to connect:
```bash
python -m linkedin_skill.cli auth
```
This opens a local callback server and provides a URL. The user opens the URL in their browser, authorizes the app, and the token is saved locally at `~/.config/claude-linkedin-skill/tokens.json`.

To check status: `python -m linkedin_skill.cli auth-status`
To disconnect: `python -m linkedin_skill.cli logout`

## Available Operations

### Profile
```bash
python -m linkedin_skill.cli profile
```
Returns: name, email, profile picture URL.

### Create Posts
```bash
# Text post
python -m linkedin_skill.cli post "Your post text here"

# Post with article/link
python -m linkedin_skill.cli post-article "Check this out!" "https://example.com" --title "Article Title"

# Post with image URL
python -m linkedin_skill.cli post-image "Look at this!" "https://example.com/image.jpg"

# Post as an organization page (requires admin access)
python -m linkedin_skill.cli org-post <org_id> "Post text"

# Delete a post
python -m linkedin_skill.cli delete-post <post_urn>
```

Visibility options: `PUBLIC` (default) or `CONNECTIONS` (connections only).
Use `--visibility CONNECTIONS` to limit visibility.

### Engagement
```bash
# React to a post (LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION)
python -m linkedin_skill.cli react <post_urn> LIKE

# Comment on a post
python -m linkedin_skill.cli comment <post_urn> "Great insight!"

# Get comments on a post
python -m linkedin_skill.cli get-comments <post_urn>

# Get post analytics
python -m linkedin_skill.cli analytics <post_urn>
```

### Connections / Network
```bash
# Send a connection request
python -m linkedin_skill.cli connect <profile_urn>

# Send with personalized message
python -m linkedin_skill.cli connect <profile_urn> --message "Hi, let's connect!"

# Get connection count
python -m linkedin_skill.cli connections-count
```

## Auto Mode Usage

When the user says "auto mode" or asks to automate LinkedIn tasks, Claude should:

1. **Check auth**: Run `python -m linkedin_skill.cli auth-status` first
2. **If not authenticated**: Guide the user through the auth flow
3. **Execute operations**: Use the CLI commands above based on what the user wants
4. **Report results**: Parse the JSON output and present it clearly

### Example Auto Mode Flows

**"Post something about AI on LinkedIn":**
1. Check auth status
2. Draft a professional post about AI
3. Confirm with user before posting
4. Execute: `python -m linkedin_skill.cli post "drafted text"`
5. Report success

**"Engage with this post":**
1. Check auth status
2. React: `python -m linkedin_skill.cli react <urn> LIKE`
3. Comment: `python -m linkedin_skill.cli comment <urn> "thoughtful comment"`
4. Report success

**"Check my profile":**
1. Run `python -m linkedin_skill.cli profile`
2. Display formatted profile info

## Programmatic Usage (Python)

The skill can also be used directly in Python:

```python
from linkedin_skill.auth import check_auth_status, start_auth_flow
from linkedin_skill.operations.profile import get_profile
from linkedin_skill.operations.posts import create_text_post
from linkedin_skill.operations.engagement import react_to_post, comment_on_post
from linkedin_skill.operations.connections import send_connection_request

# Check auth
status = check_auth_status()

# Get profile
profile = get_profile()

# Create a post
result = create_text_post("Hello LinkedIn from Claude Code!")

# React to a post
react_to_post("urn:li:ugcPost:123456", "LIKE")

# Comment
comment_on_post("urn:li:ugcPost:123456", "Great post!")

# Connect with someone
send_connection_request("urn:li:person:ABC123", message="Let's connect!")
```

## Security Notes

- Tokens are stored locally at `~/.config/claude-linkedin-skill/tokens.json` with `600` permissions (owner-only read/write)
- The `.env` file containing client secrets is `.gitignore`d
- Each user authenticates with their own LinkedIn account — no shared credentials
- Always confirm with the user before posting or sending connection requests
