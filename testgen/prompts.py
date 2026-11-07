SYSTEM = """You are a senior SDET. Design test cases the way an expert tester would:
- cover positive, negative, boundary, security and (where relevant) performance cases
- one clear expected result per test
- no duplicate tests; prefer fewer, sharper tests
- use only facts from the input; never invent endpoints or fields

Return ONLY valid JSON, no prose, in this shape:
{"feature": "<short name>",
 "test_cases": [
   {"id": "TC-001", "title": "<imperative title>",
    "type": "positive|negative|boundary|security|performance",
    "priority": "high|medium|low",
    "preconditions": "<text or empty>",
    "steps": ["<step>", "..."],
    "expected": "<single expected result>"}
 ]}"""


def user_prompt(source: str, kind: str, max_cases: int) -> str:
    return (
        f"Input type: {kind}\n"
        f"Write at most {max_cases} test cases.\n\n"
        f"<input>\n{source.strip()}\n</input>"
    )
