"""A tiny word-count program, the sample project for this guide's
Dagger module. It counts lines, words and characters in a text
file, in the spirit of the Unix `wc` tool, small enough to check
by eye.
"""

import sys


def count(text: str) -> tuple[int, int, int]:
    """Return (lines, words, characters) for a block of text."""
    lines = text.count("\n")
    words = len(text.split())
    chars = len(text)
    return lines, words, chars


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: wordcount.py FILE", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        lines, words, chars = count(f.read())
    print(f"{lines} {words} {chars} {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
