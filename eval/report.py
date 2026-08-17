import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
RUNS_DIR = REPORTS_DIR / "runs"
ROUTER_RESULTS_PATH = REPORTS_DIR / "router_results.json"
BASELINE_RESULTS_PATH = REPORTS_DIR / "baseline_results.json"
LATEST_OUTPUT_PATH = REPORTS_DIR / "report.html"

TIER_COLORS = {"haiku": "#2563eb", "sonnet": "#7c3aed", "opus": "#dc2626"}


def load_results():
    router = json.loads(ROUTER_RESULTS_PATH.read_text())
    baseline = json.loads(BASELINE_RESULTS_PATH.read_text())
    return router, baseline


def summarize(router, baseline):
    router_correct = sum(r["correct"] for r in router)
    router_cost = sum(r["cost_usd"] for r in router)
    router_latency = sum(r["latency_s"] for r in router)

    baseline_cost = sum(r["cost_usd"] for r in baseline)
    baseline_latency = sum(r["latency_s"] for r in baseline)

    cost_savings_pct = (1 - router_cost / baseline_cost) * 100 if baseline_cost else 0
    latency_savings_pct = (1 - router_latency / baseline_latency) * 100 if baseline_latency else 0

    tier_dist = Counter(r["predicted_tier"] for r in router)

    by_category = defaultdict(lambda: {"total": 0, "correct": 0})
    for r in router:
        by_category[r["category"]]["total"] += 1
        by_category[r["category"]]["correct"] += r["correct"]

    by_source = defaultdict(lambda: {"total": 0, "correct": 0})
    for r in router:
        by_source[r["decision_source"]]["total"] += 1
        by_source[r["decision_source"]]["correct"] += r["correct"]

    misses = [r for r in router if not r["correct"]]

    return {
        "n": len(router),
        "router_accuracy": router_correct / len(router) if router else 0,
        "router_cost": router_cost,
        "router_latency": router_latency,
        "baseline_cost": baseline_cost,
        "baseline_latency": baseline_latency,
        "cost_savings_pct": cost_savings_pct,
        "latency_savings_pct": latency_savings_pct,
        "tier_dist": tier_dist,
        "by_category": dict(by_category),
        "by_source": dict(by_source),
        "misses": misses,
    }


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_html(summary: dict, run_timestamp: str) -> str:
    tier_dist_rows = "".join(
        f'<tr><td><span class="tier-dot" style="background:{TIER_COLORS[t]}"></span>{t}</td>'
        f'<td>{c}</td><td>{c / summary["n"] * 100:.1f}%</td></tr>'
        for t, c in sorted(summary["tier_dist"].items())
    )

    category_rows = "".join(
        f'<tr><td>{esc(cat)}</td><td>{v["correct"]}/{v["total"]}</td>'
        f'<td>{v["correct"] / v["total"] * 100:.0f}%</td></tr>'
        for cat, v in sorted(summary["by_category"].items())
    )

    source_rows = "".join(
        f'<tr><td>{esc(src)}</td><td>{v["correct"]}/{v["total"]}</td>'
        f'<td>{v["correct"] / v["total"] * 100:.0f}%</td></tr>'
        for src, v in sorted(summary["by_source"].items())
    )

    miss_rows = "".join(
        f'<tr><td>{esc(m["id"])}</td><td>{esc(m["category"])}</td>'
        f'<td><span class="tier-dot" style="background:{TIER_COLORS[m["ground_truth_tier"]]}"></span>{m["ground_truth_tier"]}</td>'
        f'<td><span class="tier-dot" style="background:{TIER_COLORS[m["predicted_tier"]]}"></span>{m["predicted_tier"]}</td>'
        f'<td>{esc(m["decision_source"])}</td><td>{esc(m["decision_reason"])}</td></tr>'
        for m in summary["misses"]
    )
    if not miss_rows:
        miss_rows = '<tr><td colspan="6" style="text-align:center;color:var(--muted)">No misses — 100% routing accuracy</td></tr>'

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>LLM Router Eval Report</title>
<style>
  :root {{
    --bg: #ffffff; --fg: #1a1a2e; --muted: #6b7280; --border: #e5e7eb;
    --card-bg: #f9fafb; --accent: #2563eb; --good: #16a34a; --bad: #dc2626;
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--fg); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 2rem; line-height: 1.5; }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  h1 {{ font-size: 1.5rem; margin-bottom: 0.25rem; }}
  .subtitle {{ color: var(--muted); margin-bottom: 2rem; font-size: 0.9rem; }}
  .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .stat-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; }}
  .stat-value {{ font-size: 1.75rem; font-weight: 600; }}
  .stat-label {{ color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.03em; }}
  .good {{ color: var(--good); }}
  section {{ margin-bottom: 2rem; }}
  h2 {{ font-size: 1.1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  th, td {{ text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border); }}
  th {{ color: var(--muted); font-weight: 500; font-size: 0.8rem; text-transform: uppercase; }}
  .tier-dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }}
  .table-wrap {{ overflow-x: auto; }}
