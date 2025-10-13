import pathlib, pandas as pd
INP = pathlib.Path("data/processed/tdlr_scored.parquet")
OUTDIR = pathlib.Path("data/processed/exports")

def main():
    if not INP.exists():
        raise SystemExit("Run azure_sentiment.py first.")
    df = pd.read_parquet(INP)
    df["month"] = pd.to_datetime(df.get("Date"), errors="coerce").dt.to_period("M").dt.to_timestamp()
    by_month = (df.groupby(["Program","month"], dropna=False)
                  .agg(pos=("pos","mean"), neu=("neu","mean"),
                       neg=("neg","mean"), count=("Description","count"))
                  .reset_index())
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR/"program_month_sentiment.csv"
    by_month.to_csv(out, index=False)
    print(f"Wrote {out} with {len(by_month)} rows")

if __name__ == "__main__":
    main()
