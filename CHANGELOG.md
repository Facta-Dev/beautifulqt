# Changelog

All notable changes to this project are listed here. Versions follow
[Semantic Versioning](https://semver.org/), and the version lives in
`.claude-plugin/plugin.json`.

## [Unreleased]

### Added

- **Three skills for Qt 6 / C++20.** `qt-best-practices` steers new desktop
  code toward a sacred GUI thread, a widget-free domain/application, MVVM with
  bindable QObject ViewModels, QAbstractItemModel lists, ownership and
  lifetimes, the async SDK and realtime ports, SQLite and the outbox, signed
  updates, accessibility and the low-end performance budget. `qt-review`
  reviews a screen, ViewModel, model, thread boundary, adapter, CMake graph or
  diff and ranks architecture and GUI-thread contracts first. `qt-port` ports
  Qt 5, QML, PySide/PyQt, Electron or web screens to Qt 6 C++.
- **A drop-in clang-tidy and clang-format config.** `lints/.clang-tidy` pins
  the bugprone/performance/modernize/readability checks, the reviewed
  cppcoreguidelines subset and the Qt checks, with warnings as errors;
  `lints/.clang-format` is the formatter.
- **A runnable example and proof gates.** `examples/minimal/` is a Qt Widgets
  app with a ViewModel and a QTest; `scripts/check-build.sh` compiles and
  tests it when Qt is installed. `scripts/check-lints.sh` runs clang-format
  and clang-tidy, with a visible SKIP when a tool is absent.
- **A validator and a test suite.** `scripts/check-skill.py` checks
  frontmatter, links, eval cases and the plugin manifests; the offline
  `scripts/check-examples.py` checks every C++ block; `tests/` covers the
  validator, wording, lints config and gates.
- **A worked review.** `examples/review-inventory.md` shows the report shape
  and the architecture-first ranking on a small inventory window.

[Unreleased]: https://github.com/Facta-Dev/beautifulqt/compare/v0.1.0...HEAD
