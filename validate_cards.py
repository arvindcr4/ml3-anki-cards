#!/usr/bin/env python3
"""Validate an Anki tab-separated import file.

Checks that every card row has exactly two non-empty fields (front, back),
that no front is duplicated, and that the file is valid UTF-8. Lines starting
with '#' are Anki header directives / comments and are skipped.

Usage: python3 validate_cards.py [path]   (default: ml3_anki_cards.txt)
Exit status 0 when valid, 1 otherwise.
"""
import sys
from pathlib import Path

DEFAULT_FILE = Path(__file__).with_name("ml3_anki_cards.txt")


def validate(path):
    """Return (card_count, errors) for the TSV at *path*."""
    errors = []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return 0, [f"not valid UTF-8: {exc}"]

    seen = {}
    count = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            errors.append(f"line {lineno}: expected 2 fields, got {len(fields)}")
            continue
        front, back = (f.strip() for f in fields)
        if not front:
            errors.append(f"line {lineno}: empty front")
        if not back:
            errors.append(f"line {lineno}: empty back")
        if front in seen:
            errors.append(f"line {lineno}: duplicate front (first at line {seen[front]})")
        else:
            seen[front] = lineno
        count += 1

    if count == 0:
        errors.append("no cards found")
    return count, errors


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_FILE
    count, errors = validate(path)
    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    print(f"{path}: {count} cards, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
