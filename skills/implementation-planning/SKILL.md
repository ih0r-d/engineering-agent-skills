---
name: implementation-planning
description: Plan scoped software changes against established requirements and existing repository contracts. Use for implementation sequencing, affected components, verification, migration, and risk planning.
---

# Implementation Planning

## Workflow

1. Establish the approved outcome, constraints, and acceptance criteria. Inspect relevant entrypoints, callers, tests, and configuration.
2. Identify the smallest viable change and compare alternatives only where they materially affect risk or complexity.
3. Sequence changes according to dependencies, compatibility, and verification boundaries. Identify affected files when evidence supports them.
4. Define baseline checks, incremental verification, rollback or recovery needs, and unresolved prerequisites. Load the planning reference for risky changes.
5. Trace the plan to acceptance criteria. Flag unsupported estimates and stop at decisions that materially block execution.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/planning-checklist.md) | Task-specific decisions require additional guidance. |

## Constraints

- Planning does not authorize editing, staging, installation, or remote operations.
- Do not invent file paths, test results, dependencies, or delivery estimates.
- Avoid speculative abstractions and unrelated cleanup.
- Keep requirements elicitation, system design, and task backlog decomposition in their respective workflows.

## Expected Output

Return a scoped sequence of changes, affected contracts, prerequisites, verification steps, risks, and explicit exclusions.
