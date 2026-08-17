import re

from config import LONG_INPUT_TOKEN_THRESHOLD

CODE_GEN_PATTERNS = [
    r"\bwrite\b.{0,20}\bcode\b",
    r"\bwrite\b.{0,20}\b(a |an )?(script|function|program|regex|query|class|method)\b",
    r"\bbuild me a\b",
    r"\bdebug this\b",
    r"\bfix this (bug|code|error)\b",
    r"\bimplement\b",
    r"\.(py|js|ts|tsx|jsx|java|cpp|c|go|rs|rb|php|sql|sh)\b",
    r"\b(python|javascript|typescript|java|c\+\+|golang|rust|ruby|php|sql|bash|shell script)\b",
]

MULTI_STEP_PATTERNS = [
    r"\bstep by step\b",
    r"\bfirst,?\s.*\bthen\b",
    r"\bfinally,?\b",
    r"^\s*\d+[\.\)]\s",
    r"\n\s*\d+[\.\)]\s",
]

TOOL_USE_PATTERNS = [
    r"\bsearch for\b",
    r"\blook up\b",
    r"\bcall the .* api\b",
    r"\buse the .* tool\b",
    r"\bquery the\b",
    r"\bfetch (the|from)\b",
]


def _matches_any(patterns, text_lower):
    return any(re.search(p, text_lower) for p in patterns)


def is_code_generation(text: str) -> bool:
    return _matches_any(CODE_GEN_PATTERNS, text.lower())


def is_multi_step(text: str) -> bool:
    return _matches_any(MULTI_STEP_PATTERNS, text.lower())


def is_tool_use(text: str) -> bool:
    return _matches_any(TOOL_USE_PATTERNS, text.lower())


def is_long_input(text: str) -> bool:
    # rough token estimate: ~4 chars/token
    return len(text) / 4 >= LONG_INPUT_TOKEN_THRESHOLD


def has_attachment(has_file: bool = False) -> bool:
    return has_file


def check_escalation(text: str, has_file: bool = False) -> dict | None:
    """Returns a dict with the tier and reason if a free rule fires, else None."""
    if is_tool_use(text):
        return {"tier": "opus", "reason": "hard_override_tool_use"}

    if is_code_generation(text):
        return {"tier": "opus", "reason": "escalation_code_generation"}

    if is_multi_step(text):
        return {"tier": "opus", "reason": "escalation_multi_step"}

    if is_long_input(text):
        return {"tier": "opus", "reason": "escalation_long_input"}

    if has_attachment(has_file):
        return {"tier": "opus", "reason": "escalation_file_attached"}

    return None
