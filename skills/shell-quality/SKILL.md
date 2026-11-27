---
name: shell-quality
description: Review or fix Bash and POSIX sh scripts for unsafe expansions, exit-status handling, cleanup, destructive filesystem operations, and portability. Use for shell diagnostic triage or script verification.
---

# Shell Quality

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Review | Leave files untouched and use applicable local syntax checks, ShellCheck and configured formatting checks. |
| Fix | Apply edits only for requested fixes within the affected behavior. |
| Verification | Exercise behavior only in an isolated fixture after inspecting effects. |

## Workflow

1. Start with the changed script and its entry points, callers and sourced files. Inventory other scripts only for a full audit.
2. Identify actual interpreters and versions from shebangs, invocations, CI and build runners.
3. Trace arguments, expansions, pipelines, exit codes and cleanup through both success and failure paths.
4. Inspect operations on files and services before invoking the script.
5. Load relevant references according to the task.
6. Perform checks or requested fixes within the selected operating mode. Use temporary directories and controlled command stubs for destructive or network-dependent paths.
7. Save complete non-sensitive logs locally and summarize relevant diagnostics.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Shell behavior and portability](references/shell-review.md) | Diagnosing shell semantics, expansions, exit status or portability issues. |
| [Verification cases](references/verification.md) | Selecting verification commands or testing a fix. |
| [Processes and traps](references/process-lifecycle.md) | Reviewing background jobs, signal handling, traps, or cleanup status. |

## Constraints

- Keep supported interpreters, argument semantics, output and exit codes compatible.
- Contain fixes to the affected expansion, status check or cleanup path.
- Require a demonstrated need before adding a new runtime dependency or refactoring the script.
- Treat command-runner evaluation as a build automation concern.
- Use this workflow for the shell actually invoked, including recipe bodies where relevant.

## Expected Output

For each finding, report:

- Severity and file location.
- Failing arguments or exit status.
- Practical impact.
- Smallest applicable fix.
- Reproducible verification check.
