---
name: linkedin
description: Operate your LinkedIn account - post, message, search, connect. No API keys needed.
user-invocable: true
---

# LinkedIn Skill

Operate your LinkedIn account directly from Claude Code. No developer app, no API keys. Sign in via browser and go.

## Login Flow

1. Run `python -m linkedin_skill.cli login`
2. This opens `http://localhost:8585` in the user's browser with a LinkedIn sign-in form
3. User enters their email/password in the browser (credentials go directly to LinkedIn, never stored)
4. On success, session is saved and the CLI prints a success message
5. All subsequent commands use the cached session

## Instructions for Claude

1. **Always check login first**: `python -m linkedin_skill.cli status`
2. **If not logged in**: Run `python -m linkedin_skill.cli login` — tell the user a browser window will open for them to sign in
3. **Execute the requested operation** using the CLI commands below
4. **Always confirm with the user before**: posting, sending messages, sending connection requests, or deleting anything
5. **Parse JSON output** and present results in a clean, readable format

## Commands

```bash
# Login
python -m linkedin_skill.cli login                    # Opens browser to sign in
python -m linkedin_skill.cli status                   # Check if logged in
python -m linkedin_skill.cli logout                   # Log out

# Profile
python -m linkedin_skill.cli me                       # Your profile
python -m linkedin_skill.cli profile john-doe          # View anyone's profile

# Search
python -m linkedin_skill.cli search-people "ML engineer" --limit 5
python -m linkedin_skill.cli search-companies "AI startup" --limit 5
python -m linkedin_skill.cli search-jobs "python developer" --limit 10

# Posts
python -m linkedin_skill.cli post "Your post text here"
python -m linkedin_skill.cli post-link "Check this!" "https://example.com" --title "Title"
python -m linkedin_skill.cli delete-post <post_urn>

# Feed & Engagement
python -m linkedin_skill.cli feed --limit 5
python -m linkedin_skill.cli react <post_urn> LIKE
python -m linkedin_skill.cli comment <post_urn> "Great insight!"
python -m linkedin_skill.cli get-comments <post_urn>

# Connections
python -m linkedin_skill.cli connect john-doe --message "Hi!"
python -m linkedin_skill.cli disconnect john-doe
python -m linkedin_skill.cli invitations
python -m linkedin_skill.cli accept <id> <secret>

# Messaging
python -m linkedin_skill.cli conversations
python -m linkedin_skill.cli messages <conversation_id>
python -m linkedin_skill.cli send john-doe "Hey, how are you?"
```

Reaction types: `LIKE`, `PRAISE`, `EMPATHY`, `INTEREST`, `APPRECIATION`

The `public_id` is the slug from a LinkedIn URL: `linkedin.com/in/john-doe` → `john-doe`
