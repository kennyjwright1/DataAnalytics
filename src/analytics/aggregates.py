"""
Create monthly aggregates for visualization/BI.

Input:
  data/processed/tdlr_scored.parquet

Outputs:
  data/processed/exports/program_month_sentiment.csv
"""
import pathlib
import pandas as pd

INP = pathlib.Path("data/processed/tdlr_scored.parquet")
OUTDIR = pathlib.Path("data/processed/exports")

def main():
    if not INP.exists():
        raise SystemExit("Missing scored parquet. Run azure_sentiment.py first.")
    df = pd.read_parquet(INP)
    if "Date" not in df.columns:
        df["Date"] = pd.NaT
    df["month"] = pd.to_datetime(df["Date"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    by_month = (df
                .groupby(["Program","month"], dropna=False)
                .agg(pos=("pos","mean"),
                     neu=("neu","mean"),
                     neg=("neg","mean"),
                     count=("Description","count"))
                .reset_index()
                .sort_values(["Program","month"]))

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out_csv = OUTDIR / "program_month_sentiment.csv"
    by_month.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} with {len(by_month):,} rows")

if __name__ == "__main__":
    main()
