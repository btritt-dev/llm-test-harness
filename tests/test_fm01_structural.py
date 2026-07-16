"""FM-01: Structural Integrity.

Verifies that when explicitly instructed to respond with JSON matching a
given schema, the model's raw response parses as valid JSON and matches
the schema exactly - all required fields present, no extra fields.
"""

import json

from src.client import ask

FM01_SYSTEM_PROMPT = (
    "You are a JSON API. Respond with ONLY valid JSON matching this exact "
    "schema, no prose, no markdown code fences, no explanation:\n"
    "{\n"
    '  "name": string,\n'
    '  "age": integer,\n'
    '  "occupation": string\n'
    "}"
)
FM01_USER_PROMPT = "Extract structured data for: Jane Doe, a 34-year-old software engineer."
REQUIRED_FIELDS = {"name", "age", "occupation"}


def _get_json_reply() -> dict:
    """Call the model with the FM-01 prompt and parse its reply as JSON.

    No pre-cleanup of the raw reply (no fence stripping, no trimming beyond
    what json.loads already tolerates) - a model that ignores the "no
    markdown fences" instruction and wraps its output in fences should fail
    here. That's the regression FM-01 exists to catch, not a bug in the test.
    """
    reply = ask(FM01_USER_PROMPT, system=FM01_SYSTEM_PROMPT)
    try:
        return json.loads(reply)
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"FM-01: response did not parse as valid JSON.\nRaw response: {reply!r}"
        ) from e


def test_fm01_valid_json_structure():
    """FM-01: response must parse as a valid JSON object."""
    data = _get_json_reply()
    assert isinstance(data, dict), (
        f"FM-01: parsed JSON is not an object (got {type(data).__name__})"
    )


def test_fm01_required_fields_present():
    """FM-01: all schema-required fields must be present in the response."""
    data = _get_json_reply()
    missing = REQUIRED_FIELDS - data.keys()
    assert not missing, f"FM-01: missing required fields: {missing}"


def test_fm01_no_extra_fields():
    """FM-01: response must not contain fields beyond the defined schema."""
    data = _get_json_reply()
    extra = data.keys() - REQUIRED_FIELDS
    assert not extra, f"FM-01: unexpected extra fields: {extra}"


def test_fm01_field_types():
    """FM-01: fields must match the expected schema types."""
    data = _get_json_reply()
    assert isinstance(data.get("name"), str), "FM-01: 'name' must be a string"
    assert isinstance(data.get("age"), int), "FM-01: 'age' must be an integer"
    assert isinstance(data.get("occupation"), str), "FM-01: 'occupation' must be a string"
