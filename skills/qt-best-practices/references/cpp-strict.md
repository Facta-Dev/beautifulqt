# C++ strict for Qt

The C++20 subset and the ownership rules that keep a Qt app predictable on old
hardware.

## 1. The subset

- C++20; no compiler extensions; warnings as errors in the build preset.
- RAII everywhere: `std::unique_ptr` for exclusive ownership, `QObject`
  parent-child for QObject trees, `QPointer` for a non-owning guard.
- Value semantics by default; references/pointers only for polymorphism or
  non-ownership.
- `const` correctness; `[[nodiscard]]` on results and factories.
- `enum class` with an underlying type; `Q_ENUM` for QML/metaobject use.
- No `using namespace` in a header; no `#define` in a header unless it is a
  documented feature flag.

## 2. Ownership and lifetimes

- A `QObject` child dies with its parent; never `delete` a child that has one.
- A lambda connected to a signal uses the context-object overload so it
  disconnects when the receiver dies:
  `connect(sender, &Sender::signal, receiver, [receiver] { ... });`
- Do not capture `this` in a long-lived async callback without a `QPointer` or
  a value copy.
- A `QModelIndex` is transient; persist the id, re-resolve after a reset.
- `deleteLater` for a QObject destroyed from its own event; never `delete this`
  in a slot.

## 3. Errors as values

```cpp
template <class T>
using Result = std::expected<T, AppError>;
```

- Expected failures (validation, permission, network) are `Result`.
- Exceptions are for programmer errors and are never thrown across a slot or a
  thread boundary.
- Every error carries a stable `code`, a message and a `correlationId`.

## 4. Threading

- No blocking call on the GUI thread.
- `QFuture`/`QtConcurrent` for one-shot work; a worker `QObject` on a
  `QThread` for long-lived work.
- Cross-thread UI updates via queued connections.
- Shared data is immutable or guarded; prefer message passing over locks.
- `QThread::sleep`, `waitForFinished` and synchronous network calls are
  findings, not optimizations.

## 5. Qt specifics

- `QStringLiteral`/`u"..."_s` for literals; explicit conversions, no implicit
  `const char*` round trips.
- `QRegularExpression`, not `QRegExp`.
- `QStringView` for read-only parameters; `QLatin1StringView` for ASCII
  literals.
- `QVariant::value<T>()` explicitly; no implicit conversions.
- `QMetaObject::invokeMethod` with the functor overload.
- `qAsConst` → `std::as_const`; `QVector` is `QList` in Qt 6.

## 6. Warnings and lint

- `-Wall -Wextra -Wpedantic -Werror` (MSVC: `/W4 /WX`).
- clang-tidy: `bugprone-*`, `performance-*`, `modernize-*`, `readability-*`,
  `cppcoreguidelines-*` (a reviewed subset), `qt-*` where available.
- A `// NOLINT` names the check and the reason; a blanket disable is a
  finding.
- `clang-format` is the formatter; do not hand-format around it.

## 7. Review questions

1. What owns this object, and when does it die?
2. Can this callback outlive its receiver?
3. Is anything blocking the GUI thread?
4. Is this error a value or an exception? Does it cross a slot?
5. Is the model updated with the right begin/end signals?
6. Is the `#ifdef` inside `platform/`?
7. Does this compile warning-free, clang-tidy-clean, and within budget?
