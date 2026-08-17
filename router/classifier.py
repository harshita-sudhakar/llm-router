import json
import re

from anthropic import Anthropic

from config import CLASSIFIER_MODEL

JSON_OBJECT_PATTERN = re.compile(r"\{.*?\}", re.DOTALL)

CLASSIFIER_SYSTEM_PROMPT = """You are a routing classifier. Given a user prompt \
(and optionally recent conversation context), decide how much reasoning capability \
is needed to answer it well.

Respond with ONLY a JSON object, no other text, no markdown code fences, and no \
explanation before or after it. Your entire response must be exactly this shape:
{"tier": "haiku" | "sonnet" | "opus", "confidence": 0.0-1.0}

Guidance:
- "haiku": simple factual lookups, short conversational replies, low-effort follow-ups.
- "sonnet": moderate reasoning, structurally complex but not domain-hard.
- "opus": domain-specific reasoning (math proofs, legal/medical nuance), ambiguous \
multi-part questions, or anything requiring careful judgment.

If you are unsure, prefer a higher tier over guessing low."""


def classify(prompt: str, recent_context: str = "") -> dict:
    client = Anthropic()

    user_content = prompt
    if recent_context:
        user_content = f"Recent conversation context:\n{recent_context}\n\nCurrent message:\n{prompt}"

    response = client.messages.create(
        model=CLASSIFIER_MODEL,
        max_tokens=300,
        system=CLASSIFIER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    text_block = next((b for b in response.content if b.type == "text"), None)
    raw = text_block.text.strip() if text_block else ""
    match = JSON_OBJECT_PATTERN.search(raw)

    try:
        if match is None:
            raise ValueError("no JSON object found in classifier output")
        result = json.loads(match.group(0))
        tier = result.get("tier")
        confidence = float(result.get("confidence", 0.0))
        if tier not in ("haiku", "sonnet", "opus"):
            raise ValueError(f"invalid tier: {tier}")
        return {"tier": tier, "confidence": confidence}
    except (json.JSONDecodeError, ValueError, TypeError):
        # low-confidence default: fail toward the higher tier rather than guessing low
        return {"tier": "opus", "confidence": 0.0}
