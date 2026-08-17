TIER_MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-5",
    "opus": "claude-opus-5",
}

TIER_ORDER = ["haiku", "sonnet", "opus"]

CLASSIFIER_MODEL = TIER_MODELS["haiku"]

DEFAULT_TIER = "sonnet"

LONG_INPUT_TOKEN_THRESHOLD = 200
