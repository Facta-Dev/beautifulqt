# A worked review: the inventory window

The subject is a small Qt Widgets inventory window. It loads, it shows rows,
and it has five findings that a review must rank in a useful order. The fixed
version follows the contract in `qt-best-practices`.

## The module under review

```cpp
// inventoryview.cpp
void InventoryView::refresh() {
  QNetworkAccessManager manager;
  QNetworkRequest request(QUrl(QStringLiteral("https://api.example.com/v1/inventory")));
  request.setRawHeader("Authorization", QByteArray("Bearer ") + m_token);
  QNetworkReply* reply = manager.get(request);
  reply->waitForFinished();

  const QByteArray body = reply->readAll();
  m_rows.clear();
  const auto parsed = QJsonDocument::fromJson(body).array();
  for (const auto& value : parsed) {
    m_rows.append(value.toObject());
  }
  m_table->setRowCount(static_cast<int>(m_rows.size()));
  for (int row = 0; row < m_rows.size(); ++row) {
    m_table->setItem(row, 0, new QTableWidgetItem(m_rows.at(row).value("name").toString()));
  }
}
```

## The report

### Verdict

The window works on a fast network and a local API, and freezes the GUI on a
slow one. Not safe to ship; the GUI-thread violation is first because it is
the one every screen copies.

### Must fix

1. `inventoryview.cpp:2` — the **View** creates a `QNetworkAccessManager` and
   builds a raw request with the token. Rule: *views never touch the SDK,
   storage or network; the ViewModel calls a use case*. Fix: `refresh()` on
   the ViewModel; the SDK adapter owns the network and the token.
2. `inventoryview.cpp:6` — `waitForFinished()` blocks the GUI thread. Rule:
   *the GUI thread never blocks*. Fix: an async use case returning
   `QFuture<Result<InventoryPage>>`; apply the result in a queued slot.
3. `inventoryview.cpp:2` — `manager` and `reply` are locals; the reply is
   leaked and the manager dies at the end of the function. Rule: *RAII and
   QObject parent-child own everything; no raw owning pointer*. Fix: the
   adapter keeps the reply in a `QNetworkReply*` with `deleteLater` and
   aborts it on supersede.
4. `inventoryview.cpp:14` — the table is rebuilt row by row and the model is
   reset on every refresh, losing selection and scroll. Rule: *a list is a
   `QAbstractItemModel` updated with the right begin/end signals*. Fix: a
   model with `setRows`, `beginResetModel` only for a full replacement.
5. `inventoryview.cpp:9` — an empty array, a 403 and a network failure all
   render the same blank table. Rule: *one closed status enum; every status
   is rendered*. Fix: `Loading | Ready | Empty | Forbidden | NotFound |
   Offline | Error | PolicyBlocked`.

### Should fix

6. `inventoryview.cpp:3` — the token is read in the view and put in a header
   by hand. Fix: the SDK adapter reads the `SecretStore` port; the view never
   sees a token.
7. `inventoryview.cpp:14` — per-paint widget allocation; a
   `QTableWidgetItem` per cell is expensive on old hardware. Fix: a model and
   a view (or a delegate).
8. `inventoryview.cpp:2` — the URL is hard-coded; it belongs to the SDK's
   base URL and the route contract.

### Waived gates

None. The diff does not touch the lint config, the tests, or the performance
budget.

## The fixed module

```cpp
// inventoryviewmodel.h
class InventoryViewModel : public QObject {
  Q_OBJECT
  Q_PROPERTY(Status status READ status NOTIFY statusChanged)
  Q_PROPERTY(QAbstractItemModel* model READ model CONSTANT)
 public:
  enum class Status { Loading, Ready, Empty, Forbidden, NotFound, Offline, Error, PolicyBlocked };
  Q_ENUM(Status)
  explicit InventoryViewModel(InventoryUseCases useCases, QObject* parent = nullptr);
  Q_INVOKABLE void refresh();
 signals:
  void statusChanged();
 private:
  void setStatus(Status next);
  InventoryUseCases m_useCases;
  std::unique_ptr<InventoryModel> m_model;
  Status m_status = Status::Loading;
  quint64 m_requestId = 0;
};
```

```cpp
// inventoryviewmodel.cpp
void InventoryViewModel::refresh() {
  setStatus(Status::Loading);
  const quint64 requestId = ++m_requestId;
  m_useCases.listInventory().then(this, [this, requestId](const Result<InventoryPage>& result) {
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

```cpp
// inventorymodel.cpp — the model owns the rows; the view never rebuilds it.
void InventoryModel::setRows(const QList<InventoryRow>& rows) {
  beginResetModel();
  m_rows = rows;
  endResetModel();
}
```

## What changed, and why it matters

| Finding | The fixed version |
|---|---|
| View builds a request and holds the token | the SDK adapter owns the network and the keystore |
| `waitForFinished` on the GUI thread | async use case + queued result |
| Local manager/reply leaked | the adapter owns the reply and aborts it |
| Table rebuilt per refresh | a model with `setRows` |
| Blank table for empty/403/network | one status enum, every status rendered |
| Per-cell widget allocation | model + view/delegate |

The review is short on purpose. Five Must-fix findings, each with a location,
a rule, and a fix, is a better review than twenty comments that repeat the
same contract in different words.
