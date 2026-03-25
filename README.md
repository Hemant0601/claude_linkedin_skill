# Claude LinkedIn Skill

A Claude Code skill to interact with your LinkedIn account. Authenticate with your own LinkedIn and operate it in auto mode — post updates, engage with content, manage connections, and more.

## Quick Start

### 1. Create a LinkedIn Developer App

Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps) and create an app:
- Add `http://localhost:8585/callback` as an OAuth 2.0 redirect URL
- Request access to **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your Client ID and Client Secret
```

### 3. Install

```bash
pip install -e .
```

### 4. Authenticate

```bash
python -m linkedin_skill.cli auth
```

Open the displayed URL in your browser, authorize the app, and you're connected.

### 5. Use

```bash
# View your profile
python -m linkedin_skill.cli profile

# Create a post
python -m linkedin_skill.cli post "Hello LinkedIn!"

# Post with a link
python -m linkedin_skill.cli post-article "Check this out" "https://example.com"

# React to a post
python -m linkedin_skill.cli react urn:li:ugcPost:123456 LIKE

# Comment on a post
python -m linkedin_skill.cli comment urn:li:ugcPost:123456 "Great insight!"

# Send a connection request
python -m linkedin_skill.cli connect urn:li:person:ABC123 --message "Let's connect!"
```

## Using with Claude Code

This project includes a Claude Code skill at `.claude/skills/linkedin.md`. When using Claude Code in this repository, Claude can automatically:

- Check your auth status and guide you through setup
- Draft and publish LinkedIn posts
- Engage with posts (like, comment)
- Send connection requests
- View your profile and analytics

Just ask Claude things like:
- "Post about the latest trends in AI on LinkedIn"
- "Check my LinkedIn profile"
- "React to this LinkedIn post"

## Commands Reference

| Command | Description |
|---------|-------------|
| `auth` | Start OAuth authentication flow |
| `auth-status` | Check if authenticated |
| `logout` | Clear stored tokens |
| `profile` | View your profile |
| `post <text>` | Create a text post |
| `post-article <text> <url>` | Post with link |
| `post-image <text> <image_url>` | Post with image |
| `delete-post <urn>` | Delete a post |
| `org-post <org_id> <text>` | Post as organization |
| `react <urn> [type]` | React to a post |
| `comment <urn> <text>` | Comment on a post |
| `get-comments <urn>` | View post comments |
| `analytics <urn>` | View post engagement |
| `connect <urn> [--message M]` | Send connection request |
| `connections-count` | Get connection count |

## Security

- Tokens stored locally at `~/.config/claude-linkedin-skill/tokens.json` (owner-only permissions)
- `.env` file is gitignored — your secrets stay local
- Each user authenticates independently with their own LinkedIn account
