---
name: "research"
description: "Investigates an <app> question against primary sources and captures the findings as a cited Markdown brief in the repo."
division: core
---

# <app> Research skill

> Reusable workflow for answering a question from primary sources and leaving
> a cited brief behind. An agent invokes this skill; the agent supplies the
> question, the skill supplies the sourcing discipline.

## When to Activate

Activate this skill when a question about <app> (a library, a spec, an API, a
platform behavior, a competitor approach) has to be answered from
authoritative sources and the answer is worth keeping: an API contract that
will be implemented against, a version behavior that decides a design, a
claim that will end up in a document or a commit message.

Do NOT activate this skill when:

- The answer lives in the <app> codebase (read the code instead).
- The question is a one-line lookup with no lasting value.
- The request is to implement something (research first, then `plan`).

## Core Principles

- Primary sources only: official documentation, the source code itself,
  specifications, first-party API references. A blog post summarizing a spec
  is not the spec.
- Follow every claim back to the source that owns it.
- The deliverable is a file in the repo, not a chat answer that vanishes with
  the session.
- Every claim carries its source. A claim without a source is a guess.
- The reading happens in a background agent with a fresh context window, so
  the main thread keeps working.

## Rules

- Delegate the reading to a background agent with a fresh context window.
- The background agent must cite the source of every claim it writes down.
- Save the brief where the repo already keeps such notes. Match the existing
  convention; if there is none, put it somewhere sensible and say where.
- One Markdown file per investigation. Do not scatter findings across chat
  messages.
- Prefer the canonical source over a mirror or a cached copy: the upstream
  spec page, the upstream repository, the vendor's own reference.
- Record the version or date the claim was true for when the source has
  versions (a spec version, a release tag).
- Never fabricate a URL, a version number, an API signature or a quotation.
  If the source could not be reached, say so instead of filling the gap.
- Distinguish what the source states from what you concluded. Label the
  inference.
- No prices and no invented links: cite only what the source itself shows.

## Research References

| Claim | Source | Year | Link |
|-------|--------|------|------|
| Primary sources over secondary write-ups, every claim cited | mattpocock/skills, skills/engineering/research/SKILL.md | 2026 | skills/engineering/research/SKILL.md |
| The brief goes to a Markdown file in the repo, following the local convention | mattpocock/skills, skills/engineering/research/SKILL.md | 2026 | skills/engineering/research/SKILL.md |
| The desktop contracts and their owning upstream sources | `PLAYBOOK_DESKTOP_QT.md` §5 | - | `PLAYBOOK_DESKTOP_QT.md` |

## Output Format

Deliver, in order:

1. The question and the scope of the investigation.
2. The path of the brief written to disk.
3. The brief itself: findings with a citation per claim, plus a source table.

Brief shape:

```
Title: The question under investigation

Findings:
- Claim one. (Source: official docs, section, version)
- Claim two. (Source: source code, file and tag)

Sources:
| Claim | Source | Version or date | Link |
|-------|--------|-----------------|------|

Open questions:
- What could not be verified, and why.
```

State explicitly when a source could not be reached.
