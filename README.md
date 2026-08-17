# LLM Routing

A routing layer that sits in front of the Anthropic API and picks which
model tier (Haiku / Sonnet / Opus) handles each turn of a conversation,
based on task complexity — aiming to cut cost and latency on simple tasks
without sacrificing quality on hard ones.

This is a CLI project, not a Claude skill: skills don't control model
selection, so this app manages its own conversation history and calls the
API directly.

See [`plan.md`](plan.md) for the full project plan and timeline. This
README documents what's built so far (Week 1: core routing logic).

## Status

- [x] **Week 1** — core routing logic (this README)
- [x] Week 2 — eval harness (labeled test set, accuracy/cost/latency vs. an always-Opus baseline)
- [x] Week 3 — edge cases (mid-conversation shifts, report generation)
- [ ] Week 4 (stretch) — trained classifier v2

## How it works

Each turn is routed through two layers, cheapest first:

1. **Escalation rules** (`router/escalation.py`) — free, code-level regex
   checks. No API call. If the prompt mentions code/file extensions,
   multi-step language ("first... then..."), tool/agentic phrasing ("search
   for", "call the API"), is unusually long, or has a file attached, it
   escalates straight to `opus`. Tool-use language is a **hard override**,
   checked first — a malformed tool call from an underpowered model is
   worse than overpaying for a stronger one.

2. **Classifier** (`router/classifier.py`) — only runs if no escalation
   rule fired. One Haiku call, prompted to return strict JSON
   (`{"tier": ..., "confidence": ...}`). Unparseable or invalid output fails
   safe to `opus` at confidence 0.

`router/router.py` orchestrates both: escalation first, classifier as
fallback, and one more safety net — classifier confidence below `0.5`
overrides up to `opus` rather than trusting a shaky guess. It returns a
decision dict (`tier`, `reason`, `source`, `confidence`) so later failure
analysis can tell rule-hits apart from classifier judgments.

`router/conversation.py`'s `ConversationManager` holds the full message
history and resends it in full to whichever model tier gets picked each
turn, since conversation state doesn't carry over automatically when the
model changes mid-conversation. It also exposes `recent_context()` — the
last couple of turns as plain text — which gets fed into the classifier so
that context-dependent follow-ups ("what about the second one?") aren't
misjudged as simple in isolation.

## File structure

```
LLM_routing/
├── plan.md                    full project plan and timeline
├── config.py                  tier name -> Anthropic model ID mapping
├── cli.py                     interactive entry point
├── router/
│   ├── escalation.py          free pattern-based escalation rules
│   ├── classifier.py          Haiku-based judgment classifier
│   ├── router.py              combines escalation + classifier -> final decision
│   └── conversation.py        ConversationManager (shared history across model swaps)
├── tests/
│   └── test_router.py         unit tests (classifier mocked, no API key needed)
├── requirements.txt
└── .env.example                template for ANTHROPIC_API_KEY
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your ANTHROPIC_API_KEY
```

## Usage

```bash
python cli.py
```

Each response is prefixed with which tier handled it and why, e.g.:

```
you> what's the capital of France?
[routed to HAIKU — classifier: classifier_judgment]
assistant> Paris.

you> write me a python function to reverse a linked list
[routed to OPUS — escalation_rule: escalation_code_generation]
assistant> ...
```

## Tests

```bash
pytest tests/
```

Covers escalation-rule pattern matching and router decision logic
(escalation short-circuiting the classifier, low-confidence overrides).
The classifier's API call is mocked, so this suite needs no API key and
makes no network calls.
