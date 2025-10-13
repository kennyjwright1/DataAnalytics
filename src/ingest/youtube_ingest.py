import os, pathlib, pandas as pd, requests

OUT = pathlib.Path("data/raw/youtube_tdlr.parquet")

def fetch_comments(video_id, api_key, max_results=100):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 100,
        "key": api_key,
        "textFormat": "plainText"
    }
    rows = []
    while True:
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        for item in data.get("items", []):
            sn = item["snippet"]["topLevelComment"]["snippet"]
            rows.append({
                "platform": "youtube",
                "kind": "comment",
                "video_id": video_id,
                "author": sn.get("authorDisplayName"),
                "created_utc": sn.get("publishedAt"),
                "title": None,
                "Description": sn.get("textDisplay"),
                "url": f"https://www.youtube.com/watch?v={video_id}&lc={item['id']}"
            })
        token = data.get("nextPageToken")
        if not token or len(rows) >= max_results:
            break
        params["pageToken"] = token
    return rows

def main():
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise SystemExit("Set YOUTUBE_API_KEY in env")
    video_ids = [
        # Add relevant video IDs here
    ]
    all_rows = []
    for vid in video_ids:
        all_rows.extend(fetch_comments(vid, api_key, max_results=200))
    if not all_rows:
        print("No YouTube rows. Add video IDs in the script.")
        return
    df = pd.DataFrame(all_rows)
    df["Program"] = "PublicDiscussion"
    df["Date"] = pd.to_datetime(df["created_utc"]).dt.date
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Wrote {OUT} ({len(df)} rows)")

if __name__ == "__main__":
    main()
