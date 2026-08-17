"""Anthropic API pricing, USD per million tokens (as of 2026-08-16).
Source: https://platform.claude.com/docs/en/about-claude/pricing
Matches the model versions pinned in config.py (Haiku 4.5, Sonnet 5, Opus 5).
"""

PRICE_PER_MTOK = {
    "haiku": {"input": 1.0, "output": 5.0},
    "sonnet": {"input": 2.0, "output": 10.0},
    "opus": {"input": 5.0, "output": 25.0},
}


def cost(tier: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICE_PER_MTOK[tier]
    return (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000