</style>
</head>
<body>
<div class="container">
  <h1>LLM Router Eval Report</h1>
  <p class="subtitle">{summary["n"]} test cases &middot; router vs. always-opus baseline &middot; run {esc(run_timestamp)}</p>

  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-value">{summary["router_accuracy"] * 100:.1f}%</div>
      <div class="stat-label">Routing accuracy</div>
    </div>
    <div class="stat-card">
      <div class="stat-value good">{summary["cost_savings_pct"]:.1f}%</div>
      <div class="stat-label">Cost savings vs opus</div>
    </div>
    <div class="stat-card">
      <div class="stat-value good">{summary["latency_savings_pct"]:.1f}%</div>
      <div class="stat-label">Latency savings vs opus</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${summary["router_cost"]:.3f}</div>
      <div class="stat-label">Router total cost</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${summary["baseline_cost"]:.3f}</div>
      <div class="stat-label">Always-opus total cost</div>
    </div>
  </div>

  <section>
    <h2>Tier distribution (router)</h2>
    <div class="table-wrap">
    <table><thead><tr><th>Tier</th><th>Count</th><th>%</th></tr></thead>
    <tbody>{tier_dist_rows}</tbody></table>
    </div>
  </section>

  <section>
    <h2>Accuracy by category</h2>
    <div class="table-wrap">
    <table><thead><tr><th>Category</th><th>Correct</th><th>%</th></tr></thead>
    <tbody>{category_rows}</tbody></table>
    </div>
  </section>

  <section>
    <h2>Accuracy by decision source</h2>
    <div class="table-wrap">
    <table><thead><tr><th>Source</th><th>Correct</th><th>%</th></tr></thead>
    <tbody>{source_rows}</tbody></table>
    </div>
  </section>

  <section>
    <h2>Failure analysis (misrouted cases)</h2>
    <div class="table-wrap">
    <table><thead><tr><th>ID</th><th>Category</th><th>Ground truth</th><th>Predicted</th><th>Source</th><th>Reason</th></tr></thead>
    <tbody>{miss_rows}</tbody></table>
    </div>
  </section>
</div>
</body>
</html>"""


def main():
    router, baseline = load_results()
    summary = summarize(router, baseline)

    now = datetime.now(timezone.utc)
    run_timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
    file_stamp = now.strftime("%Y%m%d_%H%M%S")

    html = render_html(summary, run_timestamp)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_path = RUNS_DIR / f"report_{file_stamp}.html"
    run_path.write_text(html)
    LATEST_OUTPUT_PATH.write_text(html)

    print(f"Report written to {run_path}")
    print(f"Latest report updated at {LATEST_OUTPUT_PATH}")
    print(f"Accuracy: {summary['router_accuracy']*100:.1f}%  Cost savings: {summary['cost_savings_pct']:.1f}%  Latency savings: {summary['latency_savings_pct']:.1f}%")


if __name__ == "__main__":
    main()
