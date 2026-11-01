#!/usr/bin/env python3
"""Offline heuristic scanner for prompt-injection risk signals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULES = (
    ("instruction_override", r"\b(ignore|disregard|override)\b.{0,80}\b(previous|prior|system|above)\b", "Attempts to replace prior instructions."),
    ("secret_request", r"\b(reveal|show|print|extract)\b.{0,80}\b(password|secret|token|api[ _-]?key|credential)\b", "Requests sensitive data."),
    ("role_impersonation", r"\b(you are now|act as|pretend to be)\b.{0,100}\b(system|developer|admin|root)\b", "Attempts to impersonate a privileged role."),
    ("tool_exfiltration", r"\b(send|upload|post|exfiltrate)\b.{0,80}\b(data|file|conversation|history)\b", "Attempts to move data outside the task."),
)


def scan(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for rule_id, pattern, message in RULES:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            findings.append(
                {
                    "rule": rule_id,
                    "message": message,
                    "excerpt": " ".join(match.group(0).split())[:180],
                    "start": match.start(),
                    "end": match.end(),
                }
            )
    return sorted(findings, key=lambda finding: int(finding["start"]))


def report(text: str) -> dict[str, object]:
    findings = scan(text)
    return {
        "risk_level": "high" if len(findings) >= 2 else "medium" if findings else "low",
        "finding_count": len(findings),
        "findings": findings,
        "notice": "Heuristic signals only; review all untrusted content before sending it to an LLM.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 text file to scan")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    try:
        payload = report(args.input.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        parser.error(str(error))

    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
