---
name: task-decomposition
description: Break an established engineering objective into independently verifiable work items with dependencies, scope, and acceptance criteria. Use for backlog slicing, milestones, and sequencing deliverables.
---

# Task Decomposition

## Workflow

1. Identify the objective, approved scope, constraints, and known dependencies. Reuse existing requirements and plans.
2. Split work into coherent deliverables with observable outcomes. Prefer vertical slices where they reduce integration risk.
3. Define each item's scope, acceptance criteria, prerequisites, and verification. Load the reference when dependency ordering or slicing is unclear.
4. Identify critical dependencies, parallelizable work, and integration checkpoints. Separate discovery tasks from implementation commitments.
5. Check that the items collectively cover the objective without duplication or hidden prerequisites.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/decomposition-checklist.md) | Task-specific decisions require additional guidance. |

## Constraints

- Do not invent ticket IDs, owners, deadlines, or estimates.
- Do not create remote tickets or modify code without authorization.
- Avoid splitting trivial work into unnecessary tasks or mixing unrelated deliverables.
- Keep detailed technical implementation decisions in implementation planning.

## Expected Output

Return ordered work items with outcomes, scope, dependencies, acceptance criteria, verification, and unresolved blockers.
