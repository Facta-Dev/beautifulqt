#include <QtTest>

#include "viewmodel.h"

class ViewModelTest : public QObject {
  Q_OBJECT

 private slots:
  void incrementsAndNotifies();
};

void ViewModelTest::incrementsAndNotifies() {
  CounterViewModel viewModel;
  QSignalSpy spy(&viewModel, &CounterViewModel::countChanged);
  QCOMPARE(viewModel.status(), QStringLiteral("empty"));

  viewModel.increment();

  QCOMPARE(viewModel.count(), 1);
  QCOMPARE(viewModel.status(), QStringLiteral("ready"));
  QCOMPARE(spy.count(), 1);
}

QTEST_GUILESS_MAIN(ViewModelTest)
#include "test_viewmodel.moc"
