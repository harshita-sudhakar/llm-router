"""Rough pre-flight cost estimate for running run_eval.py + run_baseline.py,
using char/4 token approximation (no API calls)."""

from eval.pricing import cost
from eval.test_set import TEST_SET

ASSUMED_OUTPUT_TOKENS = {"haiku": 120, "sonnet": 220, "opus": 320}
CLASSIFIER_INPUT_TOKENS = 150
CLASSIFIER_OUTPUT_TOKENS = 20


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def main():
    router_cost = 0.0
    baseline_cost = 0.0

    for case in TEST_SET:
        full_input = sum(estimate_tokens(t) for t in case["turns"])
        tier = case["ground_truth_tier"]  # best guess at what the router will pick

        router_cost += cost(tier, full_input, ASSUMED_OUTPUT_TOKENS[tier])
        if case["justification"] == "classifier_judgment":
            router_cost += cost("haiku", CLASSIFIER_INPUT_TOKENS, CLASSIFIER_OUTPUT_TOKENS)

        baseline_cost += cost("opus", full_input, ASSUMED_OUTPUT_TOKENS["opus"])

    print(f"{len(TEST_SET)} test cases")
    print(f"Estimated router eval cost:   ${router_cost:.4f}")
    print(f"Estimated always-opus cost:   ${baseline_cost:.4f}")
    print(f"Estimated total (both runs):  ${router_cost + baseline_cost:.4f}")
    print("\n(Rough estimate: char/4 token approximation, assumed output lengths. Actual cost may vary.)")


if __name__ == "__main__":
    main()
