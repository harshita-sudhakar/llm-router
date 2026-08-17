"""Shared logic for running the test set through either the router or a
fixed always-X tier, capturing full outcomes for later reporting."""

import time

from anthropic import Anthropic

from config import TIER_MODELS
from eval.pricing import cost
from router.router import route


def _send_turns(client: Anthropic, model: str, turns: list[str]) -> tuple[str, int, int]:
    """Sends all turns in order as a single-user conversation (no assistant
    replies in between, since we only care about routing the final turn).
    Returns (reply_text, input_tokens, output_tokens) for the final call."""
    messages = [{"role": "user", "content": t} for t in turns]
    start = time.monotonic()
    response = client.messages.create(model=model, max_tokens=1024, messages=messages)
    latency = time.monotonic() - start

    text_block = next((b for b in response.content if b.type == "text"), None)
    reply = text_block.text if text_block else ""
    return reply, response.usage.input_tokens, response.usage.output_tokens, latency


def run_case_routed(client: Anthropic, case: dict) -> dict:
    """Routes the final turn using recent_context from prior turns, then
    sends the full turn list to whichever tier was chosen."""
    prior_turns = case["turns"][:-1]
    final_turn = case["turns"][-1]
    recent_context = "\n".join(f"user: {t}" for t in prior_turns)

    classify_start = time.monotonic()
    decision = route(final_turn, recent_context=recent_context)
    classify_latency = time.monotonic() - classify_start

    model = TIER_MODELS[decision["tier"]]
    reply, in_tok, out_tok, response_latency = _send_turns(client, model, case["turns"])

    classifier_cost = 0.0
    if decision["source"] != "escalation_rule":
        # classifier call itself used haiku; approximate its token cost
        # from a short system prompt + short JSON reply (not separately measured here)
        classifier_cost = cost("haiku", 150, 20)

    response_cost = cost(decision["tier"], in_tok, out_tok)

    return {
        "id": case["id"],
        "category": case["category"],
        "ground_truth_tier": case["ground_truth_tier"],
        "justification": case["justification"],
        "predicted_tier": decision["tier"],
        "decision_source": decision["source"],
        "decision_reason": decision["reason"],
        "confidence": decision["confidence"],
        "correct": decision["tier"] == case["ground_truth_tier"],
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cost_usd": response_cost + classifier_cost,
        "latency_s": classify_latency + response_latency,
        "reply_preview": reply[:200],
    }


def run_case_fixed_tier(client: Anthropic, case: dict, tier: str) -> dict:
    """Runs the case through a single fixed tier (e.g. always-opus baseline),
    no routing at all."""
    model = TIER_MODELS[tier]
    reply, in_tok, out_tok, latency = _send_turns(client, model, case["turns"])

    return {
        "id": case["id"],
        "category": case["category"],
        "ground_truth_tier": case["ground_truth_tier"],
        "predicted_tier": tier,
        "correct": tier == case["ground_truth_tier"],
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cost_usd": cost(tier, in_tok, out_tok),
        "latency_s": latency,
        "reply_preview": reply[:200],
    }
