# Supplementary Sources Add-on

This pack adds **compliant optional sources** to your `tdlr-sentiment` repo:
- **Reddit** (official API + PRAW) — fetch posts & comments mentioning TDLR.
- **GDELT 2.0 (news)** — fetch Global Knowledge Graph rows and titles mentioning TDLR; includes built-in TONE.
- **YouTube** (official Data API) — fetch comments for chosen videos (e.g., hearings, news segments).

> ⚖️ Always follow each platform’s Terms. Store API keys as GitHub Actions secrets or a local `.env` and **do not commit raw personal data**.
> These scripts save small text fields for NLP. Consider pushing only **aggregations** to your repo.

## Environment
Create a `.env` with any of the variables you intend to use:
```
# Reddit
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=tdlr-sentiment/0.1 by <yourname>

# YouTube
YOUTUBE_API_KEY=

# GDELT requires no key (public CSV endpoints)
```
