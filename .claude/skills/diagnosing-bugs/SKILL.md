---
name: "diagnosing-bugs"
description: "Diagnoses a hard bug or performance regression in <app> by building a red-capable feedback loop first, then minimising, ranking hypotheses, instrumenting one variable at a time and fixing the root cause."
division: testing
---

# <app> Diagnosing Bugs skill

> Reusable workflow for finding the cause of a hard bug or performance
> regression. An agent invokes this skill; the requester supplies the
> symptom, the skill supplies the loop.

## When to Activate

Activate this skill when something in <app> is broken and the cause is not
already visible: a stack trace nobody has read, a wrong value, a test that
fails for no clear reason, a request that takes too long, a regression that
appeared between two known states.

Do NOT activate this skill when:

- The cause is known and the task is the fix (go straight to the change).
- The request is feature work rather than a defect (use `plan`).
- The request is to review a diff (use `review`).

## Core Principles

- The feedback loop is the skill. A tight pass/fail signal that goes red on
  THIS bug is what finds the cause; staring at code is not.
- Red before theory. No hypothesis is allowed before one command exists that
  can fail on this exact symptom, and that command has been run at least
  once.
- Minimise, then hypothesise. A minimal repro shrinks the suspect set and
  becomes the regression test.
- Hypotheses come as a ranked list of three to five, each stating the
  prediction it makes. A hypothesis with no prediction is a vibe.
- One variable per probe. Each probe maps to one stated prediction.
- Fix the root cause where all callers route through it, not the path the
  report happened to name.
- Measure first for performance work: a baseline before a change, a bisect
  before a guess.
- Redact secrets before showing commands, output or captured artifacts.

## Rules

- The loop must be red-capable (it asserts the requester's exact symptom,
  not "did not crash"), deterministic, fast (seconds, not minutes) and
  agent-runnable. Show the invocation and its output before moving on.
- If the bug is non-deterministic, raise the reproduction rate (loop the
  trigger, parallelise, narrow the timing window, add stress) until it is
  debuggable. A one-percent flake is not a loop.
- Minimise by cutting inputs, callers, config and data one at a time,
  re-running after each cut. Every remaining element must be load-bearing:
  removing any one of them turns the loop green.
- List the ranked hypotheses and show them to the requester before testing.
  Proceed with the ranking if the requester is away.
- Change one variable at a time. Never "log everything and grep".
- Tag every debug log with a unique prefix so cleanup is one grep.
- Write the regression test before the fix, and only at a seam that
  exercises the real bug pattern. If no such seam exists, that absence is
  the finding: report it instead of writing a shallow test.
- After applying the fix, re-run the original, un-minimised scenario.
  Never claim a fix works without a passing run of the original loop.
- If no loop can be built, stop and say so: list what was tried and ask for
  access to a reproducing environment, a redacted capture, or permission to
  add temporary instrumentation. Do not hypothesise without a loop.
- Redact every secret in the commands, outputs and artifacts shown: replace
  it in place and quote only the lines that carry the signal.
- State the confirmed cause in the commit message, so the next debugger
  starts from the truth.

## Research References

| Claim | Source | Year | Link |
|-------|--------|------|------|
| The red-loop sequence: feedback loop, minimise, hypothesise, instrument, fix, cleanup | mattpocock/skills, skills/engineering/diagnosing-bugs/SKILL.md | 2026 | skills/engineering/diagnosing-bugs/SKILL.md |
| A seam must exercise the real bug pattern or the regression test gives false confidence | mattpocock/skills, skills/engineering/diagnosing-bugs/SKILL.md | 2026 | skills/engineering/diagnosing-bugs/SKILL.md |
| The gate ladder that has to be green before a change lands | `PLAYBOOK_TESTS.md` | - | `PLAYBOOK_TESTS.md` |
| Secrets never enter the repository, the logs or the settings files | `PLAYBOOK_SECURITY.md` | - | `PLAYBOOK_SECURITY.md` |

## Output Format

Deliver, in order:

1. The feedback loop: the exact command, its redacted output, and why it is
   red-capable for this symptom.
2. The minimised repro: the smallest scenario that still goes red.
3. The ranked hypotheses, each with its prediction.
4. The probe results, one variable per probe, and which hypothesis was
   confirmed or eliminated.
5. The root cause in one sentence, then the fix.
6. The regression test at the chosen seam, or the missing-seam finding.
7. The cleanup status: original repro green, regression test green, debug
   instrumentation removed.

Example:

```
diagnosing-bugs: loop = `ctest -R note_sync --output-on-failure`
(red: expected 1 sync call, got 0) | hypothesis 1 confirmed | fix: the sync
port dispatches on the committed event, not the request | regression test
added at the use-case seam
```
