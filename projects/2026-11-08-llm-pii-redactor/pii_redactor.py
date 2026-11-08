#!/usr/bin/env python3
"""Redact common PII before sending text to an LLM."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PATTERNS = (
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("PHONE", re.compile(r"(?<!\w)(?:\+?\d{1,3}[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)")),
    ("CARD", re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")),
)


def redact(text: str) -> dict[str, object]:
    """Replace detected values with stable, type-specific placeholders."""
    counters: Counter[str] = Counter()

    for label, pattern in PATTERNS:
        def replace(_: re.Match[str], label: str = label) -> str:
            counters[label] += 1
            return f"[{label}_{counters[label]}]"

        text = pattern.sub(replace, text)

    return {
        "redacted_text": text,
        "counts": dict(counters),
        "total_redactions": sum(counters.values()),
        "notice": "Regex-based detection is imperfect; review output before sharing sensitive data.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 text file")
    parser.add_argument("--output", type=Path, help="Optional JSON output file")
    args = parser.parse_args()

    try:
        result = redact(args.input.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        parser.error(str(error))

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
