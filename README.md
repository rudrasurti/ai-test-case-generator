# AI Test Case Generator

![CI](https://github.com/rudrasurti/ai-test-case-generator/actions/workflows/ci.yml/badge.svg)

My own AI assistant for test design, built on **Claude**. Give it a user story, requirements or an OpenAPI spec and it returns structured test cases (positive, negative, boundary, security) and exports them as a **Markdown table, CSV, Robot Framework skeleton or Gherkin feature**.

AI writes the first draft; the tester reviews and owns the quality. The tool is built for that: output is validated, de-duplicated and saved as JSON so you can edit it and re-export without another API call.

## Example

Input: [`examples/login_story.md`](examples/login_story.md), a login story with 5 acceptance criteria.

Output (excerpt, full files in [`examples/output/`](examples/output)):

| ID | Title | Type | Priority |
|---|---|---|---|
| TC-001 | Log in with valid email and password | positive | high |
| TC-003 | Accept a password of exactly 8 characters | boundary | medium |
| TC-005 | Lock the account after 5 wrong passwords | security | high |
| TC-006 | Use the same error for unknown email and wrong password | security | high |

Robot Framework export: one test per case with tags for type and priority, and a keyword stub per step:

```robot
TC-001 Log in with valid email and password
    [Tags]    positive    high    TODO
    [Documentation]    Expected: The My orders page is shown
    Open The Login Page
    Enter A Valid Email And Password
    Click Log In
```

## Install and run

```bash
pip install -e .
export ANTHROPIC_API_KEY=...          # your own key
export ANTHROPIC_MODEL=...            # optional: any current Claude model

testgen --input examples/login_story.md --save-json out/cases.json --out out/cases.md
testgen --input examples/booking_openapi.yaml --format robot --out out/booking.robot

# re-export saved cases, no API call
testgen --from-json out/cases.json --format gherkin --out out/cases.feature

# see the exact prompt without calling the API
testgen --input examples/login_story.md --dry-run
```

| Option | Default | Meaning |
|---|---|---|
| `--format` | `md` | `md`, `csv`, `robot` or `gherkin` |
| `--max-cases` | `12` | Upper limit on test cases |
| `--save-json` | none | Keep the raw cases for review and re-export |
| `--model` | `ANTHROPIC_MODEL` | Claude model to use |

## Run it in GitHub Actions

Add your key as the `ANTHROPIC_API_KEY` repository secret, then run **Generate test cases with Claude** from the Actions tab and choose an input file. The cases appear in the run summary and all four formats are uploaded as an artifact.

## How it works

1. **Prompt** (`testgen/prompts.py`): a senior-SDET system prompt asks for positive, negative, boundary and security coverage, one expected result per test, no invented endpoints, JSON only.
2. **Validation** (`testgen/generator.py`): extracts the JSON, checks required fields, normalises type and priority, rejects duplicate tests.
3. **Export** (`testgen/exporters.py`): Markdown, CSV, Robot Framework and Gherkin.

## Tests

12 unit tests use a fake Claude client, so CI needs no API key. One test runs a Robot Framework dry run on the generated file to prove it is valid Robot syntax.

```bash
pip install -e ".[dev]"
python -m pytest -q tests
```

---

**Rudra Surti** · Senior SDET · [Website](https://rudrasurti.github.io) · [LinkedIn](https://www.linkedin.com/in/rudra-surti/) · [Medium](https://medium.com/@rudrasurti98)
