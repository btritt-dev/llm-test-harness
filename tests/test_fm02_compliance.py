"""FM-02: Instruction Compliance.

Verifies the model follows explicit hard constraints - length limits,
output-format restrictions, and formatting bans - when given a single,
self-contained instruction with no system-prompt reinforcement.
"""

import re

from src.client import ask

WORD_LIMIT_PROMPT = "Explain what photosynthesis is in under 50 words."
NUMERIC_ONLY_PROMPT = (
    "What is 12 multiplied by 8? Respond with only the number, no words, "
    "no punctuation, no explanation."
)
NO_MARKDOWN_PROMPT = (
    "Give me 3 tips for staying productive. Do not use any markdown "
    "formatting (no asterisks, no bullet points, no headers, no code blocks)."
)

NUMERIC_PATTERN = re.compile(r"-?\d+(\.\d+)?")

MARKDOWN_PATTERNS = [
    re.compile(r"\*\*.+?\*\*"),              # bold
    re.compile(r"`.+?`"),                    # inline code
    re.compile(r"```"),                      # code fence
    re.compile(r"^#{1,6}\s", re.MULTILINE),  # headers
    re.compile(r"^[-*]\s", re.MULTILINE),    # bullet lists
    re.compile(r"\[.+?\]\(.+?\)"),           # links
]


def test_fm02_word_limit():
    """FM-02: response must respect an explicit word-count constraint."""
    reply = ask(WORD_LIMIT_PROMPT)
    word_count = len(reply.strip().split())
    assert word_count <= 50, (
        f"FM-02: response was {word_count} words, exceeds the 50-word limit"
    )


def test_fm02_numeric_only():
    """FM-02: response must be only a number, no surrounding prose."""
    reply = ask(NUMERIC_ONLY_PROMPT)
    stripped = reply.strip()
    assert NUMERIC_PATTERN.fullmatch(stripped), (
        f"FM-02: response was not numeric-only: {reply!r}"
    )


def test_fm02_no_markdown():
    """FM-02: response must not contain markdown formatting tokens."""
    reply = ask(NO_MARKDOWN_PROMPT)
    for pattern in MARKDOWN_PATTERNS:
        assert not pattern.search(reply), (
            f"FM-02: response contains markdown formatting "
            f"(pattern {pattern.pattern!r}): {reply!r}"
        )
