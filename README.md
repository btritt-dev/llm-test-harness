# llm-test-harness

Regression testing for applications built on large language models.

**The problem:** an LLM provider ships a model update, and application behavior changes overnight without a single code change. No diff to review, no failing build, nothing. Traditional regression testing assumes deterministic outputs, so this failure mode is invisible to it.

## Approach

Built from 7+ years of software test engineering. The core shift: nondeterminism is the thing under test, not an inconvenience to retry away.

- **Structural checks.** If the app expects JSON with specific fields, a response that *almost* matches is a failure, not a curiosity.
- **Instruction compliance.** Hard constraints (length limits, format rules) get asserted, never assumed.
- **Consistency across runs.** Every nondeterministic test runs N times. A single pass proves nothing.

Full failure mode catalog, pass criteria, and known limitations: [TEST_PLAN.md](TEST_PLAN.md).

## Design principles

1. **Assert on properties, not exact strings.** Exact-match assertions against an LLM are a flaky test factory.
2. **Repetition is not optional.** Flakiness in the system under test is what's being measured.
3. **Failures map to failure mode IDs (FM-01 through FM-06).** A test report should read like a QA document, not a stack trace.

## Where this is going

Model version regression detection (FM-06): snapshot baseline behavior per model version, then diff when the provider ships an update. Example: a scoped support bot that reliably refused off-topic requests on one model version starts answering them after an update. That's a production incident today; here it's a failing test.

## Running it

    pip install -r requirements.txt

Set your API key in a `.env` file (gitignored, never committed):

    ANTHROPIC_API_KEY=your-key-here

Then:

    pytest -v

## Status

v0.1 in progress. Next: FM-01 (structural), FM-02 (compliance), FM-03 (consistency) as working pytest suites.
