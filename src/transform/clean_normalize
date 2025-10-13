# src/transform/clean_normalize.py
# Combines any data/raw/*.parquet into data/interim/tdlr_clean.parquet

import pathlib, pandas as pd

RAW = pathlib.Path("data/raw")
OUT = pathlib.Path("data/interim/tdlr_clean.parquet")
MIN_TEXT_LEN = 15

def main():
    files = sorted(RAW.glob("*.parquet"))
    if not files:
        raise SystemExit("No raw parquet files in data/raw/. Run an ingest step first.")

    df = pd.concat([pd.read_parquet(p) for p in files], ignore_index=True)
    df = df.rename(columns={c: c.strip().title() for c in df.columns})

    # Build Description if needed
    if "Description" not in df.columns:
        if "Body" in df.columns and "Title" in df.columns:
            df["Description"] = (df["Title"].fillna("").astype(str) + " " +
                                 df["Body"].fillna("").astype(str)).str.strip()
        elif "Body" in df.columns:
            df["Description"] = df["Body"].astype(str)
        elif "Title" in df.columns:
            df["Description"] = df["Title"].astype(str)
        else:
            raise SystemExit("No Description/Title/Body column to score.")

    if "Program" not in df.columns:
        df["Program"] = "Unknown"
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Description"] = df["Description"].astype(str).str.strip()
    df = df[df["Description"].str.len() >= MIN_TEXT_LEN].drop_duplicates()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Wrote {OUT} with {len(df)} rows")

if __name__ == "__main__":
    main()
