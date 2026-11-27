---
name: python-quality
description: Review Python code, imports, typing, packaging, and tests for runtime or API regressions. Use for focused Python fixes, pytest verification, or Ruff, Pyright and mypy diagnostic triage.
---

# Python Quality

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Review | Inspect and report findings without modifying repository files. |
| Fix | Change the affected behavior and its tests when requested. |
| Verification | Use existing commands and report their actual coverage. |

## Workflow

1. Start with the requested diff or module and its callers and tests. For a full audit, inventory packages, entry points and test environments.
2. Determine the supported Python versions from packaging and CI. Identify how the project selects its interpreter, environment and dependency groups.
3. Trace the actual import and call paths, including installed-package behavior where relevant. Check failure, cleanup, cancellation, mutation and compatibility at the boundaries the change touches.
4. Load relevant references according to the task.
5. Prefer existing Ruff, Pyright or mypy settings and targeted pytest runs. Verify analyzer findings against runtime behavior and supported versions.
6. Keep full non-sensitive logs locally and rerun only when inputs or check conditions change.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Runtime and API review](references/quality-rubric.md) | Reviewing language semantics, typing or lifecycle behavior. |
| [Packaging and checks](references/packaging-and-checks.md) | Reviewing installed artifacts, analyzer configuration or verification procedures. |
| [Asyncio lifecycle](references/asyncio.md) | Tracing task ownership, cancellation, timeouts, or blocking work on an event loop. |
| [Typing contracts](references/typing.md) | Evaluating generic API variance, protocols, narrowing, or runtime validation boundaries. |

## Constraints

- Follow local project instructions for dependencies and configuration.
- Keep public signatures, imports and exception behavior stable during fixes.
- Prefer direct control flow and existing types over new frameworks, protocols or wrappers introduced for a single diagnostic.
- Treat formatting as a configured check or an explicit formatting task.

## Expected Output

For each finding, report:

- Severity and file location.
- Failing input or caller.
- Observed or established effect.
- Smallest applicable fix.
- Verification.

Identify gaps in the environment or coverage.
