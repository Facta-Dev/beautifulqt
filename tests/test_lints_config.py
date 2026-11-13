#!/usr/bin/env python3
"""Contract tests: the drop-in clang-tidy/clang-format config stays paired."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TIDY = REPO_ROOT / "lints" / ".clang-tidy"
FORMAT = REPO_ROOT / "lints" / ".clang-format"


class TidyConfig(unittest.TestCase):
    def setUp(self):
        self.text = TIDY.read_text(encoding="utf-8")

    def test_check_groups_are_pinned(self):
        for group in ("bugprone-*", "performance-*", "modernize-*", "readability-*", "cppcoreguidelines-*", "qt-*"):
            self.assertIn(group, self.text)

    def test_warnings_are_errors(self):
        self.assertIn("WarningsAsErrors: '*'", self.text)

    def test_naming_conventions_are_present(self):
        self.assertIn("readability-identifier-naming.PrivateMemberPrefix", self.text)

    def test_no_blanket_silence(self):
        active = [
            line.strip()
            for line in self.text.splitlines()
            if line.strip().startswith("WarningsAsErrors:")
        ]
        self.assertEqual(active, ["WarningsAsErrors: '*'"], "the active setting must keep warnings as errors")


class FormatConfig(unittest.TestCase):
    def test_format_file_exists_and_pins_the_style(self):
        text = FORMAT.read_text(encoding="utf-8")
        self.assertIn("BasedOnStyle:", text)
        self.assertIn("ColumnLimit:", text)
        self.assertIn("Standard: c++20", text)


if __name__ == "__main__":
    unittest.main()
