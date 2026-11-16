---
name: "domain-modeling"
description: "Sharpens the <app> domain model: challenges conflicting terms, resolves the vocabulary into the project glossary, and records the decisions that deserve an ADR."
division: core
---

# <app> Domain Modeling skill

> Reusable workflow for changing the <app> domain model, not just reading it.
> An agent invokes this skill; the requester supplies the vocabulary, the
> skill supplies the discipline.

## When to Activate

Activate this skill when the <app> domain language is in question: a term is
ambiguous or overloaded, a requester describes behavior the code contradicts,
a glossary entry needs writing or correcting, or a decision has been made
that a future reader would puzzle over.

Do NOT activate this skill when:

- The request is only to read existing vocabulary (one grep of the glossary
  is enough).
- The request is to add or change a test (use `tdd`).
- The request is to review a diff for correctness (use `review`).

## Core Principles

- Changing the model is active work: challenge the term, propose a precise
  canonical word, and record the resolution the moment it crystallises.
- One word per concept. Pick the best name and list the rejected ones under
  `_Avoid_`, so the vocabulary does not fork.
- The glossary holds domain language and nothing else: no implementation
  detail, no spec, no scratch pad.
- Definitions say what a thing IS, not what it does. One or two sentences.
- Only context-specific terms belong. Generic programming vocabulary
  (timeouts, error types, util patterns) stays out even when the project uses
  it heavily.
- The code is evidence. When the requester describes behavior, check the
  code and surface the contradiction instead of silently picking a side.
- ADRs are offered sparingly. Most decisions are not worth a file.

## Rules

- Update the glossary inline as terms resolve. Do not batch the writes to
  the end of the session.
- Call out a conflict with the existing glossary immediately: name the
  existing definition and the new meaning, then ask which is intended.
- For a fuzzy or overloaded term, propose one canonical term and its
  `_Avoid_` list rather than leaving both words alive.
- Stress-test relationships with concrete scenarios that probe edge cases
  and force the boundaries between concepts to be stated.
- Create files lazily: the glossary when the first term is resolved,
  `docs/adr/` when the first ADR is needed. Never create empty scaffolding.
- A single-context repo keeps one glossary at the root. A multi-context repo
  keeps a root `GLOSSARY-MAP.md` pointing at each context's glossary and ADR
  folder, plus the relationships between the contexts.
- Write an ADR only when all three hold: hard to reverse, surprising
  without context, and the result of a real trade-off. If one is missing,
  skip the ADR and say which one was missing.
- An ADR is one short paragraph: context, decision, reason. Optional
  sections (status, considered options, consequences) only when they earn
  their place. Number sequentially in `docs/adr/NNNN-slug.md`.
- Never invent a term the requester did not use or the code does not
  support.

## Research References

| Claim | Source | Year | Link |
|-------|--------|------|------|
| Glossary terms carry an `_Avoid_` list and define what a thing IS | mattpocock/skills, skills/engineering/domain-modeling/GLOSSARY-FORMAT.md | 2026 | skills/engineering/domain-modeling/GLOSSARY-FORMAT.md |
| An ADR is warranted only when hard to reverse, surprising, and a real trade-off | mattpocock/skills, skills/engineering/domain-modeling/ADR-FORMAT.md | 2026 | skills/engineering/domain-modeling/ADR-FORMAT.md |
| The active discipline: challenge terms, sharpen language, cross-reference the code | mattpocock/skills, skills/engineering/domain-modeling/SKILL.md | 2026 | skills/engineering/domain-modeling/SKILL.md |
| The layer law that gives the domain its vocabulary | `PLAYBOOK_DESKTOP_QT.md` §3 | - | `PLAYBOOK_DESKTOP_QT.md` |
| Where the ADRs of this repo live | `docs/adr/` | - | `docs/adr/` |

## Output Format

Deliver, in order:

1. The resolved terms: canonical term, its definition, and the `_Avoid_`
   list.
2. The glossary update, written inline.
3. The ADR, or the reason none was written (which of the three conditions
   was missing).
4. Open questions: terms that are still ambiguous and need a decision from
   the requester.

Example:

```
domain-modeling: "cancellation" is now canonical for a full Order cancel;
"Avoid: refund, void". Partial cancellation is a different concept and has
no term yet. ADR skipped: the refund policy choice is easy to reverse.
```
