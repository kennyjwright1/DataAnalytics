import io, pandas as pd, requests, pathlib

QUERY = '"Texas Department of Licensing and Regulation" OR TDLR'
OUT = pathlib.Path("data/raw/gdelt_gkg_tdlr.parquet")

def fetch_gkg():
    params = {
        "query": QUERY,
        "format": "CSV",
        "mode": "ArtList",
        "maxrecords": 250
    }
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

def main():
    df = fetch_gkg()
    if df.empty:
        print("No GDELT rows returned")
        return
    df = df.rename(columns={"title":"Description", "seendate":"Date"})
    df["Program"] = "News"
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Wrote {OUT} ({len(df)} rows)")

if __name__ == "__main__":
    main()
