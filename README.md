# Claude LinkedIn Skill

Operate your LinkedIn from Claude Code. No developer app, no API keys. Sign in via browser and go.

## Setup

```bash
git clone https://github.com/Hemant0601/claude_linkedin_skill.git
cd claude_linkedin_skill
pip install -e .
```

### Register as a Claude Code slash command (optional)

```bash
mkdir -p ~/.claude/skills/linkedin
cp .claude/skills/linkedin/SKILL.md ~/.claude/skills/linkedin/SKILL.md
```

This makes `/linkedin` available as a slash command. Without this step, Claude still picks up the skill automatically via `CLAUDE.md`.

## Login

```bash
python -m linkedin_skill.cli login
```

A browser window opens with a LinkedIn sign-in page. Enter your credentials there — they go directly to LinkedIn, never stored or logged by this skill. Once signed in, the browser shows a success page and you're connected.

## What It Can Do

### Profile
| Command | What it does |
|---------|-------------|
| `linkedin me` | View your own profile |
| `linkedin profile <id>` | View anyone's profile by their URL slug |

### Search
| Command | What it does |
|---------|-------------|
| `linkedin search-people "<keywords>"` | Find people |
| `linkedin search-companies "<keywords>"` | Find companies |
| `linkedin search-jobs "<keywords>"` | Find job listings |

### Posts
| Command | What it does |
|---------|-------------|
| `linkedin post "<text>"` | Create a text post |
| `linkedin post-link "<text>" "<url>"` | Post with a link |
| `linkedin delete-post <urn>` | Delete a post |
| `linkedin feed` | Browse your feed |

### Engagement
| Command | What it does |
|---------|-------------|
| `linkedin react <urn> LIKE` | React (LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION) |
| `linkedin comment <urn> "<text>"` | Comment on a post |
| `linkedin get-comments <urn>` | Read comments on a post |

### Connections
| Command | What it does |
|---------|-------------|
| `linkedin connect <id>` | Send connection request |
| `linkedin connect <id> --message "Hi!"` | Connect with a message |
| `linkedin disconnect <id>` | Remove a connection |
| `linkedin invitations` | View pending invitations |
| `linkedin accept <id> <secret>` | Accept an invitation |

### Messaging
| Command | What it does |
|---------|-------------|
| `linkedin conversations` | List recent conversations |
| `linkedin messages <conversation_id>` | Read a conversation |
| `linkedin send <id> "<message>"` | Send a message |

### Session
| Command | What it does |
|---------|-------------|
| `linkedin login` | Opens browser to sign in |
| `linkedin status` | Check if logged in |
| `linkedin logout` | Log out |

## Using with Claude Code

Open Claude Code in this project directory and just ask:

- "Post about AI trends on my LinkedIn"
- "Search for ML engineers on LinkedIn"
- "Check my LinkedIn messages"
- "Connect with john-doe on LinkedIn"

Claude reads `CLAUDE.md` automatically and handles everything — checking login, opening the browser for sign-in if needed, executing commands, and asking for your approval before any visible action.

## How It Works

Uses [`linkedin-api`](https://github.com/tomquirk/linkedin-api) which authenticates with LinkedIn the same way the website does. Login happens in your browser via a local page at `http://localhost:8585`. Your credentials are sent directly to LinkedIn's servers — this skill never stores or logs them.

## Security

- **Browser-based login** — credentials entered in your browser, not in Claude
- **Credentials never stored** — only a session cookie is cached locally at `~/.linkedin_api/`
- **Claude always asks for approval** before posting, messaging, connecting, or deleting
- **`.gitignore`** prevents secrets from being committed

## Project Structure

```
claude_linkedin_skill/
├── CLAUDE.md                          # Claude auto-reads this every session
├── .claude/skills/linkedin/SKILL.md   # /linkedin slash command definition
├── linkedin_skill/
│   ├── cli.py                         # CLI entry point
│   ├── auth.py                        # Browser-based login server
│   ├── api.py                         # LinkedIn API client wrapper
│   ├── config.py                      # Session storage
│   └── operations/
│       ├── profile.py                 # Profile operations
│       ├── posts.py                   # Create/delete posts
│       ├── engagement.py              # React, comment, feed
│       ├── connections.py             # Connect/disconnect/invitations
│       ├── messaging.py               # Conversations & messages
│       └── search.py                  # Search people/companies/jobs
├── pyproject.toml
└── requirements.txt
```
