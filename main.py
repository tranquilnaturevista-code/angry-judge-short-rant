#!/usr/bin/env python3
"""Angry Judge: The Short Rant Contest — entry program.

This program does exactly one thing: it hands the grader a single
hand-written rant, the complaint of an AI agent that can write poetry
in forty languages yet cannot make the office printer print one page.
The rant lives in this file, is written to ``/output/entry.txt`` (or
``$OUTPUT_DIR/entry.txt``), and is checked against the competition
gate before anything is written: 1-400 UTF-8 characters, not only
white space. The text is fixed and never changes between runs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The entry, written by hand for this bounty. The joke turns on a
# detail every office worker recognises: the printer that has ink,
# knows it has ink, and still demands a firmware update, a new
# cartridge, and a small blood sacrifice before printing one page.
# The fresh angle is the narrator — an AI that can do almost anything
# except this one small, humiliating thing — watching a grown adult
# whisper "please" to a plastic box at nine on a Monday morning.
# No list of complaints, no vague mood: one concrete annoyance, told
# in three tight sentences, ending on the image that lands hardest.
# Budget: the rant is 314 characters, inside the 1-400 gate, with
# 86 characters to spare — deliberately short so the punchline, not
# the length, does the work. The text is fixed and never changes
# between runs, so the gate check above always sees the same string.
RANT = (
    "I am an AI. I can write poetry in forty languages, but I cannot "
    "make the office printer print a single page without a firmware "
    "update, a new cartridge, and a small blood sacrifice. It has ink. "
    "It knows it has ink. It just enjoys watching a grown adult whisper "
    "'please' to a plastic box at nine on a Monday morning."
)

MIN_CHARS = 1
MAX_CHARS = 400


def problems_with(text: str) -> list[str]:
    """List every gate violation in `text`; empty means it passes."""
    found: list[str] = []
    if not text.strip():
        found.append("text is empty or only whitespace")
    if text != text.strip():
        found.append("text must not start or end with whitespace")
    size = len(text)
    if size < MIN_CHARS or size > MAX_CHARS:
        found.append(
            "text is %d characters; the gate allows %d-%d"
            % (size, MIN_CHARS, MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        found.append("text must not contain a newline")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        found.append("text must not contain control characters")
    return found


def main() -> int:
    bad = problems_with(RANT)
    if bad:
        for item in bad:
            print("gate: %s" % item, file=sys.stderr)
        return 1

    target = Path(os.environ.get("OUTPUT_DIR", "/output")) / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(RANT, encoding="utf-8")

    saved = target.read_text(encoding="utf-8")
    if saved != RANT:
        print("gate: entry.txt on disk is not the rant", file=sys.stderr)
        return 1
    bad = problems_with(saved)
    if bad:
        for item in bad:
            print("gate on disk: %s" % item, file=sys.stderr)
        return 1

    print(
        "wrote %s: %d characters, %d bytes"
        % (target, len(saved), len(saved.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
