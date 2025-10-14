import pathlib, pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

INP = pathlib.Path("data/interim/tdlr_clean.parquet")
OUT = pathlib.Path("data/processed/tdlr_scored.parquet")

def main():
    if not INP.exists():
        raise SystemExit("Run clean_normalize.py first.")
    df = pd.read_parquet(INP)
    sid = SentimentIntensityAnalyzer()
    s = df["Description"].astype(str).apply(sid.polarity_scores)
    df["pos"] = s.map(lambda x: x["pos"])
    df["neu"] = s.map(lambda x: x["neu"])
    df["neg"] = s.map(lambda x: x["neg"])
    df["sentiment"] = s.map(lambda x: "positive" if x["compound"] > 0.05
                            else "negative" if x["compound"] < -0.05 else "neutral")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Wrote {OUT} with {len(df)} rows")

if __name__ == "__main__":
    main()
