# LLM Routing Project — Plan
 
## The idea
A routing layer that sits in front of the Anthropic API and picks which model
tier (Haiku / Sonnet / Opus) handles each turn of a conversation, based on
task complexity. Goal: cut cost and latency on simple tasks without
sacrificing quality on hard ones. Not a Claude skill — skills don't control
model selection, so this is a standalone app/wrapper that manages its own
conversation history and calls the API directly.
 
Prior art to know and be able to speak to in interviews: RouteLLM (Berkeley
LMSYS), vLLM Semantic Router, Not Diamond, Martian, OpenRouter's auto router.
 
No front-end needed. A CLI + generated markdown/HTML report per run is enough.
Eval rigor is what makes this a real project instead of a demo.
 
---
 
## Architecture
 
1. **Classifier** — scores incoming prompt complexity. Start with a
   prompt-based classifier using Haiku (fast, cheap, no training needed).
2. **Router** — maps classifier output to a model tier. Includes hard-coded
   escalation rules (code generation, multi-step tasks, tool use always go
   to the strongest tier regardless of classifier score).
3. **Conversation manager** — single message history object; resends full
   context to whichever model is picked each turn, since state doesn't
   persist automatically across model swaps. Classifies per-turn (allows
   mid-conversation downgrading, not just escalation), but the classifier
   call includes recent context (last 1-2 turns or a short summary), not
   just the isolated current message, so context-heavy follow-ups that read
   as simple in isolation aren't misrouted to a lower tier.
4. **Eval harness** — labeled test set with ground-truth tiers, measures
   routing accuracy, cost, and latency against an always-Opus baseline.
5. **Report output** — generated markdown/HTML per run: routing decisions,
   cost/latency comparison table, failure analysis. No live dashboard.
---
 
## Timeline
 
### Week 1 — Core routing logic
- [ ] Set up API access to 2-3 model tiers (Haiku, Sonnet, Opus)
- [ ] Build prompt-based classifier (simple / moderate / complex)
- [ ] Build router with tier mapping + hard-coded escalation rules
- [ ] Build conversation manager (shared history across model swaps)
### Week 2 — Eval and rigor
- [ ] Build labeled test set (50-100 prompts, ground-truth tier per prompt)
- [ ] Categories: factual lookup, short task, multi-step reasoning, code
      generation, tool use
- [ ] Run test set through router, measure routing accuracy
- [ ] Run same test set through always-Opus baseline, capture cost/latency
- [ ] Write up comparison: accuracy, cost savings, latency savings, failure
      analysis (where and why it misrouted)
### Week 3 (if time) — Edge cases and polish
- [ ] Test mid-conversation complexity shifts (starts simple, escalates)
- [ ] Handle malformed-output risk for tool-use tasks (structured output
      always escalates by default, don't rely on classifier alone)
- [ ] Generate clean per-run report file
---
 
### Week 4 (stretch) — Trained classifier v2
- [ ] Use classification data collected from v1 runs (Week 1-2) as training
      data, kept separate from the eval set to avoid testing on training data
- [ ] Train a lightweight classifier (e.g. small fine-tuned model or
      embeddings + simple model) to replace the Haiku prompt-based call
- [ ] Run the same eval set through v2, compare head-to-head against v1:
      accuracy, latency, cost per routing decision
- [ ] Write up the comparison as the production-scale answer to "why not
      train a classifier from the start" — this becomes the strongest part
      of the interview story: v1 shipped fast and de-risked the project, v2
      shows the production-scale iteration
---
 
## Open decisions (fill in as we go)
- Classifier approach: PROMPT-BASED for v1 (using Haiku), with a TRAINED
  classifier planned as a v2 stretch goal (see Week 4). Sequencing rationale:
  v1 ships fast, de-risks the routing/conversation-manager logic, and its
  classification outputs double as training data for v2. Comparing v1 vs v2
  head-to-head (accuracy, latency, cost) is a stronger interview story than
  committing to a trained classifier from the start.
  - Call design: ONE Haiku call for anything needing judgment (complexity
    tier + ambiguous escalation signals, returned as structured JSON).
    Clear-cut escalation rules (e.g. keyword/pattern matches like "build me
    a website") run as free code-level checks, not model calls. Rationale:
    minimize routing overhead so classification cost/latency doesn't eat
    into the savings the project is meant to demonstrate.
- Mid-conversation behavior: DOWNGRADES ALLOWED. Each turn is classified
  fresh (not pinned to the highest tier hit so far), so a complex ask
  followed by a simple follow-up can drop back down. Mitigates the "context
  looks simple in isolation" risk by including recent context in the
  classifier call rather than classifying the isolated current message alone.
- Escalation rule list:
  - Keyword/pattern-based (free, code-level, no model call): code
    generation requests (write code, build me a, debug this, file
    extensions/language names); explicit multi-step asks (step by step,
    numbered requirements, first/then/finally); tool/agentic language
    (search for, look up, call the API, use the [X] tool); long input
    length (200+ tokens); file/document attached
  - Needs judgment (folded into the one Haiku classifier call): ambiguous
    structurally-complex multi-part questions; domain-specific reasoning
    (math proofs, legal/medical nuance) where topic signals difficulty even
    if phrased simply; creative writing with specific constraints vs a
    one-line prompt; prompts referencing earlier context that changes
    difficulty
  - Hard overrides (always escalate regardless of score): any detected
    tool-use/function-calling request (malformed tool output is worse than
    an overpowered model); low classifier confidence defaults to the higher
    tier rather than guessing low
- Test set categories and count — ~95-100 prompts total:
  1. Simple factual/lookup (~15) — baseline sanity check, should route Haiku
  2. Short conversational/low-effort follow-ups (~10) — tests mid-conversation
     downgrade behavior specifically
  3. Moderate reasoning, no explicit structure (~15) — structurally complex
     but doesn't trip keyword rules; tests classifier judgment, not pattern
     matching
  4. Explicit multi-step/long-form (~10) — should trip free keyword-based
     escalation, not the classifier call
  5. Code generation (~15) — mix of trivial and complex, tests escalation
     rule catches both
  6. Tool use/agentic (~10) — hard-override category, most important given
     the malformed-output risk
  7. Domain-specific reasoning (~10) — math proofs, legal/medical nuance
     phrased simply; likely richest source of failure analysis
  8. Ambiguous/edge cases (~10-15) — deliberately hard to classify; protects
     failure analysis from being cherry-picked, don't cut this for time
  - For each test prompt, record ground-truth tier AND which rule/reasoning
    justifies it (keyword rule vs classifier judgment vs hard override), so
    failure analysis can distinguish rule misses from classifier misjudgments
- Report format: HTML. Generated per run, showing routing decisions,
  cost/latency comparison table, and failure analysis. No live dashboard,
  just a static file.
---
 
## Notes / log
(running notes as the project develops)