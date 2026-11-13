---
name: qt-port
description: >-
  Port an existing desktop UI to an idiomatic Qt 6 / C++20 application with the
  same behavior: Qt 5, QML-only, PySide/PyQt, Electron, or a web screen. Use
  this skill whenever the user asks to migrate, convert, rewrite, or port an
  app or window to Qt 6, modernize a Qt 5 app, or move a web/Electron UI to a
  native desktop app. Trigger on port, migrate, convert to Qt 6, "turn this
  PySide app into C++ Qt", "move this Electron screen to Qt", or a pasted
  Qt5/PySide/Electron file. Port the original tests first, keep behavior
  identical, and write a PORTING.md.
---

# Qt port

A port preserves behavior while changing the implementation. The output is not
a Qt 5 app with new includes; it is a Qt 6 app a Qt developer would have
written, with the same observable behavior and tests proving it.

## 1. The order of work

1. **Read the source and its tests.** The tests are the specification. If
   there are none, write characterization tests against the current behavior
   first.
2. **Port the tests first.** Same cases, same assertions, expressed in Qt Test
   or a ViewModel test with `QSignalSpy`. A port without a failing test is a
   rewrite with hope.
3. **Map every screen, signal, command, network call and storage key.**
4. **Define the target layers.** domain/application/adapters/presentation/
   platform/contracts; the ViewModels and ports come first.
5. **Port one screen at a time**, with the closed status enum.
6. **Run the gates.** CMake build, ctest, clang-format/tidy, a release run on
   the reference floor.
7. **Write `PORTING.md`.** Every deliberate difference, every framework
   feature not reproduced, every dependency dropped, and why.

## 2. Qt 5 → Qt 6 mapping

| Qt 5 | Qt 6 |
|---|---|
| `QRegExp` | `QRegularExpression` (PCRE2) |
| `QStringRef`/`QStringView`-era APIs | `QStringView`/`QLatin1StringView` |
| `QDesktopWidget` | `QScreen`/`QGuiApplication::primaryScreen` |
| `QGLWidget` | `QOpenGLWidget` (or raster Widgets) |
| `QVariant` implicit conversions | Explicit `QVariant::value<T>()`/`to…` |
| `QMouseEvent::pos()` | `position()`/`globalPosition()` |
| `QTextCodec` | `QStringConverter`/`QTextDecoder` |
| `QNetworkConfiguration` | Removed; use `QNetworkAccessManager` directly |
| `qmake` project | CMake target graph |
| `Q_FOREACH`/`foreach` | Range-based `for` |
| `QSignalMapper` | Lambdas with the context-object connection |
| `QMetaObject::invokeMethod` string args | Functor overload |
| `Q_FALLTHROUGH` | `[[fallthrough]]` |

- **High-DPI is always on** in Qt 6; remove the Qt 5 attributes and test
  scaling.
- **`QString` is UTF-16 and implicit conversions are narrower**; use explicit
  `QStringLiteral`/`u"..."_s` and avoid `const char*` round trips.
- **Container/algorithm changes** (`QVector` is `QList`, `qAsConst` →
  `std::as_const`): port the types, not just the names.

## 3. PySide/PyQt → C++ Qt

- **Keep the ViewModel contract, not the Python class shape.** A Python
  service becomes a use case + port; a Python signal becomes a ViewModel
  property/command.
- **Move the SDK into the C++ adapter**; no Python network calls in a view.
- **Port the tests** to Qt Test or a C++ ViewModel test; keep the same
  behaviors.
- **Do not embed a Python runtime** to keep the old code; that defeats the
  memory/startup budget.

## 4. Electron/web → Qt

- **Replace the DOM with Widgets** (data-dense) or Quick (motion-heavy); one
  ViewModel per screen.
- **Replace `fetch`/`localStorage`** with the SDK and the SQLite projection;
  tokens go to the keystore.
- **Replace the JS event bus** with typed signals/slots and use cases.
- **Replace CSS layout** with Qt layouts; test scaling, long translations and
  keyboard navigation.
- **Drop the Chromium runtime** unless a feature genuinely needs WebEngine;
  if it does, isolate it in an optional component and budget it.

## 5. Behavior parity checklist

- [ ] Every screen, command, shortcut and menu action exists.
- [ ] Every status is rendered: loading, ready, empty, forbidden, not-found,
      offline, error, policy-blocked.
- [ ] Every network call has the same method, path, payload and headers.
- [ ] Every list uses a model and survives a reset/reorder.
- [ ] Keyboard navigation and accessibility names match or improve.
- [ ] The GUI thread never blocks; long work is off-thread.
- [ ] Tokens are in the keystore; no secret in config/SQLite/logs.
- [ ] The outbox is persisted and idempotent.
- [ ] The release build meets the startup/scroll budgets on the floor.
- [ ] The original tests pass, ported; new tests cover the Qt-only paths.
- [ ] `PORTING.md` lists every deliberate difference.

## 6. What not to do

- **Do not keep the source framework's shape.** A web page rendered in a
  `QWebEngineView`, a Python service locator, or a Qt 5 event filter chain is
  a port that will be rewritten again.
- **Do not block the GUI thread** because the old app did; that is the bug the
  port exists to fix.
- **Do not skip the tests.** A port validated only by clicking through it
  ships the source's bugs plus new ones.
- **Do not silently change behavior.** Reproduce the source quirk, pin it with
  a test, and list the fix as a follow-up — or fix it deliberately and say so.
- **Do not drop accessibility.** If the source was a mouse-only control, the
  port is a keyboard-reachable action with a name.

## 7. Cross-skill contract

- `qt-best-practices` is the target style; every ported screen follows it.
- `qt-review` reviews the port before release and ranks a broken architecture
  contract above every other finding.
- The `lints/` config is the machine-checkable half; a port that needs a lint
  exception is a port that has not finished.
