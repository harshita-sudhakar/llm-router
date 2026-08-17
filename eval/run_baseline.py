import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from anthropic import Anthropic

from eval.runner import run_case_fixed_tier
from eval.test_set import TEST_SET, validate_test_set

RESULTS_PATH = Path(__file__).resolve().parent.parent / "reports" / "baseline_results.json"
BASELINE_TIER = "opus"


def main():
    validate_test_set()
    client = Anthropic()

    only_ids = set(sys.argv[1:]) or None
    cases = [c for c in TEST_SET if only_ids is None or c["id"] in only_ids]
    if only_ids:
        missing = only_ids - {c["id"] for c in cases}
        if missing:
            print(f"Warning: unknown test ids ignored: {missing}")

    new_results = {}
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {case['id']} ({case['category']})...", end=" ")
        result = run_case_fixed_tier(client, case, BASELINE_TIER)
        new_results[case["id"]] = result
        mark = "OK" if result["correct"] else "MISS"
        print(f"{mark}")

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    if only_ids and RESULTS_PATH.exists():
        existing = {r["id"]: r for r in json.loads(RESULTS_PATH.read_text())}
        existing.update(new_results)
        order = {c["id"]: i for i, c in enumerate(TEST_SET)}
        results = sorted(existing.values(), key=lambda r: order.get(r["id"], len(order)))
    else:
        results = list(new_results.values())

    RESULTS_PATH.write_text(json.dumps(results, indent=2))

    total_cost = sum(r["cost_usd"] for r in new_results.values())
    total_latency = sum(r["latency_s"] for r in new_results.values())
    print(f"\nAlways-{BASELINE_TIER} baseline: this run cost ${total_cost:.4f}, latency {total_latency:.1f}s")
    print(f"Results written to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
