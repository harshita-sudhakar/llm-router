import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from router import escalation, router


# --- escalation.py ---

def test_code_generation_detected():
    assert escalation.is_code_generation("write me some code to sort a list")
    assert escalation.is_code_generation("can you fix this bug in app.py")
    assert not escalation.is_code_generation("what's the capital of France?")


def test_code_generation_catches_non_code_keyword_requests():
    # regression: these don't say "code" and have no matching file extension,
    # but are still code-gen requests (found via eval/run_eval.py, code_13/code_15)
    assert escalation.is_code_generation("Write a regex pattern to validate email addresses.")
    assert escalation.is_code_generation("Write a bash script that backs up a directory to S3 nightly.")


def test_multi_step_detected():
    assert escalation.is_multi_step("Let's do this step by step")
    assert escalation.is_multi_step("First, do X. Then do Y. Finally, do Z.")
    assert escalation.is_multi_step("1. do this\n2. do that")
    assert not escalation.is_multi_step("what's 2+2?")


def test_tool_use_detected():
    assert escalation.is_tool_use("search for the latest news on AI")
    assert escalation.is_tool_use("call the weather api")
    assert not escalation.is_tool_use("tell me a joke")


def test_long_input_detected():
    short_text = "hello there"
    long_text = "word " * 250
    assert not escalation.is_long_input(short_text)
    assert escalation.is_long_input(long_text)


def test_check_escalation_hard_override_tool_use_wins():
    result = escalation.check_escalation("search for and write code to parse it")
    assert result["reason"] == "hard_override_tool_use"
    assert result["tier"] == "opus"


def test_check_escalation_none_for_simple_prompt():
    assert escalation.check_escalation("what's the capital of France?") is None


# --- router.py ---

def test_route_escalation_rule_skips_classifier():
    with patch("router.router.classifier.classify") as mock_classify:
        decision = router.route("write code to reverse a string")
        assert decision["tier"] == "opus"
        assert decision["source"] == "escalation_rule"
        mock_classify.assert_not_called()


def test_route_uses_classifier_when_no_escalation():
    with patch("router.router.classifier.classify", return_value={"tier": "haiku", "confidence": 0.9}):
        decision = router.route("what's the capital of France?")
        assert decision["tier"] == "haiku"
        assert decision["source"] == "classifier"


def test_route_low_confidence_defaults_to_opus():
    with patch("router.router.classifier.classify", return_value={"tier": "sonnet", "confidence": 0.2}):
        decision = router.route("some ambiguous prompt")
        assert decision["tier"] == "opus"
        assert decision["source"] == "classifier_low_confidence"


def test_route_low_confidence_opus_stays_opus():
    with patch("router.router.classifier.classify", return_value={"tier": "opus", "confidence": 0.1}):
        decision = router.route("some ambiguous prompt")
        assert decision["tier"] == "opus"
        assert decision["source"] == "classifier"


def test_route_requires_structured_output_forces_opus_no_classifier_call():
    with patch("router.router.classifier.classify") as mock_classify:
        decision = router.route("what's the weather?", requires_structured_output=True)
        assert decision["tier"] == "opus"
        assert decision["source"] == "caller_override"
        assert decision["reason"] == "hard_override_structured_output"
        mock_classify.assert_not_called()
