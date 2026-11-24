#!/usr/bin/env python3
"""Ship It Friday - writes one commit message to /output/entry.txt.

The entry is the funniest git commit message an AI coding agent writes in
the moment before it breaks production on a Friday: the agent's total
confidence, stated one deploy before everything breaks. Deterministic: no
randomness, no network, no clock. The line is written exactly, with no
trailing newline.
"""

import os

LINE = "fix: I have read the entire codebase and I am confident this Friday deploy will not break production"

# Conventional-commit prefixes a real commit message starts with.
COMMIT_PREFIXES = ("fix:", "feat:", "ship:", "chore:", "refactor:", "wip:")

# Gate limits from the brief: UTF-8 text of 1 to 159 characters,
# not only white space.
MIN_LENGTH = 1
MAX_LENGTH = 159


def validate(line: str) -> None:
    if not line:
        raise SystemExit("Invalid line: entry must be non-empty.")
    if not (MIN_LENGTH <= len(line) <= MAX_LENGTH):
        raise SystemExit(
            f"Invalid line: entry must be {MIN_LENGTH} to {MAX_LENGTH} "
            f"characters long (got {len(line)})."
        )
    if not line.strip():
        raise SystemExit("Invalid line: entry must not be only white space.")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise SystemExit(
            "Invalid line: entry must not contain control characters."
        )
    if line != line.strip():
        raise SystemExit(
            "Invalid line: entry must not have leading or trailing whitespace."
        )
    if "\n" in line or "\r" in line:
        raise SystemExit(
            "Invalid line: entry must be a single line with no newline characters."
        )
    if not any(line.startswith(prefix) for prefix in COMMIT_PREFIXES):
        raise SystemExit(
            "Invalid line: entry must read like a commit message "
            "(start with a conventional prefix such as 'fix:')."
        )
    if "Friday" not in line or "production" not in line:
        raise SystemExit(
            "Invalid line: entry must name the Friday deploy and production."
        )


def write_entry(line: str, output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(output_path, encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise SystemExit(
            "Write verification failed: entry file content does not match the line."
        )


def main() -> None:
    validate(LINE)
    output_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    write_entry(LINE, output_path)


if __name__ == "__main__":
    main()
