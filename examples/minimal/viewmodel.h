#pragma once

#include <QObject>
#include <QString>

// The ViewModel owns the state and the commands; the View only binds.
class CounterViewModel : public QObject {
  Q_OBJECT
  Q_PROPERTY(int count READ count NOTIFY countChanged)
  Q_PROPERTY(QString status READ status NOTIFY statusChanged)

 public:
  explicit CounterViewModel(QObject* parent = nullptr);

  [[nodiscard]] int count() const;
  [[nodiscard]] QString status() const;

  Q_INVOKABLE void increment();

 signals:
  void countChanged();
  void statusChanged();

 private:
  int m_count = 0;
};
