#include <QApplication>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

#include "viewmodel.h"

int main(int argc, char** argv) {
  QApplication app(argc, argv);
  CounterViewModel viewModel;

  QWidget window;
  auto* layout = new QVBoxLayout(&window);
  auto* label = new QLabel(QStringLiteral("0"));
  auto* button = new QPushButton(QStringLiteral("Increment"));

  QObject::connect(&viewModel, &CounterViewModel::countChanged, label,
                   [&viewModel, label] { label->setText(QString::number(viewModel.count())); });
  QObject::connect(button, &QPushButton::clicked, &viewModel, &CounterViewModel::increment);

  layout->addWidget(label);
  layout->addWidget(button);
  window.show();
  return app.exec();
}
