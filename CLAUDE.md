# LinkedIn Skill for Claude Code

This project provides a LinkedIn automation skill. When a user asks anything about LinkedIn, use the CLI commands below.

## Login Flow

Before any operation, check login status:
```bash
python -m linkedin_skill.cli status
```

If the command fails with a module error, install first:
```bash
pip install -e /home/user/claude_linkedin_skill
```

If not logged in, start the browser-based login:
```bash
python -m linkedin_skill.cli login
```
This opens a local web page at `http://localhost:8585` where the user signs in with their LinkedIn email/password directly in the browser. Credentials go straight to LinkedIn — never stored or logged. Once they sign in, the session is saved automatically and the CLI reports success.

## Commands

| Action | Command |
|--------|---------|
| Login (browser) | `python -m linkedin_skill.cli login` |
| Check login | `python -m linkedin_skill.cli status` |
| Logout | `python -m linkedin_skill.cli logout` |
| My profile | `python -m linkedin_skill.cli me` |
| View profile | `python -m linkedin_skill.cli profile <public_id>` |
| Search people | `python -m linkedin_skill.cli search-people "<keywords>" --limit 10` |
| Search companies | `python -m linkedin_skill.cli search-companies "<keywords>" --limit 10` |
| Search jobs | `python -m linkedin_skill.cli search-jobs "<keywords>" --limit 10` |
| Create post | `python -m linkedin_skill.cli post "<text>"` |
| Post with link | `python -m linkedin_skill.cli post-link "<text>" "<url>" --title "<title>"` |
| Delete post | `python -m linkedin_skill.cli delete-post <post_urn>` |
| View feed | `python -m linkedin_skill.cli feed --limit 10` |
| React to post | `python -m linkedin_skill.cli react <post_urn> LIKE` |
| Comment | `python -m linkedin_skill.cli comment <post_urn> "<text>"` |
| Read comments | `python -m linkedin_skill.cli get-comments <post_urn>` |
| Connect | `python -m linkedin_skill.cli connect <public_id> --message "<msg>"` |
| Disconnect | `python -m linkedin_skill.cli disconnect <public_id>` |
| Invitations | `python -m linkedin_skill.cli invitations` |
| Accept invite | `python -m linkedin_skill.cli accept <id> <secret>` |
| Conversations | `python -m linkedin_skill.cli conversations` |
| Read messages | `python -m linkedin_skill.cli messages <conversation_id>` |
| Send message | `python -m linkedin_skill.cli send <public_id> "<message>"` |

## Rules

1. **Always check login status** before running any LinkedIn operation
2. **If not logged in**, run the login command — it opens the browser, user signs in there
3. **Always confirm with the user** before: posting, sending messages, sending connection requests, deleting anything
4. **Never store or log** the user's LinkedIn password
5. **Parse JSON output** and present results in a clean, readable format
6. The `public_id` is the slug from a LinkedIn URL: `linkedin.com/in/john-doe` → `john-doe`
7. Reaction types: `LIKE`, `PRAISE`, `EMPATHY`, `INTEREST`, `APPRECIATION`
