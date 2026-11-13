# Beautiful Qt lints

The two-file unit that turns the qt-best-practices skill into red-on-save
output:

- `.clang-tidy` — the drop-in check set: `bugprone-*`, `performance-*`,
  `modernize-*`, `readability-*`, a reviewed `cppcoreguidelines-*` subset and
  `qt-*`, with warnings as errors and the naming conventions the skill uses.
  The disabled checks are deliberate and documented in the file; a blanket
  disable is a contract change.
- `.clang-format` — the formatter. CI runs
  `clang-format --dry-run --Werror`; a hand-formatted file fails the gate.

## Running it

```bash
cmake --preset dev
clang-tidy -p build src/path/to/file.cpp
clang-format --dry-run --Werror src/path/to/file.cpp
```

`scripts/check-lints.sh` runs both on the repository's example when the tools
are installed. When `clang-format` or `clang-tidy` is missing it prints a
visible `SKIP` and exits 0 — the gate runs in CI, where the tools are pinned
(documented in the workflow), never silently downgraded on a machine that has
them.

## The check project

`lints/check/` holds deliberate violations (a blocking call, a raw owning
pointer, a missing `override`, a Qt 5 API) and a clean control. CI runs
clang-tidy over both and fails if a violation stays quiet or the clean file
reports. Keep the check project in the same style as the drop-in: the config
is the contract, the harness proves it fires.
