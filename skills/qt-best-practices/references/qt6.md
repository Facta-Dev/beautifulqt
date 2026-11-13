# Qt 6 platform digest

The Qt facts a desktop app depends on, with the design consequence. The Qt
documentation is the source; this is the review checklist.

## 1. Versions

- Qt **6.12 LTS** for new projects (five-year maintenance); **6.8 LTS**
  acceptable for conservative fleets (supported into 2029). Verify the
  support window at adoption.
- C++20 (C++17 minimum) for domain/application/adapters; Qt Widgets by
  default, Qt Quick for isolated motion-heavy surfaces.
- CMake with presets and Ninja; a locked dependency baseline (vcpkg manifest
  or Conan lockfile) for reproducible builds.
- Dynamic Qt unless a commercial license allows static linking.

## 2. Widgets vs Qt Quick

| | Qt Widgets | Qt Quick/QML |
|---|---|---|
| Rendering | CPU raster | Scene graph (GPU, software fallback) |
| Best for | Data-dense/enterprise screens | Motion-heavy, custom UI |
| Old hardware | Predictable | Test the software backend |
| ViewModel | Same | Same |

- No Qt WebEngine in the main app; it is a Chromium-sized footprint.
- A GPU path is an optimization with a tested software fallback.

## 3. The GUI thread

- The GUI thread must never block: no synchronous network, disk, parse, crypto
  or big loop.
- One-shot work: `QtConcurrent::run`/`QFuture`. Long-lived work: a `QObject`
  moved to a `QThread`. Bounded tasks: `QThreadPool`.
- Cross-thread UI updates use queued signals/slots or
  `QMetaObject::invokeMethod(..., Qt::QueuedConnection)`.
- Models are updated on their own thread; a worker returns data, the
  ViewModel applies it.
- Exceptions do not cross a slot boundary; expected failures are `Result<T>`.

## 4. Model/view

- A list is a `QAbstractItemModel` (or a proxy), not a widget per row.
- Emit the right signals: `beginInsertRows`/`endInsertRows`,
  `dataChanged` for values, `beginResetModel` only for a full replacement.
- A `QModelIndex` is transient; persist the id and re-resolve after a reset.
- Use `QSortFilterProxyModel` for sorting/filtering; do not re-sort in a view.

## 5. Networking and async

- `QNetworkAccessManager` lives behind the SDK adapter, never in a view.
- `QNetworkReply` is asynchronous; connect to `finished`, handle errors, and
  delete the reply with `deleteLater`.
- Cancellation: keep the reply and abort it when a newer request supersedes
  it.
- Long operations (`202`) poll or stream with backoff and a timeout.

## 6. CMake

- One target per layer; a target links only the targets it may depend on, so a
  layer violation fails at link time.
- `target_compile_features(cxx_std_20)`, warnings as errors, `-fno-exceptions`
  only if the dependency set allows it.
- Qt6 components are explicit: `find_package(Qt6 REQUIRED COMPONENTS Core Gui
  Widgets Network Sql Concurrent Test)`.
- `qt_standard_project_setup()`, `qt_add_executable`, `qt_add_qml_module` for
  Quick.

## 7. Packaging and updates

- Windows: MSI/MSIX with Authenticode; macOS: notarized `.app`/`.dmg`;
  Linux: AppImage/deb/rpm with a signed repository.
- Signed updates with channels, staged rollout, atomic swap and rollback;
  admins can disable or defer.
- A crash handler writes minidumps, opt-in by policy.

## 8. Platform

- `#ifdef Q_OS_*` only under `platform/`.
- Windows: native TLS stack caveats; verify TLS 1.3 support.
- macOS: universal binary; notarization.
- Linux: X11 and Wayland; test both where supported.
- No 32-bit; x86-64 and ARM64.

## 9. Accessibility

- `QAccessible` names/roles; keyboard reachability and visible focus.
- High DPI is always on in Qt 6; layouts survive scaling and long
  translations.
- Color is never the only signal.

## 10. Testing

- Qt Test for units, models and GUI interactions (`QTest::keyClick`,
  `mouseClick`).
- `QSignalSpy` for ViewModel behavior; fake ports; no GUI window.
- SQLite/WAL integration and migration fixtures.
- Performance budgets on the reference floor machine.
- Platform adapters tested per OS in CI.
