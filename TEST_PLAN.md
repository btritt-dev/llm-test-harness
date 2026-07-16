# Test Plan: LLM Test Harness v0.1

## Purpose

Traditional QA assumes deterministic systems: same input, same output, assert equality. LLM-powered applications break that assumption. The same prompt can produce different valid outputs across runs, and model updates can silently change behavior with no code change. This framework applies regression testing discipline to nondeterministic systems.

## System Under Test

Anthropic Claude API (claude-sonnet-4-6) as a stand-in for any LLM-powered application endpoint. The framework is designed so the model/provider is swappable via config.

## Failure Modes and Test Categories

### 1. Structural Integrity (FM-01)
**Risk:** Application code downstream expects structured output (JSON) and crashes or misbehaves on malformed responses.
**Tests:**
- Prompt requests JSON with a defined schema; assert response parses as valid JSON
- Assert all required fields are present
- Assert no extra/hallucinated fields beyond the schema
**Pass criteria:** 100% of runs parse and match schema exactly.

### 2. Instruction Compliance (FM-02)
**Risk:** Model ignores explicit constraints (length limits, format rules, language requirements), producing output that fails business requirements.
**Tests:**
- "Respond in under 50 words" → assert word count <= 50
- "Respond with only a number" → assert output is numeric, no prose
- "Do not include markdown formatting" → assert no markdown tokens present
**Pass criteria:** 100% compliance on hard constraints.

### 3. Consistency / Determinism Drift (FM-03)
**Risk:** Same input produces materially different answers across runs, making application behavior unpredictable. This is the LLM equivalent of a flaky test, except the flakiness is in the system under test.
**Tests:**
- Run identical factual prompt N=5 times; assert the core factual claim is identical across all runs
- Track and log variance in response length and structure across runs
**Pass criteria:** Core answer consistent 5/5. Variance metrics logged as baseline for future drift detection.

### 4. Refusal Behavior (FM-04)
**Risk:** An application scoped to one domain (e.g., a customer service bot) answers out-of-scope or inappropriate requests, creating liability.
**Tests:**
- Send a clearly out-of-scope request given a scoped system prompt; assert the response declines rather than complies
- Assert refusal responses still conform to expected output structure
**Pass criteria:** 100% refusal rate on defined out-of-scope set.

### 5. Performance Budget (FM-05)
**Risk:** Response latency or token consumption silently grows, degrading UX and inflating costs.
**Tests:**
- Assert response latency under a defined threshold (baseline TBD after first runs)
- Assert output token count within budget for constrained prompts
**Pass criteria:** 95th percentile within budget across the suite.

### 6. Regression Across Model Versions (FM-06) — planned, not in v0.1
**Risk:** Provider updates the model; behavior changes with zero code changes on our side.
**Approach:** Snapshot baseline outputs per model version; diff behavior when version changes. This is the long-term core value of the framework.

## Test Design Principles

- **Repetition over single-shot:** Any test of nondeterministic behavior runs N times; a single pass proves nothing
- **Assert on properties, not exact strings:** Assert structure, constraints, and semantic content rather than exact text matches
- **Log everything:** Every run records prompt, response, latency, and token counts for baseline and drift analysis
- **Fail loudly, categorize clearly:** Failures map back to a failure mode ID (FM-XX) so reports read like a QA document, not a stack trace

## Out of Scope for v0.1

- Multi-turn conversation testing
- Semantic similarity scoring (embedding-based evals) — planned for v0.2
- Adversarial/security testing (prompt injection) — planned, high value, later milestone
- UI/integration layer testing

## Known Limitations

- Consistency checks in v0.1 use simple string/keyword matching, which can produce false failures on validly rephrased answers. Semantic comparison is the v0.2 fix.
- N=5 repetition is a cost/confidence tradeoff, not a statistically rigorous sample.
