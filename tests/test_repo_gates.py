#!/usr/bin/env python3
"""Gate tests: the repository's own validators must pass."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(*command: str) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)


class Gates(unittest.TestCase):
    def test_skill_validator_passes(self):
        result = run(sys.executable, "scripts/check-skill.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_examples_are_balanced(self):
        result = run(sys.executable, "scripts/check-examples.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless(shutil.which("cmake") and shutil.which("pkg-config"), "cmake/pkg-config not installed")
class BuildGate(unittest.TestCase):
    def test_example_builds_when_qt_is_present(self):
        has_qt = run("pkg-config", "--exists", "Qt6Core").returncode == 0
        if not has_qt:
            self.skipTest("Qt6 development files not found")
        result = run("bash", "scripts/check-build.sh")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
