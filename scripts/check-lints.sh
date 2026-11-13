#!/usr/bin/env bash
# check-lints.sh — prove the drop-in clang-format/clang-tidy config.
# The clean control must stay quiet; the violation harness must fire.
# A missing tool is a visible SKIP, never a silent pass; CI installs the tools
# and runs the same script.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

have() { command -v "$1" >/dev/null 2>&1; }

FORMAT_FILES=(
  examples/minimal/main.cpp
  examples/minimal/viewmodel.h
  examples/minimal/viewmodel.cpp
  examples/minimal/test_viewmodel.cpp
  lints/check/clean.cpp
  lints/check/violations.cpp
)

if have clang-format; then
  echo "check-lints: clang-format --dry-run --Werror"
  clang-format --dry-run --Werror "${FORMAT_FILES[@]}"
else
  echo "check-lints: SKIP clang-format — not installed (CI runs it)"
fi

if ! have clang-tidy; then
  echo "check-lints: SKIP clang-tidy — not installed (CI runs it)"
  exit 0
fi

BUILD="${TMPDIR:-/tmp}/beautifulqt-check"
cmake -S examples/minimal -B "$BUILD" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON >/dev/null

echo "check-lints: clang-tidy must stay quiet on the clean control"
CLEAN_OUT="$(clang-tidy -p "$BUILD" lints/check/clean.cpp 2>&1 || true)"
if printf '%s\n' "$CLEAN_OUT" | grep -qE '(warning|error):'; then
  printf '%s\n' "$CLEAN_OUT" >&2
  echo "check-lints: FAIL — the clean control reported a finding" >&2
  exit 1
fi

echo "check-lints: clang-tidy must fire on the violation harness"
VIOL_OUT="$(clang-tidy -p "$BUILD" lints/check/violations.cpp 2>&1 || true)"
if ! printf '%s\n' "$VIOL_OUT" | grep -qE '(warning|error):'; then
  echo "check-lints: FAIL — the violation harness stayed quiet" >&2
  exit 1
fi

echo "check-lints: OK"
