#!/usr/bin/env python3
"""Check that every C++ code block in the skills and docs is structurally sane.

A full compile needs Qt and a build; this pass is the offline gate that runs
everywhere: it strips comments and literals and verifies that braces, brackets
and parentheses balance in each ```cpp block. `scripts/check-build.sh` compiles
the runnable example when Qt is available; the two together are the example
gate.

Stdlib only, Python 3.9+. Exit 1 on any imbalance.
"""

from __future__ import annotations

import sys
from pathlib import Path

DOC_GLOBS = (
    "README.md",
    "CONTRIBUTING.md",
    "examples/*.md",
    "skills/*/SKILL.md",
    "skills/*/references/*.md",
    "skills/*/references/**/*.md",
)
CPP_LANGS = {"cpp", "c++", "cc", "cxx"}


def doc_files(root: Path):
    found = set()
    for pattern in DOC_GLOBS:
        for path in root.glob(pattern):
            if path.is_file() and "evals" not in path.parts:
                found.add(path)
    return sorted(found)


def cpp_blocks(text: str):
    """Yield (start_line, code) for each cpp/c++ fenced block."""
    fence = None
    lang = ""
    start = 0
    body = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if fence is None:
            if stripped.startswith("```"):
                fence = "```"
                lang = stripped[3:].strip().split(",")[0].lower()
                start = number + 1
                body = []
            continue
        if stripped.startswith("```") and not stripped[3:].strip():
            if lang in CPP_LANGS:
                yield start, "\n".join(body)
            fence = None
            continue
        body.append(line)


def check_balance(code: str):
    """Return (line_offset, message) or None. Comments/literals are skipped."""
    pairs = {"(": ")", "[": "]", "{": "}"}
    closers = {v: k for k, v in pairs.items()}
    stack = []
    i = 0
    quote = None
    line = 1
    while i < len(code):
        ch = code[i]
        nxt = code[i + 1] if i + 1 < len(code) else ""
        if ch == "\n":
            line += 1
            i += 1
            continue
        if quote is not None:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch == "/" and nxt == "/":
            end = code.find("\n", i)
            i = len(code) if end == -1 else end
            continue
        if ch == "/" and nxt == "*":
            end = code.find("*/", i + 2)
            if end == -1:
                return line, "unterminated block comment"
            line += code[i:end].count("\n")
            i = end + 2
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            continue
        if ch in pairs:
            stack.append((ch, line))
        elif ch in closers:
            if not stack or stack[-1][0] != closers[ch]:
                return line, "unexpected %r" % ch
            stack.pop()
        i += 1
    if quote is not None:
        return line, "unterminated string"
    if stack:
        opener, open_line = stack[-1]
        return open_line, "unclosed %r" % opener
    return None


def check_repo(root: Path):
    problems = []
    checked = 0
    for path in doc_files(root):
        text = path.read_text(encoding="utf-8")
        for start, code in cpp_blocks(text):
            checked += 1
            result = check_balance(code)
            if result:
                offset, message = result
                problems.append((path.relative_to(root).as_posix(), start + offset - 1, message))
    return problems, checked


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    problems, checked = check_repo(root)
    for path, line, message in problems:
        print("%s:%d: %s" % (path, line, message))
    errors = len(problems)
    print("%d error%s, %d cpp blocks checked" % (errors, "" if errors == 1 else "s", checked))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
