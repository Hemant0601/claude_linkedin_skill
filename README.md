# Claude LinkedIn Skill

A Claude Code skill to operate your LinkedIn account. No developer app, no API keys, no OAuth setup. Just log in and go.

## How to Deploy & Use with Claude Code

### Step 1: Clone and Install

```bash
git clone https://github.com/Hemant0601/claude_linkedin_skill.git
cd claude_linkedin_skill
pip install -e .
```

### Step 2: Register the Skill

Copy the skill into your Claude Code user-level skills directory:

```bash
mkdir -p ~/.claude/skills/linkedin
cp .claude/skills/linkedin/SKILL.md ~/.claude/skills/linkedin/SKILL.md
```

This makes `/linkedin` available as a slash command across all your Claude Code projects.

### Step 3: Login to LinkedIn

```bash
python -m linkedin_skill.cli login
```

Enter your LinkedIn email and password. That's it — no developer app, no API keys.

### Step 4: Use It

Open Claude Code and type `/linkedin` or just ask naturally:

- "Post about AI trends on my LinkedIn"
- "Search for ML engineers on LinkedIn"
- "Check my LinkedIn messages"
- "Connect with john-doe on LinkedIn"

Claude reads the `CLAUDE.md` file automatically and knows how to use every command.

---

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
| `linkedin react <urn> LIKE` | React to a post (LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION) |
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
| `linkedin login` | Log in with email/password |
| `linkedin status` | Check if logged in |
| `linkedin logout` | Log out |

---

## How It Works

Uses the [`linkedin-api`](https://github.com/tomquirk/linkedin-api) library which authenticates directly with LinkedIn using your email/password — the same way the LinkedIn website works. No LinkedIn Developer App or OAuth registration needed.

## How Claude Code Picks It Up

This project uses two mechanisms so Claude automatically knows how to operate LinkedIn:

1. **`CLAUDE.md`** (project root) — Claude reads this file automatically in every session. It contains the full command reference and rules (always confirm before posting, never store passwords, etc.)

2. **`.claude/skills/linkedin/SKILL.md`** — Registers `/linkedin` as a slash command. Copy this to `~/.claude/skills/linkedin/SKILL.md` to make it available globally.

## Security

- **No credentials stored in the project** — password is only used during login to get a session cookie
- **Session cookies** are cached locally by the library at `~/.linkedin_api/`
- **Claude always asks for approval** before posting, messaging, connecting, or deleting
- **`.gitignore`** prevents any secrets from being committed

## Project Structure

```
claude_linkedin_skill/
├── CLAUDE.md                          # Claude auto-reads this — command reference & rules
├── .claude/skills/linkedin/SKILL.md   # Skill definition for /linkedin slash command
├── linkedin_skill/
│   ├── cli.py                         # CLI entry point
│   ├── auth.py                        # Login/logout/status
│   ├── api.py                         # LinkedIn API client wrapper
│   ├── config.py                      # Session storage
│   └── operations/
│       ├── profile.py                 # Profile operations
│       ├── posts.py                   # Create/delete posts
│       ├── engagement.py              # React, comment, feed
│       ├── connections.py             # Connect/disconnect/invitations
│       ├── messaging.py               # Conversations & messages
│       └── search.py                  # Search people/companies/jobs
├── pyproject.toml                     # Package config
└── requirements.txt                   # linkedin-api dependency
```
