---
name: diagnosing-bugs
description: "Delegate to the diagnosing-bugs skill: diagnose a hard bug or performance regression in <app> with the red-loop, minimise, hypothesise, instrument, fix sequence."
division: testing
---

# /diagnosing-bugs

## Delegate

Delegate to the **diagnosing-bugs** skill.

Activate when something in <app> is broken and the cause is not already
visible: a stack trace nobody has read, a wrong value, a failing test, a
slow request, a regression between two known states. The skill builds a
red-capable feedback loop first, then minimises, ranks hypotheses, probes one
variable at a time, fixes the root cause and leaves a regression test behind.

Do not activate for a known cause that only needs the change, for feature work
(use `plan`), or for a diff review (use `review`).
