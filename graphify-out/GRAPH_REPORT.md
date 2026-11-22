# Graph Report - .  (2026-11-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 737 nodes · 960 edges · 100 communities (61 shown, 39 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `44795b1a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CheckSkillTests
- Path
- interface
- CounterViewModel
- What You Must Do When Invoked
- YamlParser
- Qt best practices
- 2. Categories, in ranking order
- Beautiful Qt
- Qt 6 platform digest
- Qt patterns
- Contributing
- violations.cpp
- Qt architecture contract
- BestPractices
- README.md
- A worked review: the inventory window
- graphify reference: extra exports and benchmark
- check_repo
- C++ strict for Qt
- Qt port
- TidyConfig
- PackageTests
- run
- `<app>` Packaging Reviewer
- `<app>` Qt Threading Reviewer
- `<app>` Widgets UI Reviewer
- `<app>` Architect
- `<app>` Build Resolver
- `<app>` Code Explorer
- `<app>` Code Reviewer
- `<app>` Planner
- `<app>` TDD Guide
- `<app>` Platform Boundary Reviewer
- `<app>` Test Author
- `<app>` add-linux-packaging skill
- `<app>` add-slice skill
- `<app>` add-view skill
- <app> Claim Check skill
- <app> Clean-Room Rebuild skill
- <app> Corpus Retrieval skill
- <app> Diagnosing Bugs skill
- <app> Domain Modeling skill
- <app> Grilling skill
- `<app>` learn skill
- `<app>` plan skill
- `<app>` platform-port skill
- <app> Research skill
- `<app>` review skill
- `<app>` ship skill
- `<app>` spec skill
- <app> Test-Driven Development skill
- <app> Verified Status skill
- <app> Visual Review skill
- graphify reference: query, path, explain
- build
- beautifulqt — agent instructions
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Install
- guard-bash.sh
- /add-linux-packaging
- /add-slice
- /add-view
- /claim-check
- /clean-room-rebuild
- /corpus-retrieval
- /diagnosing-bugs
- /domain-modeling
- /grilling
- /learn
- /plan
- /platform-port
- /research
- /review
- /ship
- /spec
- /tdd
- /verified-status
- /visual-review
- Playbooks for `beautifulqt` — load on demand
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- check-lints.sh
- CLAUDE.md
- README.md
- CREDITS.md
- CREDITS.md
- CREDITS.md
- CREDITS.md
- CREDITS.md
- extraction-spec.md
- CREDITS.md
- CREDITS.md
- CREDITS.md
- CREDITS.md
- CREDITS.md
- check-build.sh

