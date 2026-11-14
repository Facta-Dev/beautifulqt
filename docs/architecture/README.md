# beautifulqt — Architecture Diagrams

Rendered with [Archify](https://github.com/tt-a1i/archify). Each entry is a standalone,
explorable HTML page (inline SVG, dark/light themes, live motion) paired with its source
JSON candidate. The set documents the Qt 6 desktop architecture contract this repo
teaches: the `domain` / `application` / `adapters` / `presentation` / `platform` layer
wall, MVVM with bindable `QObject` ViewModels and `QAbstractItemModel`, the sacred GUI
thread with `QFuture`/`QtConcurrent`/worker `QThread`s, the CMake target graph that makes
a layer violation a link error, and the drop-in `clang-tidy`/`clang-format` config plus
the CI gates that prove the contract.

| Diagram | Type | What it shows | JSON | HTML |
|---|---|---|---|---|
| c4-containers | architecture | Container view: the operator and the single Qt 6 desktop process (GUI thread + worker pool), the Backend API as the source of truth, the system browser carrying OIDC + PKCE, the OS keystore, the local SQLite (WAL) projection and outbox, the OS tray behind the NotifierPort and the managed policy that outranks user settings — with the three skills and the lints/CI gates framing the delivery | [json](c4-containers.json) | [html](c4-containers.html) |
| services-slices | architecture | Module topology: the composition root, the `presentation/` views and ViewModels, `application/`, `domain/`, `adapters/{in,out}/`, `platform/` and `contracts/`, wired through ports — the slice and layer walls named with the gate that enforces each one (CMake target graph, clang-tidy include checks, the `#ifdef Q_OS_*` grep) | [json](services-slices.architecture.json) | [html](services-slices.architecture.html) |
| auth-algorithm | workflow | The trust algorithm as gated steps: sign in → PKCE verifier and state → the system browser → the redirect → the token endpoint → the OS keystore → rotation with reuse detection, with the managed-policy gate on the side | [json](auth-algorithm.workflow.json) | [html](auth-algorithm.workflow.html) |
| outbox-algorithm | workflow | Durable offline delivery: the optimistic row and the queued mutation in one SQLite transaction → drain on startup, reconnect and timer → the SDK send with an idempotency key → settle, or restore the previous value and retry with backoff until the dead letter | [json](outbox-algorithm.workflow.json) | [html](outbox-algorithm.workflow.html) |
| auth-sequence | sequence | The full sign-in chain across the operator, the ViewModel, the system browser, the token endpoint and the OS keystore, then the refresh with reuse detection revoking the family | [json](auth-sequence.sequence.json) | [html](auth-sequence.sequence.html) |
| outbox-sequence | sequence | The outbox message trace: optimistic write and queue in one transaction, the worker thread claims the row, the SDK posts with an idempotency key, the server answer settles the row — and the failure path that restores the value, requeues with backoff and ends in a dead letter | [json](outbox-sequence.sequence.json) | [html](outbox-sequence.sequence.html) |
| database-dataflow | dataflow | Where state goes: the ViewModel's commands into the use cases, the SQLite (WAL) projection and outbox, the config files, the OS keystore for secrets, and the HTTPS call to the Backend API that stays the source of truth | [json](database-dataflow.dataflow.json) | [html](database-dataflow.dataflow.html) |
| runtime-lifecycle | lifecycle | Process runtime states: `QApplication` and the platform adapters → composition root → View + ViewModel → steady state → drain the outbox → quit, with the single-instance gate, the startup-budget gate and the managed-policy kill switch | [json](runtime-lifecycle.lifecycle.json) | [html](runtime-lifecycle.lifecycle.html) |

Authored with Archify. The repository content is grounded in the architecture contract in
the README, the skill references (`skills/qt-best-practices/references/qt-architecture.md`,
`qt6.md`, `qt-patterns.md`, `cpp-strict.md`), the two skills' `SKILL.md` bodies, the
`lints/` unit and the `scripts/` CI gates.

**Adapted roles.** This is a desktop client, not a backend, so three of the eight file
names carry their series meaning but not their backend content:

| Role | Adapted to | Why |
|---|---|---|
| `auth-*` | OIDC + PKCE in the system browser, tokens in the OS keystore behind `SecretStorePort`, managed policy | there is no auth server here; the trust boundary is the operator's machine, the browser and the keystore |
| `outbox-*` | the persisted SQLite outbox, drained on a worker thread with an idempotency key and backoff | there is no broker or job queue; the durable queue is a table in the local database |
| `database-dataflow` | SQLite (WAL) projection + config files + the OS keystore, with the Backend API over HTTPS as the authority | there is no local server database; the local store is a cache and the API is the source of truth |
