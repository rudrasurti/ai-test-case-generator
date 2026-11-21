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


def _one_line(text) -> str:
    return " ".join(str(text).split())


def _ts_string(text) -> str:
    return _one_line(text).replace("\\", "\\\\").replace("'", "\\'")


def to_playwright(data: dict) -> str:
    """Playwright (TypeScript) skeleton: one test per case, steps as comments to implement."""
    feature = _ts_string(data["feature"])
    lines = ["import { test, expect } from '@playwright/test';", "",
             f"// Generated test cases for {_one_line(data['feature'])}.",
             "// Each test is marked fixme: implement the steps, then change test.fixme to test.", "",
             f"test.describe('{feature}', () => {{"]
    for tc in data["test_cases"]:
        title = _ts_string(f"{tc['id']} {tc['title']}")
        lines.append(f"  test.fixme('{title}', {{ tag: ['@{tc['type']}', '@{tc['priority']}'] }}, async ({{ page }}) => {{")
        if tc["preconditions"]:
            lines.append(f"    // Given: {_one_line(tc['preconditions'])}")
        lines.append("    await page.goto('/'); // TODO: open the start page")
        for i, step in enumerate(tc["steps"], 1):
            lines.append(f"    // Step {i}: {_one_line(step)}")
        lines.append(f"    // Expected: {_one_line(tc['expected'])}")
        lines.append("    // await expect(page.getByRole(...)).toBeVisible();")
        lines.append("  });")
        lines.append("")
    lines.append("});")
    return "\n".join(lines) + "\n"


def _pascal(text) -> str:
    words = re.findall(r"[A-Za-z0-9]+", str(text))
    return "".join(w[:1].upper() + w[1:] for w in words)


def _java_string(text) -> str:
    return _one_line(text).replace("\\", "\\\\").replace('"', '\\"')


def _java_tests(data: dict, driver_import: str, driver_decl: str) -> str:
    cls = (_pascal(data["feature"]) or "Generated") + "Test"
    if cls[0].isdigit():
        cls = "Test" + cls
    lines = ["import org.testng.SkipException;", "import org.testng.annotations.Test;", driver_import, "",
             f"// Generated test cases for {_one_line(data['feature'])}.",
             "// Implement each test, then remove the SkipException.", "",
             f"public class {cls} {{", f"    {driver_decl}", ""]
    for tc in data["test_cases"]:
        method = "test" + re.sub(r"[^A-Za-z0-9]", "", str(tc["id"])) + _pascal(tc["title"])
        lines.append(f"    @Test(groups = {{\"{tc['type']}\", \"{tc['priority']}\"}}, "
                     f"description = \"{_java_string(tc['id'] + ' ' + tc['title'])}\")")
        lines.append(f"    public void {method}() {{")
        if tc["preconditions"]:
            lines.append(f"        // Given: {_one_line(tc['preconditions'])}")
        for i, step in enumerate(tc["steps"], 1):
            lines.append(f"        // Step {i}: {_one_line(step)}")
        lines.append(f"        // Expected: {_one_line(tc['expected'])}")
        lines.append('        throw new SkipException("TODO: implement this test");')
        lines.append("    }")
        lines.append("")
    lines.append("}")
    return "\n".join(lines) + "\n"


def to_selenium(data: dict) -> str:
    """Selenium (Java, TestNG) skeleton: one test method per case, steps as comments."""
    return _java_tests(data, "import org.openqa.selenium.WebDriver;",
                       "private WebDriver driver; // TODO: create it in a @BeforeMethod")


def to_appium(data: dict) -> str:
    """Appium (Java, TestNG) skeleton: one test method per case, steps as comments."""
    return _java_tests(data, "import io.appium.java_client.AppiumDriver;",
                       "private AppiumDriver driver; // TODO: create it in a @BeforeMethod")


EXPORTERS = {"md": to_markdown, "csv": to_csv, "robot": to_robot, "gherkin": to_gherkin, "playwright": to_playwright,
             "selenium": to_selenium, "appium": to_appium}
