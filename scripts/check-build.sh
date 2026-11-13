#!/usr/bin/env bash
# check-build.sh — compile and test the runnable Qt example.
# A missing Qt is a visible SKIP, never a silent pass; CI installs Qt and runs
# the same script.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v cmake >/dev/null 2>&1; then
  echo "check-build: SKIP — cmake not found"
  exit 0
fi

if ! pkg-config --exists Qt6Core 2>/dev/null && ! ls /usr/lib/*/cmake/Qt6 >/dev/null 2>&1; then
  echo "check-build: SKIP — Qt6 development files not found"
  exit 0
fi

BUILD="${TMPDIR:-/tmp}/beautifulqt-build"
cmake -S examples/minimal -B "$BUILD" -DCMAKE_BUILD_TYPE=Release
cmake --build "$BUILD" --parallel
ctest --test-dir "$BUILD" --output-on-failure
echo "check-build: OK"
