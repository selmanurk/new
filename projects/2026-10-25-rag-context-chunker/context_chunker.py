#!/usr/bin/env python3
"""Split plain text into overlapping, RAG-ready chunks without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
WORD = re.compile(r"\S+")


def estimate_tokens(text: str) -> int:
    """A transparent rough estimate for English-like text (about 0.75 words/token)."""
    return max(1, round(len(WORD.findall(text)) / 0.75)) if text.strip() else 0


def sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_BOUNDARY.split(text.strip()) if part.strip()]


def chunk_text(text: str, max_chars: int = 1200, overlap_chars: int = 160) -> list[dict[str, object]]:
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    if overlap_chars < 0 or overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be non-negative and smaller than max_chars")

    source = " ".join(text.split())
    if not source:
        return []

    result: list[dict[str, object]] = []
    current = ""
    for sentence in sentences(source):
        if current and len(current) + 1 + len(sentence) > max_chars:
            result.append({"text": current, "characters": len(current), "estimated_tokens": estimate_tokens(current)})
            overlap = current[-overlap_chars:].lstrip() if overlap_chars else ""
            current = f"{overlap} {sentence}".strip()
        else:
            current = f"{current} {sentence}".strip()

        while len(current) > max_chars:
            piece = current[:max_chars].rsplit(" ", 1)[0] or current[:max_chars]
            result.append({"text": piece, "characters": len(piece), "estimated_tokens": estimate_tokens(piece)})
            remainder = current[len(piece):].lstrip()
            overlap = piece[-overlap_chars:].lstrip() if overlap_chars else ""
            current = f"{overlap} {remainder}".strip()

    if current:
        result.append({"text": current, "characters": len(current), "estimated_tokens": estimate_tokens(current)})

    for index, item in enumerate(result, start=1):
        item["id"] = index
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 text file to chunk")
    parser.add_argument("--max-chars", type=int, default=1200)
    parser.add_argument("--overlap-chars", type=int, default=160)
    parser.add_argument("--output", type=Path, help="Write JSON to this file instead of stdout")
    args = parser.parse_args(argv)

    try:
        text = args.input.read_text(encoding="utf-8")
        chunks = chunk_text(text, args.max_chars, args.overlap_chars)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))

    payload = {"source": str(args.input), "chunk_count": len(chunks), "chunks": chunks}
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
