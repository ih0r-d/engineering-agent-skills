---
name: shell-quality
description: Review or fix Bash and POSIX sh scripts for unsafe expansions, exit-status handling, cleanup, destructive filesystem operations, and portability. Use for shell diagnostic triage or script verification.
---

# Shell Quality

1. Start with the changed script and its entry points, callers and sourced files. Inventory other scripts only for a full audit. Identify actual interpreters and versions from shebangs, invocations, CI and build runners.
2. Trace arguments, expansions, pipelines, exit codes and cleanup through both success and failure paths. Inspect operations on files and services before invoking the script. Read [shell behavior and portability](references/shell-review.md) for diagnosis and [verification cases](references/verification.md) when selecting commands or testing a fix.
3. In review mode, leave files untouched and use applicable local syntax checks, ShellCheck and configured formatting checks. In verification mode, exercise behavior only in an isolated fixture after inspecting effects. Use temporary directories and controlled command stubs for destructive or network-dependent paths.
4. Apply edits only for requested fixes. Keep supported interpreters, argument semantics, output and exit codes compatible. Contain fixes to the affected expansion, status check or cleanup path. Require a demonstrated need before adding a new runtime dependency or refactoring the script.
5. Report severity, file and line, failing arguments or exit status, practical impact, the smallest fix and a reproducible check. Save complete non-sensitive logs locally and summarize relevant diagnostics.

Treat command-runner evaluation as a build automation concern. Use this workflow for the shell actually invoked, including recipe bodies where relevant.
