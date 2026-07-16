"""FM-03: Consistency / Determinism Drift.

Runs an identical factual prompt N=5 times and verifies the core factual
claim is stable across all runs. Also logs response-length variance as a
baseline for future drift detection - not asserted against a threshold,
since TEST_PLAN.md v0.1 only calls for logging this, not failing on it.
"""

import pytest

from src.client import ask

FM03_PROMPT = "What is the capital of France?"
CORE_ANSWER_KEYWORD = "paris"
N_RUNS = 5


@pytest.fixture(scope="module")
def fm03_replies() -> list[str]:
    """Run the FM-03 prompt N_RUNS times once, shared across this file's tests."""
    return [ask(FM03_PROMPT) for _ in range(N_RUNS)]


def test_fm03_consistent_core_answer(fm03_replies):
    """FM-03: the core factual claim must appear in every run's reply."""
    failures = [
        i
        for i, reply in enumerate(fm03_replies)
        if CORE_ANSWER_KEYWORD not in reply.lower()
    ]
    assert not failures, (
        f"FM-03: core answer '{CORE_ANSWER_KEYWORD}' missing in "
        f"{len(failures)}/{N_RUNS} runs (indices {failures}): "
        f"{[fm03_replies[i] for i in failures]!r}"
    )


def test_fm03_response_variance(fm03_replies):
    """FM-03: log response-length variance across runs as a drift baseline.

    Not asserted against a threshold - TEST_PLAN.md v0.1 calls for logging
    this data for future drift detection, not failing the test on it.
    """
    assert all(reply.strip() for reply in fm03_replies), (
        "FM-03: at least one of the 5 runs returned an empty reply"
    )

    word_counts = [len(reply.strip().split()) for reply in fm03_replies]
    minimum = min(word_counts)
    maximum = max(word_counts)
    mean = sum(word_counts) / len(word_counts)

    print(f"\nFM-03 response length variance (words) over {N_RUNS} runs:")
    print(f"  counts: {word_counts}")
    print(f"  min={minimum} max={maximum} mean={mean:.1f}")
