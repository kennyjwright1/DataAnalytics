import os, pathlib, pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

INP = pathlib.Path("data/interim/tdlr_clean.parquet")
OUT = pathlib.Path("data/processed/tdlr_scored.parquet")

def client():
    ep = os.environ.get("AZURE_TEXT_ENDPOINT")
    key = os.environ.get("AZURE_TEXT_KEY")
    if not ep or not key:
        raise SystemExit("Missing AZURE_TEXT_ENDPOINT or AZURE_TEXT_KEY.")
    return TextAnalyticsClient(endpoint=ep, credential=AzureKeyCredential(key))

def main():
    if not INP.exists():
        raise SystemExit("Run clean_normalize.py first.")
    df = pd.read_parquet(INP)
    texts = df["Description"].astype(str).tolist()

    cl = client()
    results = []
    for i in range(0, len(texts), 10):
        resp = cl.analyze_sentiment(documents=texts[i:i+10])
        for r in resp:
            if r.is_error:
                results.append(("unknown", 0.0, 0.0, 0.0))
            else:
                results.append((r.sentiment, r.confidence_scores.positive,
                                r.confidence_scores.neutral, r.confidence_scores.negative))
    n = min(len(results), len(df))
    df = df.iloc[:n].copy()
    df[["sentiment","pos","neu","neg"]] = pd.DataFrame(results[:n], index=df.index)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Wrote {OUT} with {len(df)} rows")

if __name__ == "__main__":
    main()
