# Claude LinkedIn Skill

A Claude Code skill to operate your LinkedIn account. No developer app, no API keys, no OAuth setup. Just log in and go.

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Log in with your LinkedIn account
python -m linkedin_skill.cli login

# 3. Done! Start using it.
python -m linkedin_skill.cli me              # View your profile
python -m linkedin_skill.cli post "Hello!"   # Create a post
python -m linkedin_skill.cli feed            # View your feed
```

## What Can It Do?

| Feature | Command | Example |
|---------|---------|---------|
| **Login** | `login` | `linkedin login` |
| **Your Profile** | `me` | `linkedin me` |
| **View Profile** | `profile <id>` | `linkedin profile john-doe` |
| **Search People** | `search-people <q>` | `linkedin search-people "ML engineer"` |
| **Search Companies** | `search-companies <q>` | `linkedin search-companies "AI startup"` |
| **Search Jobs** | `search-jobs <q>` | `linkedin search-jobs "python developer"` |
| **Create Post** | `post <text>` | `linkedin post "Hello LinkedIn!"` |
| **Post with Link** | `post-link <text> <url>` | `linkedin post-link "Read this" "https://..."` |
| **View Feed** | `feed` | `linkedin feed --limit 5` |
| **React** | `react <urn> [type]` | `linkedin react <urn> LIKE` |
| **Comment** | `comment <urn> <text>` | `linkedin comment <urn> "Great!"` |
| **Connect** | `connect <id>` | `linkedin connect john-doe --message "Hi!"` |
| **Message** | `send <id> <text>` | `linkedin send john-doe "Hey!"` |
| **Conversations** | `conversations` | `linkedin conversations` |
| **Invitations** | `invitations` | `linkedin invitations` |

## Using with Claude Code

This repo includes a Claude Code skill (`.claude/skills/linkedin.md`). When using Claude Code here, just say things like:

- "Log me in to LinkedIn"
- "Post about AI trends on my LinkedIn"
- "Find ML engineers and connect with them"
- "Check my LinkedIn messages"
- "React to posts in my feed"

Claude handles everything — checking login, executing commands, and asking for your approval before any visible action.

## How It Works

Uses the [`linkedin-api`](https://github.com/tomquirk/linkedin-api) library which authenticates directly with LinkedIn using your email/password — the same way the LinkedIn website works. No LinkedIn Developer App, no OAuth app registration, no API keys needed.

## Security

- Password is only used during login to establish a session cookie
- Session cookies are cached by the library at `~/.linkedin_api/`
- No credentials are stored in the project or committed to git
- All actions that are visible to others (posts, messages, connections) require your explicit approval when used through Claude
