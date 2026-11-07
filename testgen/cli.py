import argparse
import json
import pathlib
import sys

from .exporters import EXPORTERS
from .generator import DEFAULT_MODEL, generate, parse_and_validate
from .prompts import SYSTEM, user_prompt
from .generator import detect_kind


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="testgen", description="Generate test cases with Claude.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="User story, requirements or OpenAPI file")
    src.add_argument("--from-json", help="Re-export test cases saved earlier as JSON (no API call)")
    ap.add_argument("--format", choices=sorted(EXPORTERS), default="md")
    ap.add_argument("--out", help="Write output to this file (default: print)")
    ap.add_argument("--save-json", help="Also save the raw test cases as JSON")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-cases", type=int, default=12)
    ap.add_argument("--dry-run", action="store_true", help="Print the prompt only; no API call")
    args = ap.parse_args(argv)

    if args.from_json:
        data = parse_and_validate(pathlib.Path(args.from_json).read_text())
    else:
        source = pathlib.Path(args.input).read_text()
        if args.dry_run:
            print("--- system ---\n" + SYSTEM + "\n--- user ---\n" + user_prompt(source, detect_kind(source), args.max_cases))
            return 0
        data = generate(source, model=args.model, max_cases=args.max_cases)

    if args.save_json:
        pathlib.Path(args.save_json).write_text(json.dumps(data, indent=2))
    output = EXPORTERS[args.format](data)
    if args.out:
        pathlib.Path(args.out).write_text(output)
        print(f"Wrote {len(data['test_cases'])} test cases to {args.out}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
