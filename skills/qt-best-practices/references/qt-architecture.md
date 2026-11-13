# Qt architecture contract

The layer contract from the facta desktop handbook, reduced to what a Qt 6 app
must keep. It is enforced by the CMake target graph and `lints/.clang-tidy`.

## 1. The layers

```text
INBOUND                              OUTBOUND
Views (Widgets/QML) + ViewModels     SDK/HTTP · Realtime · SQLite · Keystore
Realtime events · OS events          Notifications · Updater · Telemetry
                 │                              ▲
                 ▼                              │
        APPLICATION (use cases, ports, policy, sync, outbox)
                 │
                 ▼
        DOMAIN (entities, value objects, rules, events)
```

| Layer | May depend on | Must not depend on |
|---|---|---|
| **domain** | std, shared-kernel; QtCore value types if the ADR allows | `QObject`, signals/slots, QtGui/Widgets/Quick/Network/Sql, OS APIs |
| **application** | domain, contracts, QtCore (`QObject`, `QFuture`, `QTimer`) | QtGui/Widgets/Quick/Network/Sql/WebSockets, platform adapters |
| **adapters/out** | application ports, platform, Qt Network/Sql/WebSockets | views, viewmodels |
| **adapters/in** | application, contracts | other slices' internals, SQL/HTTP |
| **presentation/views** | ViewModel types, ui-kit | SDK, storage, network, application directly |
| **platform** | OS APIs, Qt Core/GUI | domain/application |
| **contracts** | shared-kernel | everything else |

## 2. Ports

The consumer declares the port; the adapter implements it.

| Port | Declared by | Implemented by |
|---|---|---|
| `LeadRepositoryPort` | feature application | SDK + SQLite adapter |
| `SessionPort` | application | keystore + SDK adapter |
| `PolicyPort` | application | managed policy reader |
| `RealtimePort` | application | SSE/WebSocket/polling adapters |
| `NotifierPort` | ViewModel | tray/toast/dialog adapter |
| `NavigatorPort` | ViewModel | the shell/router |
| `ClockPort` | domain | system clock (tests use a fake) |
| `SecretStorePort` | application | OS keystore adapter |
| `UpdaterPort` | application | signed updater adapter |

Ports return `QFuture<Result<T>>`; errors are values, never exceptions across
layers.

## 3. CMake target graph

- One target per layer/slice: `domain_<slice>`, `application_<slice>`,
  `adapter_<slice>`, `viewmodel_<slice>`, `view_<slice>`, `platform`.
- `target_link_libraries` lists only the allowed targets; a layer violation
  fails at link time.
- A shared `contracts` target holds DTOs, error codes, the event envelope and
  the policy schema.
- The composition root is a single `app` target that links the adapters and
  builds the ViewModels.

## 4. Slices

- One slice = one backend slice; same name in the folder, the URL module, the
  permission prefix, the realtime topic and the tests.
- Slice folders: `domain/ application/ adapters/{in,out}/
  presentation/{viewmodels,views}/ contracts/`.
- A slice never imports another slice's internals; shared behavior moves to
  `shared-kernel` or a port.

## 5. MVVM

- ViewModel: `QObject`, bindable properties, one status enum, invokable
  commands, a model for lists.
- View: Widgets or QML binding to the ViewModel; no business conditions.
- Navigation by route through a `NavigatorPort`; no window pointers.
- One ViewModel per screen; no global mutable singletons.
- Test with `QSignalSpy` and fake ports; no GUI window.

## 6. Threading

- GUI thread never blocks.
- One-shot: `QtConcurrent`; long-lived: a worker `QObject` on a `QThread`;
  bounded: `QThreadPool`.
- Queued connections for cross-thread UI updates.
- Cancellation and stale-result guards.
- No exceptions across a slot boundary.

## 7. Security and policy

- Secrets in the OS keystore; no secret in SQLite/config/logs.
- Signed updates; trusted plugin paths; TLS always on.
- Managed policy wins; kill switch applied immediately.
- Authorization server-side; the UI hides actions.

## 8. Performance

- Budgets on the reference floor: startup, screen switch, scroll FPS, memory.
- Model + proxy for lists; sized pixmaps; no per-paint allocations.
- No WebEngine in the main app; no GPU assumption.
- A regression fails CI.

## 9. Testing

- Domain/application: Qt Test, no GUI.
- ViewModel: `QSignalSpy` + fake ports.
- Model: insert/remove/reset, proxy sort/filter.
- SQLite: real file/WAL + migration fixtures.
- GUI: `QTest::keyClick`/`mouseClick`; accessibility names.
- Platform adapters per OS in CI.

## 10. The enforcement map

| Rule | Where |
|---|---|
| domain/application do not include QtGui/Widgets/Quick/Network/Sql | CMake link graph + clang-tidy `include` checks |
| `#ifdef Q_OS_*` only in `platform/` | a grep gate in CI |
| views do not include the SDK/storage/network | CMake target graph |
| no blocking call on the GUI thread | review + clang-tidy concurrency checks |
| no `NOLINT` without a reason | `lints/check` + review |
| no warnings | `-Werror` in the CMake preset |

When a change needs an exception, re-cut the layout; do not add a link or a
`NOLINT`. A config exception is a contract change.
