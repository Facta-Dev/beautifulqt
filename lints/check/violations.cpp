#include <QObject>
#include <string>

// Deliberate violations for the CI harness. Do not copy this file.
// Each block is expected to be flagged; the clean control must stay quiet.

class Base : public QObject {
 public:
  virtual void run() {}
};

class MissingOverride : public Base {
 public:
  void run() {}  // modernize-use-override
};

void owningRawPointer() {
  auto* value = new int(1);  // cppcoreguidelines-owning-memory
  (void)value;
}

void cStyleCast(double value) {
  int truncated = (int)value;  // cppcoreguidelines-pro-type-cstyle-cast
  (void)truncated;
}

void copyInsteadOfConstRef(const std::string value) {  // performance-unnecessary-value-param
  (void)value;
}

void emptyBranch(bool condition) {
  if (condition) {
  }  // readability-*
}
