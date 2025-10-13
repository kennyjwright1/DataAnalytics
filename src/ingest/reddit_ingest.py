import os, pathlib, pandas as pd, datetime as dt
import praw

OUT = pathlib.Path("data/raw/reddit_tdlr.parquet")

def client():
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ.get("REDDIT_USER_AGENT","tdlr-sentiment/0.1")
    )

def search_terms():
    return [
        '"Texas Department of Licensing and Regulation"',
        'TDLR',
        'Texas licensing regulation'
    ]

def fetch_submissions(r, q, limit=200):
    for subm in r.subreddit('all').search(q, sort='new', limit=limit):
        yield {
            "platform":"reddit",
            "kind":"submission",
            "id": subm.id,
            "subreddit": str(subm.subreddit),
            "created_utc": dt.datetime.utcfromtimestamp(subm.created_utc).isoformat(),
            "author": str(subm.author) if subm.author else None,
            "title": subm.title,
            "body": getattr(subm, "selftext", None),
            "url": subm.url,
            "permalink": f"https://reddit.com{subm.permalink}"
        }

def fetch_comments(r, q, limit=200):
    for subm in r.subreddit('all').search(q, sort='new', limit=limit):
        subm.comments.replace_more(limit=0)
        for c in subm.comments.list():
            yield {
                "platform":"reddit",
                "kind":"comment",
                "id": c.id,
                "subreddit": str(subm.subreddit),
                "created_utc": dt.datetime.utcfromtimestamp(c.created_utc).isoformat(),
                "author": str(c.author) if c.author else None,
                "title": subm.title,
                "body": c.body,
                "url": f"https://reddit.com{c.permalink}",
                "parent_submission": subm.id
            }

def main():
    r = client()
    rows = []
    for q in search_terms():
        rows.extend(list(fetch_submissions(r, q, limit=100)))
        rows.extend(list(fetch_comments(r, q, limit=25)))
    if not rows:
        print("No Reddit rows found")
        return
    df = pd.DataFrame(rows)
    df.rename(columns={"body":"Description"}, inplace=True)
    df["Program"] = "PublicDiscussion"
    df["Date"] = pd.to_datetime(df["created_utc"]).dt.date
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Wrote {OUT} ({len(df)} rows)")

if __name__ == "__main__":
    main()
