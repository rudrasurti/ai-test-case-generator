import json
import pathlib
import types

import pytest

from testgen import cli
from testgen.exporters import EXPORTERS
from testgen.generator import GenerationError, detect_kind, generate, parse_and_validate

ROOT = pathlib.Path(__file__).resolve().parents[1]
SAMPLE = (ROOT / "examples" / "login_test_cases.json").read_text()


class FakeClient:
    """Stands in for anthropic.Anthropic so tests need no API key."""

    def __init__(self, reply):
        self.reply, self.calls = reply, []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return types.SimpleNamespace(content=[types.SimpleNamespace(text=self.reply)])


def test_generate_parses_reply_in_code_fence():
    client = FakeClient("```json\n" + SAMPLE + "\n```")
    data = generate("story", client=client, model="test-model", max_cases=6)
    assert len(data["test_cases"]) == 6
    call = client.calls[0]
    assert call["model"] == "test-model" and "senior SDET" in call["system"]
    assert "at most 6 test cases" in call["messages"][0]["content"]


def test_detects_openapi_input():
    assert detect_kind((ROOT / "examples" / "booking_openapi.yaml").read_text()) == "OpenAPI specification"
    assert detect_kind("As a user I want...") == "User story / requirements"


def test_rejects_reply_without_json():
    with pytest.raises(GenerationError):
        parse_and_validate("Sorry, I cannot help with that.")


def test_rejects_missing_fields_and_duplicates():
    with pytest.raises(GenerationError, match="missing 'expected'"):
        parse_and_validate(json.dumps({"test_cases": [{"title": "a", "type": "positive", "priority": "high", "steps": []}]}))
    tc = {"title": "Same", "type": "positive", "priority": "high", "steps": ["x"], "expected": "y"}
    with pytest.raises(GenerationError, match="Duplicate"):
        parse_and_validate(json.dumps({"test_cases": [tc, dict(tc)]}))


def test_normalises_unknown_type_and_priority():
    tc = {"title": "t", "type": "Weird", "priority": "URGENT", "steps": ["s"], "expected": "e"}
    data = parse_and_validate(json.dumps({"test_cases": [tc]}))
    assert data["test_cases"][0]["type"] == "positive"
    assert data["test_cases"][0]["priority"] == "medium"
    assert data["test_cases"][0]["id"] == "TC-001"


@pytest.mark.parametrize("fmt,needle", [("md", "| TC-005 |"), ("csv", "TC-006,"),
                                        ("robot", "*** Test Cases ***"), ("gherkin", "Scenario: TC-001")])
def test_exporters(fmt, needle):
    assert needle in EXPORTERS[fmt](parse_and_validate(SAMPLE))


def test_robot_export_is_valid_robot(tmp_path):
    robot = pytest.importorskip("robot")
    path = tmp_path / "gen.robot"
    path.write_text(EXPORTERS["robot"](parse_and_validate(SAMPLE)))
    rc = robot.run(str(path), dryrun=True, output=None, report=None, log=None, stdout=None)
    assert rc == 0


def test_cli_from_json_writes_file(tmp_path):
    out = tmp_path / "cases.feature"
    assert cli.main(["--from-json", str(ROOT / "examples" / "login_test_cases.json"), "--format", "gherkin", "--out", str(out)]) == 0
    assert "Feature: Login" in out.read_text()


def test_cli_dry_run_prints_prompt(capsys):
    assert cli.main(["--input", str(ROOT / "examples" / "login_story.md"), "--dry-run"]) == 0
    assert "locked for 15 minutes" in capsys.readouterr().out
