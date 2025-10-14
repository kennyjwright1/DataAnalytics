# src/viz/build_site.py
import pathlib
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone

DATA = pathlib.Path("data/processed/exports/program_month_sentiment.csv")
DOCS = pathlib.Path("docs")

def _style_line(fig, ylab):
    fig.update_layout(
        template="plotly_white",
        legend_title="Program",
        margin=dict(l=40, r=20, t=60, b=40),
        hovermode="x unified",
        font=dict(family="Inter, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif", size=14),
    )
    fig.update_traces(mode="lines+markers")
    fig.update_xaxes(
        title="Month",
        rangeslider=dict(visible=True),
        rangeselector=dict(
            buttons=[
                dict(count=6,  step="month", stepmode="backward", label="6M"),
                dict(count=12, step="month", stepmode="backward", label="12M"),
                dict(step="all", label="All"),
            ]
        ),
    )
    fig.update_yaxes(title=ylab, rangemode="tozero")

def main():
    if not DATA.exists():
        raise SystemExit("Missing exports CSV. Run aggregates.py first.")
    df = pd.read_csv(DATA, parse_dates=["month"])

    if df.empty:
        raise SystemExit("No rows to plot.")

    # --- KPIs ---
    last_refresh = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_items = int(df["count"].sum())
    last_month = df["month"].max()
    last_month_items = int(df.loc[df["month"] == last_month, "count"].sum())

    # --- Smoothing: 3-month rolling averages per Program ---
    df = df.sort_values(["Program", "month"]).copy()
    for col in ["pos", "neg"]:
        df[f"{col}_roll3"] = df.groupby("Program")[col].transform(lambda s: s.rolling(3, min_periods=1).mean())

    # --- Charts ---
    pos = px.line(
        df, x="month", y="pos_roll3", color="Program",
        title="Average Positive Sentiment by Program (Monthly, 3-mo avg)",
        labels={"pos_roll3": "Positive (0–1)"}
    )
    _style_line(pos, "Positive (0–1)")
    pos.update_traces(hovertemplate="<b>%{x|%b %Y}</b><br>Positive: %{y:.2f}<extra></extra>")

    neg = px.line(
        df, x="month", y="neg_roll3", color="Program",
        title="Average Negative Sentiment by Program (Monthly, 3-mo avg)",
        labels={"neg_roll3": "Negative (0–1)"}
    )
    _style_line(neg, "Negative (0–1)")
    neg.update_traces(hovertemplate="<b>%{x|%b %Y}</b><br>Negative: %{y:.2f}<extra></extra>")

    vol = px.bar(
        df, x="month", y="count", color="Program", barmode="group",
        title="Monthly Volume by Program",
        labels={"count": "Items"}
    )
    vol.update_layout(
        template="plotly_white",
        legend_title="Program",
        margin=dict(l=40, r=20, t=60, b=40),
        font=dict(family="Inter, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif", size=14),
    )
    vol.update_xaxes(
        title="Month",
        rangeslider=dict(visible=True),
        rangeselector=dict(
            buttons=[
                dict(count=6,  step="month", stepmode="backward", label="6M"),
                dict(count=12, step="month", stepmode="backward", label="12M"),
                dict(step="all", label="All"),
            ]
        ),
    )
    vol.update_traces(hovertemplate="<b>%{x|%b %Y}</b><br>Items: %{y}<extra></extra>")

    # --- Compose HTML ---
    kpi_html = f"""
    <section style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0 20px">
      <div style="padding:14px 16px;border:1px solid #eee;border-radius:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)">
        <div style="font-size:12px;color:#666">Last refresh</div>
        <div style="font-weight:600">{last_refresh}</div>
      </div>
      <div style="padding:14px 16px;border:1px solid #eee;border-radius:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)">
        <div style="font-size:12px;color:#666">Total items</div>
        <div style="font-weight:600">{total_items:,}</div>
      </div>
      <div style="padding:14px 16px;border:1px solid #eee;border-radius:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)">
        <div style="font-size:12px;color:#666">Items in {last_month.strftime('%b %Y')}</div>
        <div style="font-weight:600">{last_month_items:,}</div>
      </div>
    </section>
    """

    html = f"""<!doctype html>
<meta charset="utf-8">
<title>TDLR Sentiment Dashboard</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.plot.ly" crossorigin>
<style>
  body {{ font-family: Inter, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 18px; }}
  h1 {{ margin: 4px 0 12px; font-size: 28px; }}
  .card {{ margin: 18px 0; }}
</style>
<h1>TDLR Sentiment Dashboard</h1>
{ kpi_html }
<div class="card">{pos.to_html(full_html=False, include_plotlyjs='cdn')}</div>
<div class="card">{neg.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="card">{vol.to_html(full_html=False, include_plotlyjs=False)}</div>
"""
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print("Wrote docs/index.html with styled KPIs + 3 charts")

if __name__ == "__main__":
    main()
