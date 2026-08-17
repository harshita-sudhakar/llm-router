import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from anthropic import Anthropic

from eval.runner import run_case_routed
from eval.test_set import TEST_SET, validate_test_set

RESULTS_PATH = Path(__file__).resolve().parent.parent / "reports" / "router_results.json"


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
        result = run_case_routed(client, case)
        new_results[case["id"]] = result
        mark = "OK" if result["correct"] else "MISS"
        print(f"{mark} predicted={result['predicted_tier']} truth={result['ground_truth_tier']}")

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    if only_ids and RESULTS_PATH.exists():
        existing = {r["id"]: r for r in json.loads(RESULTS_PATH.read_text())}
        existing.update(new_results)
        # preserve original TEST_SET order
        order = {c["id"]: i for i, c in enumerate(TEST_SET)}
        results = sorted(existing.values(), key=lambda r: order.get(r["id"], len(order)))
    else:
        results = list(new_results.values())

    RESULTS_PATH.write_text(json.dumps(results, indent=2))

    correct = sum(r["correct"] for r in results)
    total_cost = sum(r["cost_usd"] for r in new_results.values())
    print(f"\nRouter eval: {correct}/{len(results)} correct overall (this run cost ${total_cost:.4f})")
    print(f"Results written to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