## God Nodes (most connected - your core abstractions)
1. `CheckSkillTests` - 37 edges
2. `build_valid_repo()` - 32 edges
3. `Checker` - 26 edges
4. `write()` - 24 edges
5. `YamlParser` - 16 edges
6. `Qt best practices` - 16 edges
7. `Beautiful Qt` - 15 edges
8. `interface` - 14 edges
9. `What You Must Do When Invoked` - 12 edges
10. `add_portable_plugin()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `count`  [INFERRED]
  examples/minimal/main.cpp → examples/minimal/viewmodel.h
- `ViewModelTest::incrementsAndNotifies()` --calls--> `count`  [INFERRED]
  examples/minimal/test_viewmodel.cpp → examples/minimal/viewmodel.h
- `ViewModelTest::incrementsAndNotifies()` --calls--> `increment`  [INFERRED]
  examples/minimal/test_viewmodel.cpp → examples/minimal/viewmodel.h
- `ViewModelTest::incrementsAndNotifies()` --calls--> `status`  [INFERRED]
  examples/minimal/test_viewmodel.cpp → examples/minimal/viewmodel.h

## Import Cycles
- None detected.

## Communities (100 total, 39 thin omitted)

### Community 0 - "CheckSkillTests"
Cohesion: 0.16
Nodes (10): add_portable_plugin(), build_valid_repo(), CheckSkillTests, error_messages(), formatted(), load_checker(), png_header(), portable_with() (+2 more)

### Community 1 - "Path"
Cohesion: 0.16
Nodes (19): Any, check_repo(), Checker, _fold_block(), format_problem(), _is_relative(), _json_key_line(), main() (+11 more)

### Community 2 - "interface"
Cohesion: 0.07
Nodes (29): author, name, url, interface, publication, description, extensions, com.openai (+21 more)

### Community 3 - "CounterViewModel"
Cohesion: 0.09
Nodes (21): main(), QObject, ViewModelTest, ViewModelTest::incrementsAndNotifies(), private, CounterViewModel, count, countChanged (+13 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 5 - "YamlParser"
Cohesion: 0.25
Nodes (6): Exception, _parse_quoted(), Small YAML subset: maps, lists, quoted scalars, | and > blocks., _split_flow(), YamlError, YamlParser

### Community 6 - "Qt best practices"
Cohesion: 0.12
Nodes (16): 10. Security, 11. Performance, 12. Accessibility and internationalization, 13. Testing, 14. Cross-skill contract, 1. Mindset, 2. Before you hand back code, 3. The GUI thread and threading (+8 more)

### Community 7 - "2. Categories, in ranking order"
Cohesion: 0.12
Nodes (15): 1. Report shape, 2. Categories, in ranking order, 3. Waived gates, 4. How to review, 5. Worked example, 6. Cross-skill contract, Accessibility and i18n, Architecture contracts (always Must fix, ranked first) (+7 more)

### Community 8 - "Beautiful Qt"
Cohesion: 0.14
Nodes (14): A worked example, Agent kit (Claude Code), Architecture diagrams, Beautiful Qt, Contributing, License, Repository layout, Siblings (+6 more)

### Community 9 - "Qt 6 platform digest"
Cohesion: 0.17
Nodes (11): 10. Testing, 1. Versions, 2. Widgets vs Qt Quick, 3. The GUI thread, 4. Model/view, 5. Networking and async, 6. CMake, 7. Packaging and updates (+3 more)

### Community 10 - "Qt patterns"
Cohesion: 0.17
Nodes (11): 10. Testing patterns, 1. The bindable ViewModel, 2. The model, 3. The async use case, 4. The outbox, 5. The realtime port, 6. The Navigator and Notifier ports, 7. Single-instance and OS events (+3 more)

### Community 11 - "Contributing"
Cohesion: 0.18
Nodes (9): Added, Changelog, [Unreleased], Contributing, Good first contributions, License, Making a change, Style (+1 more)

### Community 12 - "violations.cpp"
Cohesion: 0.22
Nodes (5): Base, copyInsteadOfConstRef(), QObject, MissingOverride, string

### Community 13 - "Qt architecture contract"
Cohesion: 0.18
Nodes (11): 10. The enforcement map, 1. The layers, 2. Ports, 3. CMake target graph, 4. Slices, 5. MVVM, 6. Threading, 7. Security and policy (+3 more)

### Community 14 - "BestPractices"
Cohesion: 0.29
Nodes (4): BestPractices, bp_body(), ReviewSkill, rv_body()

### Community 15 - "README.md"
Cohesion: 0.20
Nodes (5): beautifulqt — Architecture Diagrams, Beautiful Qt lints, Running it, The check project, Privacy policy

### Community 16 - "A worked review: the inventory window"
Cohesion: 0.20
Nodes (9): A worked review: the inventory window, Must fix, Should fix, The fixed module, The module under review, The report, Verdict, Waived gates (+1 more)

### Community 17 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 18 - "check_repo"
Cohesion: 0.39
Nodes (8): check_balance(), check_repo(), cpp_blocks(), doc_files(), main(), Path, Yield (start_line, code) for each cpp/c++ fenced block., Return (line_offset, message) or None. Comments/literals are skipped.

### Community 19 - "C++ strict for Qt"
Cohesion: 0.22
Nodes (8): 1. The subset, 2. Ownership and lifetimes, 3. Errors as values, 4. Threading, 5. Qt specifics, 6. Warnings and lint, 7. Review questions, C++ strict for Qt

### Community 20 - "Qt port"
Cohesion: 0.22
Nodes (8): 1. The order of work, 2. Qt 5 → Qt 6 mapping, 3. PySide/PyQt → C++ Qt, 4. Electron/web → Qt, 5. Behavior parity checklist, 6. What not to do, 7. Cross-skill contract, Qt port

### Community 23 - "run"
Cohesion: 0.36
Nodes (4): CompletedProcess, BuildGate, Gates, run()

### Community 24 - "`<app>` Packaging Reviewer"
Cohesion: 0.29
Nodes (6): `<app>` Packaging Reviewer, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 25 - "`<app>` Qt Threading Reviewer"
Cohesion: 0.29
Nodes (6): `<app>` Qt Threading Reviewer, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 26 - "`<app>` Widgets UI Reviewer"
Cohesion: 0.29
Nodes (6): `<app>` Widgets UI Reviewer, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 27 - "`<app>` Architect"
Cohesion: 0.29
Nodes (6): `<app>` Architect, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 28 - "`<app>` Build Resolver"
Cohesion: 0.29
Nodes (6): `<app>` Build Resolver, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 29 - "`<app>` Code Explorer"
Cohesion: 0.29
Nodes (6): `<app>` Code Explorer, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 30 - "`<app>` Code Reviewer"
Cohesion: 0.29
Nodes (6): `<app>` Code Reviewer, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 31 - "`<app>` Planner"
Cohesion: 0.29
Nodes (6): `<app>` Planner, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 32 - "`<app>` TDD Guide"
Cohesion: 0.29
Nodes (6): `<app>` TDD Guide, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 33 - "`<app>` Platform Boundary Reviewer"
Cohesion: 0.29
Nodes (6): `<app>` Platform Boundary Reviewer, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 34 - "`<app>` Test Author"
Cohesion: 0.29
Nodes (6): `<app>` Test Author, Core Mission, Expertise Areas, Guiding Principles, Output Format, Quality Standards

### Community 35 - "`<app>` add-linux-packaging skill"
Cohesion: 0.29
Nodes (6): `<app>` add-linux-packaging skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 36 - "`<app>` add-slice skill"
Cohesion: 0.29
Nodes (6): `<app>` add-slice skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 37 - "`<app>` add-view skill"
Cohesion: 0.29
Nodes (6): `<app>` add-view skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 38 - "<app> Claim Check skill"
Cohesion: 0.29
Nodes (6): <app> Claim Check skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 39 - "<app> Clean-Room Rebuild skill"
Cohesion: 0.29
Nodes (6): <app> Clean-Room Rebuild skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 40 - "<app> Corpus Retrieval skill"
Cohesion: 0.29
Nodes (6): <app> Corpus Retrieval skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 41 - "<app> Diagnosing Bugs skill"
Cohesion: 0.29
Nodes (6): <app> Diagnosing Bugs skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 42 - "<app> Domain Modeling skill"
Cohesion: 0.29
Nodes (6): <app> Domain Modeling skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 43 - "<app> Grilling skill"
Cohesion: 0.29
Nodes (6): <app> Grilling skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 44 - "`<app>` learn skill"
Cohesion: 0.29
Nodes (6): `<app>` learn skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 45 - "`<app>` plan skill"
Cohesion: 0.29
Nodes (6): `<app>` plan skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 46 - "`<app>` platform-port skill"
Cohesion: 0.29
Nodes (6): `<app>` platform-port skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 47 - "<app> Research skill"
Cohesion: 0.29
Nodes (6): <app> Research skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 48 - "`<app>` review skill"
Cohesion: 0.29
Nodes (6): `<app>` review skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 49 - "`<app>` ship skill"
Cohesion: 0.29
Nodes (6): `<app>` ship skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 50 - "`<app>` spec skill"
Cohesion: 0.29
Nodes (6): `<app>` spec skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 51 - "<app> Test-Driven Development skill"
Cohesion: 0.29
Nodes (6): <app> Test-Driven Development skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 52 - "<app> Verified Status skill"
Cohesion: 0.29
Nodes (6): <app> Verified Status skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 53 - "<app> Visual Review skill"
Cohesion: 0.29
Nodes (6): <app> Visual Review skill, Core Principles, Output Format, Research References, Rules, When to Activate

### Community 54 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 55 - "build"
Cohesion: 0.53
Nodes (5): build(), main(), package_files(), Path, Files to package, relative to root, in a stable order.

### Community 56 - "beautifulqt — agent instructions"
Cohesion: 0.50
Nodes (3): beautifulqt — agent instructions, graphify, Model routing (Claude Code + Ollama)

### Community 57 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 58 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 59 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 60 - "Install"
Cohesion: 0.50
Nodes (4): Any agent, Claude Code, Install, OpenAI Codex and ChatGPT

### Community 61 - "guard-bash.sh"
Cohesion: 0.83
Nodes (3): has(), has_i(), guard-bash.sh script

## Knowledge Gaps
- **361 isolated node(s):** `private`, `Q_PROPERTY`, `countChanged`, `statusChanged`, `m_count` (+356 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Beautiful Qt` connect `Beautiful Qt` to `Install`, `README.md`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `Qt architecture contract` connect `Qt architecture contract` to `README.md`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `private`, `Q_PROPERTY`, `countChanged` to the rest of the system?**
  _367 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `interface` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `CounterViewModel` be split into smaller, more focused modules?**
  _Cohesion score 0.09359605911330049 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Qt best practices` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._