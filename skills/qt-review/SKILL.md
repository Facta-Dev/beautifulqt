---
name: qt-review
description: >-
  Review a Qt 6 / C++ desktop change — a Widgets or QML screen, a ViewModel, a
  QAbstractItemModel, a worker/thread boundary, the SDK or SQLite adapter, the
  CMake target graph, a diff — and produce a prioritized report where every
  finding cites the file and line, the rule it breaks, and the smallest fix.
  Use this skill whenever the user asks to review, audit, critique, or "find
  problems in" a Qt app, a window, a model, or a threading change. Trigger on
  review, audit, code review, PR review, "what is wrong with this window",
  "check this worker", "review this model", or a pasted .cpp/.h/QML file.
  Architecture and GUI-thread contracts always rank first.
---

# Qt review

A review is a prioritized list of findings, not a rewrite. Read the whole
change first. Every finding has four parts: **location** (file and line),
**severity**, **the rule it breaks** (named or quoted), and **the smallest
fix**. If you cannot cite a rule or a user-visible consequence, it is not a
finding; it is a preference for the Notes section, if anywhere.

## 1. Report shape

```text
## Verdict
<one paragraph: what this change does, whether it is safe to ship, and the
single most important thing to fix>

## Must fix
1. <file>:<line> — <finding>. Rule: <rule or contract>. Fix: <smallest fix>.

## Should fix
...

## Notes
...

## Waived gates
...
```

- **Must fix** blocks merge or release: a blocking GUI-thread call, a broken
  layer, a dangling pointer/lifetime bug, a token outside the keystore, a
  blocking network call, a model updated from the wrong thread.
- **Should fix** is worth doing in this change or the next: a per-paint
  allocation, a missing accessibility name, a slow startup path.
- **Notes** is optional. Do not pad the report to look thorough.

## 2. Categories, in ranking order

### Architecture contracts (always Must fix, ranked first)

A broken architecture contract (ranked above everything) is a Must fix even
when the app works. Check:

- `domain`/`application` imports QtGui/Widgets/Quick/Network/Sql, a widget, a
  window, or a platform API. They talk through ports.
- A **View** (Widgets/QML) imports the SDK, storage or network, or contains a
  business condition beyond "show this status".
- A **ViewModel** imports a widget/window or navigates by pointer instead of a
  `Navigator` route.
- `#ifdef Q_OS_*` outside `platform/`.
- A CMake target links a layer it is not allowed to link.
- A permission decision made client-side as a security control.

Name the violated rule and quote it; the fix is to move the logic to the layer
that owns it.

### GUI thread and threading

- A blocking call on the GUI thread: synchronous network, large file read,
  `QProcess::waitForFinished`, `QThread::sleep`, heavy parse/crypto.
- A widget/model/QObject touched from a non-owner thread; a direct connection
  where a queued one is required.
- A `QFuture`/worker result applied without cancellation or superseding; a
  stale result overwriting a newer state.
- A `QTimer` doing polling/retry work that belongs in the application layer.
- An exception crossing a slot boundary.

### Memory and lifetimes

- A raw pointer to a deleted `QObject`; a lambda capturing `this` without the
  context-object overload.
- A child with a parent deleted manually; a parent-child cycle hidden behind
  smart pointers.
- A `QModelIndex` persisted across a reset; a dangling `QStringRef`/view.
- A missed `deleteLater` on a QObject created per event.
- Copy-on-write detach in a hot loop.

### MVVM and models

- A list copied into a widget instead of a `QAbstractItemModel`.
- A status modeled as independent booleans instead of the one closed enum.
- A model that emits `dataChanged` for a structural change, or
  `beginResetModel` for a single row.
- A ViewModel with a widget/window pointer; a global mutable singleton.
- A view with business logic instead of a status switch.

### Security

- A token/password in SQLite, config, logs, a crash dump or the binary; the
  keystore is the only secret store.
- A remote script/content evaluated or a plugin/DLL loaded from an untrusted
  path.
- TLS disabled, a custom CA with no validation, or an `--insecure` default.
- An update without signature verification; a policy kill switch ignored.
- A client-side permission check presented as access control.

### Performance

- A blocking startup path; heavy work before the first window.
- A widget per row; a model without virtualization.
- A per-paint allocation, a deep layout, or a scaled giant pixmap.
- Qt WebEngine in the main app; a GPU-only path with no software fallback.
- No measurement on the reference floor; a budget raised without evidence.

### Accessibility and i18n

- An action reachable only by mouse; no accessible name/role; focus lost.
- Hard-coded strings instead of `tr()`; concatenated sentences; RTL/long
  translations untested.
- Color-only meaning; a focus ring removed with no replacement.
- Hard-coded pixel sizes around text that break with scaling.

### Tests

- No ViewModel test with `QSignalSpy`; no model row/insert/reset test.
- No migration fixtures; no SQLite/WAL integration test.
- No GUI test for the critical interaction; no performance budget on the
  floor; no platform adapter test.
- A test that asserts implementation instead of behavior.

## 3. Waived gates

If the diff deletes or weakens a lint, a test, a type, an accessibility check
or a budget, flag the deletion itself, loudly — even when the new code looks
fine. Look for:

- A new `// NOLINT` **without a reason**; a blanket `// NOLINTNEXTLINE`; a
  check disabled in `.clang-tidy` or a warning removed from the CMake flags.
- A CMake target linked around a layer rule; a `friend` or `#define private
  public` used to bypass a boundary.
- A skipped test without an owner and expiry; a migration fixture deleted; a
  performance budget raised without a device-lab run.
- A `const` removed, ownership made manual, or an exception introduced across
  a slot to make a path compile.

State the deletion, the reason it claims, and what it would take to keep the
gate. "Temporarily" is not a reason; an expiring waiver with an owner is.

## 4. How to review

1. **Read the change twice.** First for intent, then for the diff.
2. **Run the gates if you can:** CMake build, `ctest`, `clang-format
   --dry-run --Werror`, `clang-tidy -p build`, a release run on the floor.
3. **Check the GUI thread and the architecture first.** They are the
   expensive findings; style is cheap.
4. **Cite evidence.** File and line for every Must fix; a rule name or a
   quoted contract for every finding.
5. **Propose the smallest fix.** "Rewrite the window" is not a fix; "move the
   parse to `QtConcurrent::run` and apply the result in a queued slot" is.
6. **Stop when the change is safe.** An empty Should-fix section is a valid
   review.

## 5. Worked example

`examples/review-inventory.md` is a full review of a small inventory window:
the blocking loader, the model and the ViewModel, the findings in ranking
order, and the fixed module. It shows the GUI-thread violation first, then the
lifetime bug, then the model update, then the startup budget.

## 6. Cross-skill contract

- `qt-best-practices` defines the rules this review cites. When a finding and
  the skill disagree, the skill is the source.
- `qt-port` produces the change; this review checks it before release.
- The `lints/` config is the machine-checkable subset. A finding the config
  can catch should become a rule, not a repeated comment.
