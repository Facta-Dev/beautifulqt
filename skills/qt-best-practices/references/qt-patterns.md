# Qt patterns

The patterns a Qt desktop app needs, with the failure mode each prevents.

## 1. The bindable ViewModel

```cpp
class InventoryViewModel : public QObject {
  Q_OBJECT
  Q_PROPERTY(Status status READ status NOTIFY statusChanged)
  Q_PROPERTY(QAbstractItemModel* model READ model CONSTANT)
public:
  enum class Status { Loading, Ready, Empty, Forbidden, NotFound, Offline, Error, PolicyBlocked };
  Q_ENUM(Status)

  explicit InventoryViewModel(InventoryUseCases useCases, QObject* parent = nullptr);

  Status status() const { return m_status; }
  QAbstractItemModel* model() const { return m_model.get(); }
  Q_INVOKABLE void refresh();

signals:
  void statusChanged();

private:
  void setStatus(Status next);
  InventoryUseCases m_useCases;
  std::unique_ptr<InventoryModel> m_model;
  Status m_status = Status::Loading;
};
```

- One closed status enum; a switch that misses a value is a compile warning
  turned error.
- Commands are `Q_INVOKABLE`; the View binds or connects; no widget import.
- ViewModel tests use `QSignalSpy` and fake use cases.

## 2. The model

- Subclass `QAbstractListModel`/`QAbstractTableModel`.
- Emit `beginInsertRows`/`endInsertRows`, `dataChanged`, and only reset for a
  full replacement.
- `roleNames()` exposes typed roles; QML binds them by name.
- A proxy handles sort/filter; the view never re-sorts.

## 3. The async use case

- The ViewModel calls a use case returning `QFuture<Result<T>>`.
- Connect the future's `then`/watcher to a queued slot; apply the result on
  the GUI thread.
- Keep a generation counter or the last request id; a stale result is dropped.
- Cancellation aborts the reply/task and clears the pending state.

## 4. The outbox

1. Write the optimistic row and the queued mutation in one SQLite transaction.
2. Send with an idempotency key.
3. On success, apply the server's answer and settle the row.
4. On failure, restore the previous value and show why.
5. Drain on startup, reconnect and a timer; a dead-letter view for admins.

## 5. The realtime port

```cpp
class RealtimePort {
public:
  virtual ~RealtimePort() = default;
  virtual void start(const RealtimeConfig& config) = 0;
  virtual void stop() = 0;
  virtual void setTopics(const QSet<QString>& topics) = 0;
signals:
  void stateChanged(RealtimeState state);
  void eventReceived(const EventEnvelope& event);
  void resyncRequired();
};
```

- Adapters: SSE, WebSocket, polling; the same state machine and envelope.
- Snapshot + stream, dedupe by event id, resume tokens, heartbeats, backoff.
- The app is fully correct with polling or no streaming.

## 6. The Navigator and Notifier ports

- Navigation is by route (`Route` value type), not by window pointer.
- The ViewModel emits `navigate(Route)`; the shell resolves it.
- Notifications go through a `NotifierPort`; the ViewModel does not know
  whether it is a tray balloon, a toast or a dialog.

## 7. Single-instance and OS events

- `QLocalServer`/`QLocalSocket` for a second launch: forward the args and
  exit.
- Tray, deep links, power/network changes enter through `platform/` adapters
  and become application events.
- The GUI thread only handles the UI reaction.

## 8. Secure storage

- Tokens in the OS keystore behind `SecretStorePort` (Windows Credential
  Manager, macOS Keychain, libsecret).
- SQLite/config hold no secrets.
- Clear on sign-out and tenant switch.

## 9. Performance patterns

- Lazy-load heavy screens; keep startup light.
- Model + proxy instead of a widget per row.
- Size pixmaps for the target DPI; no per-paint allocations.
- Measure cold start, screen switch, scroll FPS and memory on the floor.
- No WebEngine in the main app; no GPU assumption.

## 10. Testing patterns

- Qt Test for units and GUI; `QSignalSpy` for ViewModels.
- Fake ports, no real network/disk in a unit test.
- SQLite migrations against fixtures of every released version.
- A performance budget test in CI on the reference machine.
