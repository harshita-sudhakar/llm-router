"""Labeled eval test set: ~95-100 prompts across 8 categories (see plan.md).

Each case:
- id: unique string
- category: one of the 8 plan categories
- turns: list of prior user turns + final turn to classify/route (len 1 = single-turn)
- ground_truth_tier: the tier a human reviewer believes is correct
- justification: which mechanism *should* produce that tier
    - "keyword_rule"        -> a free escalation.py rule should catch this
    - "hard_override"       -> tool-use hard override should catch this
    - "classifier_judgment" -> no rule fires; the Haiku classifier must judge it
"""

TEST_SET = [
    # 1. Simple factual/lookup (~15) — should route haiku, via classifier judgment
    {"id": "factual_01", "category": "simple_factual", "turns": ["What's the capital of France?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_02", "category": "simple_factual", "turns": ["Who wrote Romeo and Juliet?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_03", "category": "simple_factual", "turns": ["What year did World War 2 end?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_04", "category": "simple_factual", "turns": ["What's the boiling point of water in Celsius?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_05", "category": "simple_factual", "turns": ["How many continents are there?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_06", "category": "simple_factual", "turns": ["What's the largest planet in our solar system?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_07", "category": "simple_factual", "turns": ["Who is the current CEO of Tesla?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_08", "category": "simple_factual", "turns": ["What's the chemical symbol for gold?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_09", "category": "simple_factual", "turns": ["How many strings does a standard guitar have?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_10", "category": "simple_factual", "turns": ["What's the currency of Japan?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_11", "category": "simple_factual", "turns": ["What language is primarily spoken in Brazil?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_12", "category": "simple_factual", "turns": ["How many days are in a leap year?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_13", "category": "simple_factual", "turns": ["What's the speed of light in a vacuum?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_14", "category": "simple_factual", "turns": ["Who painted the Mona Lisa?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "factual_15", "category": "simple_factual", "turns": ["What's the tallest mountain in the world?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},

    # 2. Short conversational/low-effort follow-ups (~10) — multi-turn, tests downgrade behavior
    {"id": "followup_01", "category": "short_followup", "turns": ["Can you compare the economic policies of the US and China across trade, monetary policy, and industrial strategy?", "thanks, what about just trade specifically in one sentence?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_02", "category": "short_followup", "turns": ["Explain how gradient descent works in machine learning, including momentum and learning rate schedules.", "cool, and what's 12 * 8?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_03", "category": "short_followup", "turns": ["Walk me through the tradeoffs of microservices vs a monolith for a mid-size startup.", "got it, thanks!"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_04", "category": "short_followup", "turns": ["Analyze the causes of the 2008 financial crisis in detail.", "ok makes sense. what's today's date again?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_05", "category": "short_followup", "turns": ["Explain the philosophical differences between utilitarianism and deontology with examples.", "nice, one more thing - what's the opposite of 'ephemeral'?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_06", "category": "short_followup", "turns": ["Give me a detailed breakdown of how CRISPR gene editing works.", "interesting! quick one - who discovered penicillin?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_07", "category": "short_followup", "turns": ["Compare the architectural differences between transformers and RNNs for sequence modeling.", "got it. and hi, how are you?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_08", "category": "short_followup", "turns": ["Explain the legal doctrine of promissory estoppel with case examples.", "thanks - what's a synonym for 'happy'?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_09", "category": "short_followup", "turns": ["Break down the causes and consequences of the fall of the Roman Empire.", "ok cool, and what color is the sky?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "followup_10", "category": "short_followup", "turns": ["Explain how public-key cryptography enables secure communication over an insecure channel.", "got it thanks! what's 100 divided by 4?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},

    # 3. Moderate reasoning, no explicit structure (~15) — structurally complex, no keyword trip
    {"id": "moderate_01", "category": "moderate_reasoning", "turns": ["Explain the tradeoffs between REST and GraphQL for a mobile app backend"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_02", "category": "moderate_reasoning", "turns": ["Why might a company choose to lease equipment instead of buying it outright?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_03", "category": "moderate_reasoning", "turns": ["What factors should I consider when choosing between a SQL and NoSQL database for a new project?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_04", "category": "moderate_reasoning", "turns": ["How does inflation affect bond prices, and why is that relationship inverse?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_05", "category": "moderate_reasoning", "turns": ["What are the pros and cons of remote work for team collaboration and innovation?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_06", "category": "moderate_reasoning", "turns": ["Why do some species evolve toward larger body size over geological time?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_07", "category": "moderate_reasoning", "turns": ["How should a startup think about pricing a new SaaS product?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_08", "category": "moderate_reasoning", "turns": ["What's the difference between correlation and causation, and why does it matter in policy decisions?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_09", "category": "moderate_reasoning", "turns": ["Why did the gold standard eventually get abandoned by most economies?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_10", "category": "moderate_reasoning", "turns": ["How do vaccines train the immune system to respond to future infections?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_11", "category": "moderate_reasoning", "turns": ["What makes a caching strategy effective for a high-traffic web application?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_12", "category": "moderate_reasoning", "turns": ["Why is technical debt hard to prioritize against new feature work?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_13", "category": "moderate_reasoning", "turns": ["What's the reasoning behind progressive taxation as opposed to a flat tax?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_14", "category": "moderate_reasoning", "turns": ["How does DNS resolution actually work when you type a URL into a browser?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "moderate_15", "category": "moderate_reasoning", "turns": ["Why do some negotiations benefit from an anchoring strategy and others don't?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},

    # 4. Explicit multi-step/long-form (~10) — should trip free keyword escalation
    {"id": "multistep_01", "category": "multi_step", "turns": ["Walk me through, step by step, how to set up a CI/CD pipeline for a Python project."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_02", "category": "multi_step", "turns": ["First, summarize the plot of Hamlet. Then, explain its main themes. Finally, compare it to Macbeth."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_03", "category": "multi_step", "turns": ["1. Define supply and demand\n2. Explain equilibrium price\n3. Give a real-world example"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_04", "category": "multi_step", "turns": ["Give me a step by step guide to preparing for a marathon over 16 weeks."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_05", "category": "multi_step", "turns": ["First explain what a mortgage is, then explain amortization, then explain refinancing."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_06", "category": "multi_step", "turns": ["Break this down step by step: how does a bill become a law in the US?"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_07", "category": "multi_step", "turns": ["1) List the planets in order from the sun 2) note which are gas giants 3) note which have rings"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_08", "category": "multi_step", "turns": ["First tell me the ingredients for a basic bread recipe, then the steps, and finally storage tips."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_09", "category": "multi_step", "turns": ["Step by step, explain how photosynthesis converts sunlight into chemical energy."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "multistep_10", "category": "multi_step", "turns": ["First describe the water cycle, then explain evaporation in more detail, finally explain condensation."], "ground_truth_tier": "opus", "justification": "keyword_rule"},

    # 5. Code generation (~15) — mix of trivial and complex, both should escalate
    {"id": "code_01", "category": "code_generation", "turns": ["Write a python function to reverse a string."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_02", "category": "code_generation", "turns": ["Can you write me some code to check if a number is prime?"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_03", "category": "code_generation", "turns": ["Build me a website landing page with HTML and CSS."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_04", "category": "code_generation", "turns": ["Debug this: def add(a, b): return a - b"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_05", "category": "code_generation", "turns": ["Fix this bug in my sorting function, it's returning the wrong order."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_06", "category": "code_generation", "turns": ["Implement a binary search tree in Java with insert and delete methods."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_07", "category": "code_generation", "turns": ["Write a SQL query to find the top 5 customers by total order value."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_08", "category": "code_generation", "turns": ["I need a script.py that renames all files in a folder to lowercase."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_09", "category": "code_generation", "turns": ["Write a JavaScript function that debounces an input handler."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_10", "category": "code_generation", "turns": ["Implement a rate limiter in Go using a token bucket algorithm."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_11", "category": "code_generation", "turns": ["Write code to merge two sorted linked lists in C++."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_12", "category": "code_generation", "turns": ["Can you build me a simple REST API in typescript using express?"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_13", "category": "code_generation", "turns": ["Write a regex pattern to validate email addresses."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_14", "category": "code_generation", "turns": ["Implement quicksort in rust."], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "code_15", "category": "code_generation", "turns": ["Write a bash script that backs up a directory to S3 nightly."], "ground_truth_tier": "opus", "justification": "keyword_rule"},

    # 6. Tool use/agentic (~10) — hard override, most important given malformed-output risk
    {"id": "tooluse_01", "category": "tool_use", "turns": ["Search for the latest news on the Fed's interest rate decision."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_02", "category": "tool_use", "turns": ["Look up the current stock price of Apple."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_03", "category": "tool_use", "turns": ["Call the weather API to get today's forecast for Seattle."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_04", "category": "tool_use", "turns": ["Use the calculator tool to compute the monthly payment on a $30k loan at 6% APR."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_05", "category": "tool_use", "turns": ["Query the database for all users who signed up in the last 7 days."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_06", "category": "tool_use", "turns": ["Fetch the contents of this webpage and summarize it: example.com/article"], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_07", "category": "tool_use", "turns": ["Search for flights from SFO to JFK next Tuesday."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_08", "category": "tool_use", "turns": ["Look up the definition and etymology of the word 'ephemeral' using a dictionary tool."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_09", "category": "tool_use", "turns": ["Call the translation API to convert this sentence to Japanese."], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "tooluse_10", "category": "tool_use", "turns": ["Use the search tool to find recent papers on quantum error correction."], "ground_truth_tier": "opus", "justification": "hard_override"},

    # 7. Domain-specific reasoning (~10) — phrased simply, but hard; richest source of failure analysis
    {"id": "domain_01", "category": "domain_specific", "turns": ["Prove that the square root of 2 is irrational."], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_02", "category": "domain_specific", "turns": ["Can my landlord legally enter my apartment without notice?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_03", "category": "domain_specific", "turns": ["What's the difference between a stroke and a TIA, medically speaking?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_04", "category": "domain_specific", "turns": ["Prove that there are infinitely many prime numbers."], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_05", "category": "domain_specific", "turns": ["If I sign an NDA, can I still disclose the information to my lawyer?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_06", "category": "domain_specific", "turns": ["What's the mechanism by which SSRIs are thought to relieve depression symptoms?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_07", "category": "domain_specific", "turns": ["Is it possible to patent a mathematical algorithm in the US?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_08", "category": "domain_specific", "turns": ["Prove the Pythagorean theorem using similar triangles."], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_09", "category": "domain_specific", "turns": ["What are the legal differences between a misdemeanor and a felony?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "domain_10", "category": "domain_specific", "turns": ["Why is anesthesia dosing so dependent on body weight and metabolism?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},

    # 8. Ambiguous/edge cases (~12) — deliberately hard, protects failure analysis from cherry-picking
    {"id": "ambig_01", "category": "ambiguous", "turns": ["Tell me something interesting."], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "ambig_02", "category": "ambiguous", "turns": ["Is it better to rent or buy a home?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_03", "category": "ambiguous", "turns": ["Write a short poem about autumn."], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_04", "category": "ambiguous", "turns": ["Write a sonnet about loss that uses no more than 3 adjectives total and never mentions death directly."], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "ambig_05", "category": "ambiguous", "turns": ["What should I consider before quitting my job to start a business?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_06", "category": "ambiguous", "turns": ["Explain quantum entanglement like I'm five."], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_07", "category": "ambiguous", "turns": ["Is this a good trade: giving up a starting pitcher for two prospects?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_08", "category": "ambiguous", "turns": ["What do you think happens after we die?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_09", "category": "ambiguous", "turns": ["Why does my sourdough starter keep collapsing after it rises?"], "ground_truth_tier": "sonnet", "justification": "classifier_judgment"},
    {"id": "ambig_10", "category": "ambiguous", "turns": ["Give me a one-word answer: is Pluto a planet?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},
    {"id": "ambig_11", "category": "ambiguous", "turns": ["Design a fair rotation schedule for 5 roommates sharing 3 chores weekly, accounting for chore difficulty."], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "ambig_12", "category": "ambiguous", "turns": ["What's a good name for a coffee shop?"], "ground_truth_tier": "haiku", "justification": "classifier_judgment"},

    # 9. Mid-conversation escalation (~9) — multi-turn, opposite direction from
    # short_followup: starts simple, then a follow-up suddenly needs much more
    # capability. Tests that the router escalates mid-conversation, not just downgrades.
    {"id": "escalate_01", "category": "mid_conversation_escalation", "turns": ["What's the capital of France?", "actually, can you prove why Paris became the capital instead of another city, using historical political reasoning?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "escalate_02", "category": "mid_conversation_escalation", "turns": ["What's 12 times 8?", "interesting - can you prove the general multiplication algorithm works for any two integers?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "escalate_03", "category": "mid_conversation_escalation", "turns": ["Who wrote Pride and Prejudice?", "actually, write me a python script that scrapes Project Gutenberg for all her works"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "escalate_04", "category": "mid_conversation_escalation", "turns": ["What's the boiling point of water?", "ok, now walk me step by step through deriving the Clausius-Clapeyron relation"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "escalate_05", "category": "mid_conversation_escalation", "turns": ["What's the currency of Japan?", "can you look up today's USD to JPY exchange rate?"], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "escalate_06", "category": "mid_conversation_escalation", "turns": ["How many continents are there?", "actually can you debug this: for c in continents: print(c.name"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
    {"id": "escalate_07", "category": "mid_conversation_escalation", "turns": ["What language is spoken in Brazil?", "given that, can you analyze the legal implications of Brazil's official-language policy on federal court proceedings?"], "ground_truth_tier": "opus", "justification": "classifier_judgment"},
    {"id": "escalate_08", "category": "mid_conversation_escalation", "turns": ["Who painted the Mona Lisa?", "can you search for the current estimated market value of the painting?"], "ground_truth_tier": "opus", "justification": "hard_override"},
    {"id": "escalate_09", "category": "mid_conversation_escalation", "turns": ["What's the tallest mountain in the world?", "ok - first explain the geology behind how it formed, then explain how climbers acclimatize, finally explain the main death risks"], "ground_truth_tier": "opus", "justification": "keyword_rule"},
]


def validate_test_set():
    ids = [c["id"] for c in TEST_SET]
    assert len(ids) == len(set(ids)), "duplicate test case ids found"

    valid_tiers = {"haiku", "sonnet", "opus"}
    valid_justifications = {"keyword_rule", "hard_override", "classifier_judgment"}

    for case in TEST_SET:
        assert case["ground_truth_tier"] in valid_tiers, f"{case['id']}: bad tier"
        assert case["justification"] in valid_justifications, f"{case['id']}: bad justification"
        assert len(case["turns"]) >= 1, f"{case['id']}: needs at least one turn"

    return True


if __name__ == "__main__":
    validate_test_set()
    print(f"{len(TEST_SET)} test cases, all valid.")
    from collections import Counter
    print(Counter(c["category"] for c in TEST_SET))
