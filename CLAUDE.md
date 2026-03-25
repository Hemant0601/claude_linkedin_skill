# Claude Code Project Instructions

## LinkedIn Skill

This project is a LinkedIn automation skill. Use the skill defined at `.claude/skills/linkedin.md` to operate the user's LinkedIn account.

### Quick Reference

Before any LinkedIn operation, always check login status first:
```bash
python -m linkedin_skill.cli status
```

If not logged in, tell the user to run:
```bash
python -m linkedin_skill.cli login
```

### Available Commands
```bash
python -m linkedin_skill.cli login              # Log in
python -m linkedin_skill.cli status             # Check login
python -m linkedin_skill.cli me                 # My profile
python -m linkedin_skill.cli profile <id>       # View a profile
python -m linkedin_skill.cli search-people <q>  # Search people
python -m linkedin_skill.cli search-jobs <q>    # Search jobs
python -m linkedin_skill.cli post "<text>"      # Create post
python -m linkedin_skill.cli feed               # View feed
python -m linkedin_skill.cli react <urn> LIKE   # React to post
python -m linkedin_skill.cli comment <urn> "x"  # Comment
python -m linkedin_skill.cli connect <id>       # Connect
python -m linkedin_skill.cli send <id> "msg"    # Send message
python -m linkedin_skill.cli conversations      # View messages
```

### Rules
- **Always confirm with the user** before posting, messaging, connecting, or deleting
- Never store or log the user's LinkedIn password
- Parse JSON output from CLI and present it in a clean, readable format
