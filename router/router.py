from router import classifier, escalation

LOW_CONFIDENCE_THRESHOLD = 0.5


def route(
    prompt: str,
    recent_context: str = "",
    has_file: bool = False,
    requires_structured_output: bool = False,
) -> dict:
    """Decide which model tier should handle this turn.

    Free, code-level escalation rules run first. If none fire, falls back to
    the Haiku classifier call. Low classifier confidence defaults to the
    higher tier rather than guessing low.

    requires_structured_output: set by the caller (not inferred from prompt
    text) when the call is already known to involve tool use / function
    calling / another structured-output format. Skips keyword-guessing
    entirely and escalates immediately, since a malformed structured output
    is worse than the cost of an "overpowered" model.
    """
    if requires_structured_output:
        return {
            "tier": "opus",
            "reason": "hard_override_structured_output",
            "source": "caller_override",
            "confidence": 1.0,
        }

    escalated = escalation.check_escalation(prompt, has_file=has_file)
    if escalated is not None:
        return {
            "tier": escalated["tier"],
            "reason": escalated["reason"],
            "source": "escalation_rule",
            "confidence": 1.0,
        }

    result = classifier.classify(prompt, recent_context=recent_context)
    tier = result["tier"]
    confidence = result["confidence"]

    if confidence < LOW_CONFIDENCE_THRESHOLD and tier != "opus":
        return {
            "tier": "opus",
            "reason": "low_confidence_default",
            "source": "classifier_low_confidence",
            "confidence": confidence,
        }

    return {
        "tier": tier,
        "reason": "classifier_judgment",
        "source": "classifier",
        "confidence": confidence,
    }
