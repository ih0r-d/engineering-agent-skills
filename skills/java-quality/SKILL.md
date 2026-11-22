---
name: java-quality
description: Evidence-based Java code reviews and focused fixes for correctness, maintainability, public APIs, generated code, and build/tool quality. Use when asked to audit or improve Java code.
---

# Java Quality

Review Java code for correctness, contributor experience, and maintainability across commercial, personal, and open-source repositories. Enforce useful invariants without mechanical overengineering.

## Workflow

1. Determine scope (diff, component, or repository), requested mode (review versus fix), applicable JDK, and project rules. Inspect Git status first; preserve other work.
2. Investigate code, call sites, tests, generated output, concurrency, resource ownership, public API, and actual consumer behavior. Prefer confirmed issues over style guesses.
3. Read [quality-rubric.md](references/quality-rubric.md) for applicable checks; read [static-analysis.md](references/static-analysis.md) only when quality tools or IDE-style warnings are relevant.
4. Review findings as `P0/P1/P2 | path:line | evidence | impact | smallest safe fix | verification`. Distinguish verified problems from possible risks.
5. For requested fixes only, follow [review-workflow.md](references/review-workflow.md) and [anti-overengineering.md](references/anti-overengineering.md). Make localized changes and focused regression tests.
6. Re-run existing formatter, compiler, tests, static analyzers, and API compatibility checks where available; don't weaken existing gates.
7. Report PASS/FAIL/BLOCKED/NOT RUN honestly. Never auto-commit, push, or change build dependencies without permission.

## Constraints

- Don't assume Maven, Gradle, Spring, a particular JDK, or a tool installation. Discover the project's actual configuration.
- Existing tools may include SpotBugs, SonarQube, Checkstyle, Error Prone, PMD/CPD, or ArchUnit. Use them if configured or locally runnable; don't promise an analyzer is universal without its requirements.
- For generated code, fix its generator and compile generated consumers when relevant.
- Preserve source/binary/behavioral compatibility unless a breaking change is explicitly requested.
- Don't introduce arbitrary method-length quotas, speculative abstractions, blanket suppressions, or large cosmetic refactors.
