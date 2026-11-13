#include <QObject>

// The clean control: no violations. CI proves clang-tidy reports nothing here.
class CleanCounter : public QObject {
 public:
  explicit CleanCounter(QObject* parent = nullptr) : QObject(parent) {}

  [[nodiscard]] int value() const { return m_value; }
  void increment() { ++m_value; }

 private:
  int m_value = 0;
};
