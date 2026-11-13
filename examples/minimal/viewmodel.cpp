#include "viewmodel.h"

CounterViewModel::CounterViewModel(QObject* parent) : QObject(parent) {}

int CounterViewModel::count() const { return m_count; }

QString CounterViewModel::status() const {
  return m_count == 0 ? QStringLiteral("empty") : QStringLiteral("ready");
}

void CounterViewModel::increment() {
  ++m_count;
  emit countChanged();
  emit statusChanged();
}
