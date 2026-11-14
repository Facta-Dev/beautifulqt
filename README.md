<p align="center">
  <img src="assets/icon.png" alt="Beautiful Qt: a green Q on a dark field" width="160">
</p>

# Beautiful Qt

Three standard [Agent Skills](https://agentskills.io) and a lints config that
teach coding agents to write, review, port, and enforce idiomatic
**Qt 6 desktop applications in C++20**:

- **`qt-best-practices`** loads whenever an agent writes or changes a Qt app,
  and steers it toward a sacred GUI thread, a widget-free core and a
  low-end performance budget.
- **`qt-review`** reviews existing code — a Widgets/QML screen, ViewModel,
  model, thread boundary, SDK/SQLite adapter, or diff — and writes a
  prioritized report where every finding cites the rule it breaks and shows
  the fix.
- **`qt-port`** ports Qt 5, QML-only, PySide/PyQt, Electron, or a web screen
  to Qt 6 C++ with the same behavior, porting the original tests first.
- **`lints/`** is a drop-in clang-tidy + clang-format unit that runs in CI.

They work with Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI,
and any other agent that reads the Agent Skills format.

## Why

Qt rewards discipline and punishes shortcuts, especially on old hardware:

- A blocking call on the GUI thread freezes the window on a slow disk or a
  slow network.
- A widget per row makes a 100k-row list unusable.
- A lambda that captures `this` without the context-object connection crashes
  after the receiver dies.
- A Qt 5 API that compiles today disappears tomorrow.
- A secret in SQLite or a log is a breach on a shared machine.
- WebEngine in the main app blows the memory budget before any feature ships.

Beautiful Qt is the contract that catches those before review.

## Install

### Claude Code

```bash
/plugin marketplace add Facta-Dev/beautifulqt
/plugin install beautiful-qt@beautiful-qt
```

### OpenAI Codex and ChatGPT

The repository ships a portable `plugin.json` with the `com.openai` interface
block. Point Codex at the repository, or package it with:

```bash
python3 scripts/package-openai-plugin.py --out beautiful-qt.zip
```

### Any agent

Copy `skills/qt-best-practices`, `skills/qt-review`, and `skills/qt-port` into
your agent's skills directory. Each skill is a `SKILL.md` plus a `references/`
digest; no runtime, no network.

## A worked example

Without the skill, an agent writes a loader that blocks the GUI thread and
leaks the reply:

```cpp
// Without the skill: a synchronous network call in a slot.
void InventoryView::refresh() {
  QNetworkAccessManager manager;
  QNetworkReply* reply = manager.get(QNetworkRequest(apiUrl()));
  reply->waitForFinished();
  const QByteArray body = reply->readAll();
  m_model->reset(parse(body));
}
```

Problems: the GUI thread blocks on the network; the manager and reply die at
the end of the slot; the model resets on every refresh; an error is
indistinguishable from an empty list.

With the skill, the ViewModel calls an async use case, the SDK owns the
network, and the model applies the result on the GUI thread:

```cpp
// With the skill: async use case, one status, result on the GUI thread.
void InventoryViewModel::refresh() {
  setStatus(Status::Loading);
  const auto requestId = ++m_requestId;
  m_useCases.listInventory().then(this, [this, requestId] (const Result<InventoryPage>& result) {
    if (requestId != m_requestId) return;  // a newer refresh superseded this one
    if (!result) {
      setStatus(statusFor(result.error()));
      return;
    }
    m_model->setRows(result->rows);
    setStatus(result->rows.isEmpty() ? Status::Empty : Status::Ready);
  });
}
```

The status enum, the layer contract and the threading rules are in
[`skills/qt-best-practices/references/qt-architecture.md`](skills/qt-best-practices/references/qt-architecture.md).

## The architecture contract

```text
Views (Widgets/QML) + ViewModels  ──►  application (use cases, ports)  ──►  domain
        ▲                                      ▲
        └── state + commands ──────────────────┘
adapters/out: SDK/HTTP · Realtime · SQLite · Keystore · Updater · Telemetry
platform: the only place with #ifdef Q_OS_*
```

| Layer | Owns | Must not touch |
|---|---|---|
| **domain** | Entities, rules, events | `QObject`, QtGui/Widgets/Network/Sql, OS APIs |
| **application** | Use cases, ports, policy, sync, outbox | widgets, network/sql adapters |
| **adapters/out** | SDK, realtime, SQLite, keystore, updater | views, viewmodels |
| **presentation** | ViewModels, Widgets/QML | SDK, storage, network directly |
| **platform** | Per-OS code | domain/application |

The unbreakable rules:

1. The GUI thread never blocks.
2. `#ifdef Q_OS_*` appears only under `platform/`.
3. Views never touch the SDK, storage or network.
4. ViewModels never touch widgets or windows; navigation is by route.
5. Errors are values; exceptions do not cross layers.

## Architecture diagrams

The repository ships eight [Archify](https://github.com/tt-a1i/archify) diagrams under
[`docs/architecture/`](docs/architecture/README.md), each a standalone HTML page you can
open in a browser — inline SVG, dark/light themes, live motion — with its source JSON
next to it.

| Diagram | Type | HTML |
|---|---|---|
| Container architecture | architecture | [c4-containers.html](docs/architecture/c4-containers.html) |
| Layers, slices & dependency walls | architecture | [services-slices.architecture.html](docs/architecture/services-slices.architecture.html) |
| Trust algorithm (OS keystore + OIDC/PKCE) | workflow | [auth-algorithm.workflow.html](docs/architecture/auth-algorithm.workflow.html) |
| Offline outbox algorithm | workflow | [outbox-algorithm.workflow.html](docs/architecture/outbox-algorithm.workflow.html) |
| Trust sequence | sequence | [auth-sequence.sequence.html](docs/architecture/auth-sequence.sequence.html) |
| Offline outbox sequence | sequence | [outbox-sequence.sequence.html](docs/architecture/outbox-sequence.sequence.html) |
| Dataflow (local state, secrets, API) | dataflow | [database-dataflow.dataflow.html](docs/architecture/database-dataflow.dataflow.html) |
| Runtime lifecycle | lifecycle | [runtime-lifecycle.lifecycle.html](docs/architecture/runtime-lifecycle.lifecycle.html) |

The full index — what each diagram shows, and how the `auth`, `outbox` and
`database-dataflow` roles are adapted for a desktop client — is in
[`docs/architecture/README.md`](docs/architecture/README.md).

## The lints config

[`lints/.clang-tidy`](lints/.clang-tidy) and
[`lints/.clang-format`](lints/.clang-format) are copy-in units:

- **clang-tidy:** `bugprone-*`, `performance-*`, `modernize-*`,
  `readability-*`, a reviewed `cppcoreguidelines-*` subset and `qt-*`, with
  warnings as errors and the naming conventions the skill uses.
- **clang-format:** the formatter; CI runs `--dry-run --Werror`.

[`scripts/check-lints.sh`](scripts/check-lints.sh) runs both on the example and
the violation harness. A missing tool prints a visible `SKIP`; CI installs the
tools and runs the same script. [`lints/check/`](lints/README.md) holds the
deliberate violations plus a clean control.

The runnable example in [`examples/minimal/`](examples/minimal/CMakeLists.txt)
is compiled and tested by [`scripts/check-build.sh`](scripts/check-build.sh)
when Qt is installed.

## What it does not do

- The skills contain instructions and reference text only. They make no
  network calls and collect no data ([PRIVACY.md](PRIVACY.md)).
- When a Qt/C++ toolchain is available, the skills run CMake, ctest,
  clang-format, and clang-tidy; without one, they work from the code alone.
- The lint config is a copy-in unit, not a dependency.
- The skills do not replace a reference-machine performance lab or a store
  review; they tell the agent what those must prove.

## Repository layout

```text
skills/
  qt-best-practices/   SKILL.md + references/ (Qt 6, patterns,
                       architecture, strict C++)
  qt-review/           SKILL.md (report format, ranking, waived gates)
  qt-port/             SKILL.md (Qt 5/QML/PySide/Electron/web → Qt 6)
lints/
  .clang-tidy          the drop-in checks
  .clang-format        the formatter
  check/               the violation harness + clean control
scripts/
  check-skill.py       frontmatter, links, evals, manifests
  check-examples.py    C++ block balance (offline gate)
  check-build.sh       CMake build + ctest of the example
  check-lints.sh       clang-format/clang-tidy (SKIP if absent)
  package-openai-plugin.py
tests/                 validator, wording, lints-config and gate tests
examples/
  minimal/             a runnable Qt Widgets example + QTest
  review-inventory.md  a full worked review
docs/
  architecture/        eight Archify diagrams (C4, slices, auth,
                       outbox, dataflow, lifecycle) + their index
```

## Sources

- The Qt 6 documentation (Widgets, Quick, model/view, threading, CMake,
  packaging, accessibility).
- The facta desktop handbook (`PLAYBOOK_DESKTOP_QT.md`): GUI thread, layers,
  MVVM, realtime, storage/outbox, performance budgets, enterprise policy.
- The C++ Core Guidelines and clang-tidy/clang-format documentation.

## Contributing

Rule proposals are welcome; open an issue with the
[rule template](.github/ISSUE_TEMPLATE/propose-a-rule.yml) and a source. A
rule without a source and a failing example is a preference, not a rule. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Siblings

Beautiful Qt is part of the Beautiful series for the facta playbooks:
[beautiful-j2ee](https://github.com/Facta-Dev/beautiful-j2ee),
[beautifulandroid](https://github.com/Facta-Dev/beautifulandroid),
[beautifulcli](https://github.com/Facta-Dev/beautifulcli),
[beautifulextension](https://github.com/Facta-Dev/beautifulextension),
[beautifulgo](https://github.com/Facta-Dev/beautifulgo),
[beautifulios](https://github.com/Facta-Dev/beautifulios),
[beautifulnodejs](https://github.com/Facta-Dev/beautifulnodejs),
[beautifulpython](https://github.com/Facta-Dev/beautifulpython),
[beautifulreact](https://github.com/Facta-Dev/beautifulreact),
[beautifulreactnative](https://github.com/Facta-Dev/beautifulreactnative),
[beautifulrust](https://github.com/Facta-Dev/beautifulrust).

## License

MIT — see [LICENSE](LICENSE).
