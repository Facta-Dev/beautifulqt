# Contributing

Thanks for helping make BeautifulQt better. Issues and pull requests are
welcome. A few conventions keep the skills consistent and trustworthy.

## The one rule: every rule needs a source

The skills are a synthesis of published Qt, C++ and architecture guidance,
not a list of opinions. Each rule you add or change should trace back to one of
the sources in the README — the Qt 6 documentation, the facta desktop
handbook, or the C++ Core Guidelines — or to another source of similar weight,
such as the Qt bug tracker, the clang-tidy/clang-format docs, or a Qt RFC.
Link it in your pull request. If the sources disagree, say which one you
followed and why.

## Good first contributions

- **A rule the skills get wrong or miss.** Open a "Propose a rule" issue with
  the source, a short example of code the agent writes today, and what it
  should write instead.
- **A review false positive.** If `qt-review` flags something that's actually
  fine, open an issue with the code and the finding. These become new eval
  cases.
- **A new eval case.** A realistic prompt, the input files it needs, and one
  assertion per file. Open an issue and a maintainer will scaffold the case
  with you.
- **A broken install path.** Agents move their skill directories. If an
  install step in the README stopped working, a fix with a link to the agent's
  current docs is very welcome.

## Making a change

1. **Edit the skill.** Each skill is `skills/<name>/SKILL.md`. Keep it under
   about 500 lines; longer material belongs in `references/`. Explain why a
   rule matters, not just what it is.
2. **Keep the examples sane.** `python3 scripts/check-examples.py` checks that
   every C++ block in the skills and docs has balanced braces and literals.
   When Qt is installed, `bash scripts/check-build.sh` compiles and tests the
   runnable example.
3. **Check lint changes.** If you touch `lints/`, keep the check set in
   `.clang-tidy` aligned with the skill, and keep the deliberate violations in
   `lints/check/` flagged while the clean control stays quiet.
4. **Keep the wording contracts green.**
   `tests/test_skill_wording.py` pins the canonical phrases (the unbreakable
   clause, the `NOLINT`/clang-tidy listing, the review priority headings, and
   the `qt-review` cross-reference). If your change touches that wording,
   update the skill and the test in the same PR.
5. **Run the tests:** `python3 -m unittest discover -s tests -t .`.
6. **Validate the plugin** with `claude plugin validate .` from the repo root.
7. **Add a line to the Unreleased section of [CHANGELOG.md](CHANGELOG.md).**

## Style

- Write for an agent reading it mid-task: direct, imperative, one idea per
  bullet.
- Prefer a short code example to a paragraph of description.
- No Claude-specific instructions in the skills. They are standard Agent
  Skills and should work in any agent.

## License

By contributing, you agree your contribution is licensed under the MIT
license in [LICENSE](LICENSE).
