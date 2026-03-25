# LinkedIn Skill

Operate your LinkedIn account directly from Claude Code. No developer app, no API keys, no OAuth setup. Just log in and go.

## How It Works

This skill uses the `linkedin-api` library which authenticates directly with LinkedIn using your email/password — the same way the LinkedIn website does. No LinkedIn Developer App needed.

## First-Time Setup

1. **Install**: `pip install -e .` (from the project root)
2. **Login**: `python -m linkedin_skill.cli login`
   - Enter your LinkedIn email and password when prompted
   - That's it. You're connected.
3. **Check status**: `python -m linkedin_skill.cli status`

## Auto Mode Instructions

When the user wants to operate LinkedIn, Claude should:

1. **Always check login first**: `python -m linkedin_skill.cli status`
2. **If not logged in**: Tell the user to run `python -m linkedin_skill.cli login` and enter their credentials
3. **Execute the requested operation** using the CLI commands below
4. **Always confirm with the user before**: posting, sending messages, sending connection requests, or deleting anything
5. **Parse JSON output** and present results in a clean, readable format

## Commands Reference

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

## Example Auto Mode Flows

**User: "Post about AI trends on my LinkedIn"**
1. Run `status` to check login
2. Draft a professional post about AI trends
3. Show the draft to the user and ask for approval
4. On approval: `python -m linkedin_skill.cli post "drafted text"`
5. Report success

**User: "Find ML engineers and connect with them"**
1. Run `status` to check login
2. `python -m linkedin_skill.cli search-people "machine learning engineer" --limit 10`
3. Show results to user
4. Ask which ones to connect with
5. For each approved: `python -m linkedin_skill.cli connect <public_id> --message "personalized message"`

**User: "Check my messages"**
1. Run `status` to check login
2. `python -m linkedin_skill.cli conversations`
3. Display conversations in readable format
4. If user wants to read one: `python -m linkedin_skill.cli messages <id>`

**User: "Engage with my feed"**
1. Run `status` to check login
2. `python -m linkedin_skill.cli feed --limit 5`
3. Show feed posts to user
4. Ask which to engage with
5. React/comment as requested

## Security Notes

- Credentials are handled by the `linkedin-api` library which caches session cookies at `~/.linkedin_api/`
- Session info stored at `~/.config/claude-linkedin-skill/session.json` (owner-only permissions)
- Password is never stored — only used during login to establish a session
- Always ask user for confirmation before taking actions that are visible to others
