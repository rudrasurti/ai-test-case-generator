import csv
import io
import re


def to_markdown(data: dict) -> str:
    lines = [f"# Test cases: {data['feature']}", "",
             "| ID | Title | Type | Priority | Steps | Expected |", "|---|---|---|---|---|---|"]
    for tc in data["test_cases"]:
        steps = "<br>".join(f"{i}. {s}" for i, s in enumerate(tc["steps"], 1))
        lines.append(f"| {tc['id']} | {tc['title']} | {tc['type']} | {tc['priority']} | {steps} | {tc['expected']} |")
    return "\n".join(lines) + "\n"


def to_csv(data: dict) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["ID", "Title", "Type", "Priority", "Preconditions", "Steps", "Expected"])
    for tc in data["test_cases"]:
        w.writerow([tc["id"], tc["title"], tc["type"], tc["priority"], tc["preconditions"],
                    " | ".join(tc["steps"]), tc["expected"]])
    return out.getvalue()


def _keyword(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9 ]", "", text).strip().title() or "Step"


def to_robot(data: dict) -> str:
    """Robot Framework skeleton: one test per case, steps as keywords to implement."""
    lines = ["*** Settings ***", f"Documentation    Generated test cases for {data['feature']}.",
             "...              Implement each keyword, then remove the TODO tag.", "",
             "*** Test Cases ***"]
    keywords = {}
    for tc in data["test_cases"]:
        lines.append(f"{tc['id']} {tc['title']}")
        lines.append(f"    [Tags]    {tc['type']}    {tc['priority']}    TODO")
        lines.append(f"    [Documentation]    Expected: {tc['expected']}")
        for step in tc["steps"]:
            kw = _keyword(step)
            keywords[kw] = step
            lines.append(f"    {kw}")
        lines.append("")
    lines.append("*** Keywords ***")
    for kw, step in keywords.items():
        lines += [kw, f"    Fail    Not implemented: {step}", ""]
    return "\n".join(lines)


def to_gherkin(data: dict) -> str:
    lines = [f"Feature: {data['feature']}", ""]
    for tc in data["test_cases"]:
        lines.append(f"  @{tc['type']} @{tc['priority']}")
        lines.append(f"  Scenario: {tc['id']} {tc['title']}")
        if tc["preconditions"]:
            lines.append(f"    Given {tc['preconditions']}")
        for i, step in enumerate(tc["steps"]):
            word = "When" if i == 0 else "And"
            lines.append(f"    {word} {step}")
        lines.append(f"    Then {tc['expected']}")
        lines.append("")
    return "\n".join(lines)


EXPORTERS = {"md": to_markdown, "csv": to_csv, "robot": to_robot, "gherkin": to_gherkin}
