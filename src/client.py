"""Minimal wrapper around the Anthropic API for the test harness."""

import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Resolve .env relative to this file, not the process's cwd, so it loads
# correctly whether pytest is invoked from the repo root or elsewhere.
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

MODEL = "claude-sonnet-4-6"


def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not found. Create a .env file at the project "
            "root with ANTHROPIC_API_KEY=your-key-here."
        )
    return anthropic.Anthropic(api_key=api_key)


def ask(prompt: str, max_tokens: int = 1024, system: str | None = None) -> str:
    """Send a single user prompt to the model and return its text reply.

    Pass `system` to set a system prompt (e.g. instructing JSON-only output).
    """
    client = get_client()
    kwargs = {"system": system} if system is not None else {}
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    return "".join(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    reply = ask("Reply with exactly one short sentence confirming you are working.")
    print(reply)
