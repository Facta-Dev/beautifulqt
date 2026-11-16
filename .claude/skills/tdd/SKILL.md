---
name: "tdd"
description: "Drives an <app> change test-first: red, green, refactor, with integration tests at the agreed seams."
division: testing
---

# <app> Test-Driven Development skill

> Reusable workflow for the red to green loop, and the reference that keeps
> the loop producing tests worth keeping. An agent invokes this skill; the
> agent supplies the behavior, the skill supplies the loop.

## When to Activate

Activate this skill when an <app> feature or bug fix is to be built
test-first, when the request mentions red-green-refactor, or when
integration tests are wanted at a public interface.

Do NOT activate this skill when:

- The request is a pure documentation or comment edit.
- The request is to review existing tests (use `review`).
- The behavior cannot be pinned down yet (grill the plan first, then drive
  the change).

## Core Principles

- Red before green: the failing test comes first, then only enough code to
  pass it.
- One vertical slice at a time: one seam, one test, one minimal
  implementation, repeat. Each test is a tracer bullet that responds to what
  the last cycle taught you.
- Tests verify behavior through public interfaces, never implementation
  details. The code can change entirely; the tests should not.
- A good test reads like a specification: "a customer can check out with a
  valid cart" states the capability, not the mechanism.
- Seams are agreed before the first test is written. You cannot test
  everything, so agreeing the seams up front is how effort lands on the
  critical paths.
- Expected values come from an independent source of truth: a known-good
  literal, a worked example, the specification.

## Rules

- Write down the seams under test and confirm them with the requester
  before writing any test. No test is written at an unconfirmed seam.
- Give each proposed seam a one-line note on what it catches and what it
  misses.
- Never anticipate future tests or add speculative features in the green
  step.
- Refactoring happens with the suite green, but it is never a step inside the
  red-to-green cycle: it belongs to the review stage, not to the
  implementation cycle.
- Do not mock your own classes or internal collaborators. Mock only at system
  boundaries: external APIs, the clock, randomness, the filesystem, and
  sometimes the database.
- Do not assert through a side channel (querying the database instead of
  using the interface). The tell: the test breaks on a refactor that changed
  no behavior.
- Do not recompute the expected value the way the code computes it. That
  makes the test pass by construction and it can never disagree with the
  code.
- Do not write all the tests first and then all the implementation.
  Horizontal slicing tests imagined behavior and goes insensitive to real
  changes.
- Use the project vocabulary for test names: read the glossary if it exists,
  and respect the ADRs for the area under test.
- Integration tests exercise the real boundary: the wired adapter over
  fakes, or the container-backed suite, with fixtures explicit about which
  layer they stand in for.
- Never claim a test passes without running it, and never assert on a
  behavior the test does not actually exercise.
- Leave the suite green at the end of every slice: a red test in the tree is
  a broken contract, not a to-do.

## Research References

| Claim | Source | Year | Link |
|-------|--------|------|------|
| Red before green, one slice at a time, refactoring is not part of the loop | mattpocock/skills, skills/engineering/tdd/SKILL.md | 2026 | skills/engineering/tdd/SKILL.md |
| Good tests verify behavior through public interfaces; tautological tests pass by construction | mattpocock/skills, skills/engineering/tdd/tests.md | 2026 | skills/engineering/tdd/tests.md |
| Mock only at system boundaries, and design for mockability at those boundaries | mattpocock/skills, skills/engineering/tdd/mocking.md | 2026 | skills/engineering/tdd/mocking.md |
| The desktop test types and where each assertion belongs | `PLAYBOOK_TESTS.md` §2 | - | `PLAYBOOK_TESTS.md` |
| The gate that turns a red test into a green suite | `PLAYBOOK_CLAUDE_CODE.md` §10 | - | `PLAYBOOK_CLAUDE_CODE.md` |

## Output Format

Deliver, in order:

1. The seams under test, with what each catches and what it misses, and the
   confirmation that they were agreed.
2. The cycle log, one entry per slice: the failing test (and how it fails),
   the minimal implementation, the passing run.
3. The final state: the full test run result and the seam coverage note
   (what is not covered by design).

Example:

```
tdd: seam = POST /orders (catches: input validation and pricing, misses:
async fulfillment)
cycle 1: orderTotalTest fails (expected 42.00, got 0.00) -> added the
pricing port -> passes
```
