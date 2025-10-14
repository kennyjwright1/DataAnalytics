# src/viz/build_site.py
import pathlib, pandas as pd, plotly.express as px

DATA = pathlib.Path("data/processed/exports/program_month_sentiment.csv")
DOCS = pathlib.Path("docs")

def main():
    if not DATA.exists():
        raise SystemExit("Missing exports CSV. Run aggregates.py first.")
    df = pd.read_csv(DATA, parse_dates=["month"])
    if df.empty:
        raise SystemExit("No rows to plot.")

    # Charts
    pos = px.line(
        df, x="month", y="pos", color="Program",
        title="Average Positive Sentiment by Program (Monthly)",
        labels={"month": "Month", "pos": "Positive (0–1)"}
    )
    neg = px.line(
        df, x="month", y="neg", color="Program",
        title="Average Negative Sentiment by Program (Monthly)",
        labels={"month": "Month", "neg": "Negative (0–1)"}
    )
    vol = px.bar(
        df, x="month", y="count", color="Program", barmode="group",
        title="Monthly Volume by Program",
        labels={"month": "Month", "count": "Items"}
    )

    # Compose a single HTML page with all three figures
    html = f"""<!doctype html>
<meta charset="utf-8">
<title>TDLR Sentiment Dashboard</title>
<h1 style="font-family:system-ui;margin:16px 0">TDLR Sentiment Dashboard</h1>
<div>{pos.to_html(full_html=False, include_plotlyjs='cdn')}</div>
<div style="margin-top:24px">{neg.to_html(full_html=False, include_plotlyjs=False)}</div>
<div style="margin-top:24px">{vol.to_html(full_html=False, include_plotlyjs=False)}</div>
"""
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS/"index.html").write_text(html, encoding="utf-8")
    print("Wrote docs/index.html with 3 charts")

if __name__ == "__main__":
    main()
