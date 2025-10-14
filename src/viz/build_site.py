import pathlib, pandas as pd, plotly.express as px
DATA = pathlib.Path("data/processed/exports/program_month_sentiment.csv")
DOCS = pathlib.Path("docs")

def main():
    if not DATA.exists():
        raise SystemExit("Run aggregates.py first.")
    df = pd.read_csv(DATA, parse_dates=["month"])
    fig = px.line(df, x="month", y="pos", color="Program",
                  title="Avg Positive Sentiment by Program (Monthly)")
    DOCS.mkdir(parents=True, exist_ok=True)
    out = DOCS/"index.html"
    fig.write_html(out, include_plotlyjs="cdn", full_html=True)
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
