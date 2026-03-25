---
name: linkedin
description: Operate your LinkedIn account - post, message, search, connect. No API keys needed.
user-invocable: true
---

# LinkedIn Skill

Operate your LinkedIn account directly from Claude Code. No developer app, no API keys, no OAuth setup. Just log in and go.

## How It Works

Uses the `linkedin-api` library which authenticates directly with LinkedIn using your email/password — the same way the LinkedIn website does.

## First-Time Setup

1. **Install**: `pip install -e .` (from the project root)
2. **Login**: `python -m linkedin_skill.cli login` (enter your LinkedIn email and password)
3. **Check status**: `python -m linkedin_skill.cli status`

## Instructions for Claude

When the user invokes `/linkedin` or asks to operate LinkedIn:

1. **Always check login first**: `python -m linkedin_skill.cli status`
2. **If not logged in**: Tell the user to run `python -m linkedin_skill.cli login`
3. **Execute the requested operation** using the CLI commands below
4. **Always confirm with the user before**: posting, sending messages, sending connection requests, or deleting anything
5. **Parse JSON output** and present results in a clean, readable format

## Commands

### Login / Session
```bash
python -m linkedin_skill.cli login                    # Log in (prompts for email/password)
python -m linkedin_skill.cli status                   # Check if logged in
python -m linkedin_skill.cli logout                   # Log out
```

### Profile
```bash
python -m linkedin_skill.cli me                       # Your profile
python -m linkedin_skill.cli profile john-doe          # View anyone's profile by public ID
```

The `public_id` is the slug from someone's LinkedIn URL: `linkedin.com/in/john-doe` → `john-doe`

### Search
```bash
python -m linkedin_skill.cli search-people "machine learning engineer" --limit 5
python -m linkedin_skill.cli search-companies "artificial intelligence" --limit 5
python -m linkedin_skill.cli search-jobs "python developer" --limit 10
```

### Posts
```bash
python -m linkedin_skill.cli post "Your post text here"
python -m linkedin_skill.cli post "Check this out" --visibility CONNECTIONS
python -m linkedin_skill.cli post-link "Great read!" "https://example.com" --title "Article"
python -m linkedin_skill.cli delete-post <post_urn>
```

### Feed
```bash
python -m linkedin_skill.cli feed                     # View your feed
python -m linkedin_skill.cli feed --limit 5           # Limit results
```

### Engagement
```bash
python -m linkedin_skill.cli react <post_urn> LIKE
python -m linkedin_skill.cli react <post_urn> PRAISE
python -m linkedin_skill.cli comment <post_urn> "Great insight!"
python -m linkedin_skill.cli get-comments <post_urn>
```

Reaction types: `LIKE`, `PRAISE`, `EMPATHY`, `INTEREST`, `APPRECIATION`

### Connections
```bash
python -m linkedin_skill.cli connect john-doe
python -m linkedin_skill.cli connect john-doe --message "Hi, love your work!"
python -m linkedin_skill.cli disconnect john-doe
python -m linkedin_skill.cli invitations              # View pending invites
python -m linkedin_skill.cli accept <id> <secret>     # Accept an invite
```

### Messaging
```bash
python -m linkedin_skill.cli conversations            # List recent conversations
python -m linkedin_skill.cli messages <conversation_id>  # Read messages
python -m linkedin_skill.cli send john-doe "Hey, how are you?"
```

## Example Flows

**"Post about AI trends"** → check status → draft post → show user for approval → `cli post "text"` → report

**"Find ML engineers"** → check status → `cli search-people "ML engineer"` → show results → ask who to connect with → `cli connect <id>`

**"Check my messages"** → check status → `cli conversations` → display → if user picks one → `cli messages <id>`

## Security

- Session cookies cached at `~/.linkedin_api/` by the library
- Password is never stored — only used during login
- Always ask user for confirmation before visible actions
