import json
import os
import re

from .prompts import SYSTEM, user_prompt

TYPES = {"positive", "negative", "boundary", "security", "performance"}
PRIORITIES = {"high", "medium", "low"}
DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")


class GenerationError(ValueError):
    pass


def detect_kind(text: str) -> str:
    if re.search(r"^\s*(openapi|swagger)\s*:", text, re.M) or '"openapi"' in text:
        return "OpenAPI specification"
    return "User story / requirements"


def parse_and_validate(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.S)  # tolerate code fences around the JSON
    if not match:
        raise GenerationError("Model reply contained no JSON object")
    data = json.loads(match.group(0))
    cases = data.get("test_cases")
    if not isinstance(cases, list) or not cases:
        raise GenerationError("No test_cases in model reply")
    seen = set()
    for i, tc in enumerate(cases, 1):
        for key in ("title", "type", "priority", "steps", "expected"):
            if key not in tc:
                raise GenerationError(f"Test case {i} is missing '{key}'")
        tc["type"] = tc["type"].lower() if tc["type"].lower() in TYPES else "positive"
        tc["priority"] = tc["priority"].lower() if tc["priority"].lower() in PRIORITIES else "medium"
        tc.setdefault("preconditions", "")
        tc["id"] = tc.get("id") or f"TC-{i:03d}"
        if tc["title"].lower() in seen:
            raise GenerationError(f"Duplicate test title: {tc['title']}")
        seen.add(tc["title"].lower())
    data.setdefault("feature", "Feature")
    return data


def generate(source: str, client=None, model: str = DEFAULT_MODEL, max_cases: int = 12) -> dict:
    """Ask Claude for test cases. `client` is an anthropic.Anthropic() or a test double."""
    if client is None:
        import anthropic  # imported lazily so tests and exports work without the SDK key

        client = anthropic.Anthropic()
    reply = client.messages.create(
        model=model,
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_prompt(source, detect_kind(source), max_cases)}],
    )
    text = "".join(getattr(block, "text", "") for block in reply.content)
    return parse_and_validate(text)
