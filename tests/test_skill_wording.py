#!/usr/bin/env python3
"""Contract tests: SKILL.md wording guarantees (the unbreakable-clause pins)."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "skills"
BP = ROOT / "qt-best-practices" / "SKILL.md"
RV = ROOT / "qt-review" / "SKILL.md"


def bp_body() -> str:
    return BP.read_text(encoding="utf-8")


def rv_body() -> str:
    return RV.read_text(encoding="utf-8")


class BestPractices(unittest.TestCase):
    def test_unbreakable_clause_present(self):
        body = bp_body()
        self.assertIn("The contracts below are **unbreakable and non-waivable**", body)
        self.assertIn("developers cannot opt out, and neither can you", body)

    def test_silencing_prohibition_names_the_tokens(self):
        body = bp_body()
        self.assertIn("never to weaken or delete the lints", body)
        self.assertIn("re-cut the layout", body)
        self.assertIn("NOLINT", body)
        self.assertIn("clang-tidy", body)

    def test_points_at_review_as_the_critic(self):
        body = bp_body()
        self.assertIn("Review treats a broken contract as an automatic Must fix", body)
        self.assertIn("`qt-review`", body)

    def test_names_the_layer_walls(self):
        body = bp_body()
        for phrase in ("GUI thread", "QObject", "platform/", "Result<T>"):
            self.assertIn(phrase, body)


class ReviewSkill(unittest.TestCase):
    def test_architecture_category_ranks_first_as_must_fix(self):
        body = rv_body()
        self.assertIn("Architecture contracts (always Must fix, ranked first)", body)
        self.assertIn("broken architecture contract (ranked above everything)", body)

    def test_waiver_detection_clause(self):
        body = rv_body()
        self.assertIn("Waived gates", body)
        self.assertIn("flag the deletion itself, loudly", body)
        self.assertIn("NOLINT", body)
        self.assertIn("clang-tidy", body)


if __name__ == "__main__":
    unittest.main()
