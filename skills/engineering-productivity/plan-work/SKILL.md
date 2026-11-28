---
name: plan-work
description: Plan implementation or decompose an approved engineering objective into verifiable work items. Use for sequencing a scoped change, delivery slices, backlog dependencies, migration, and verification planning.
---

# Plan Work

## Workflow

1. Identify the approved outcome, scope, constraints, and acceptance criteria. Reuse existing requirements and plans. Inspect relevant callers, contracts, tests, and configuration when available. Honor explicit technology constraints and record unknowns.
2. For a scoped implementation plan, identify the smallest viable change, affected boundaries, and dependencies. Compare options where they materially affect risk or complexity. Name files only where evidence supports them.
3. For work decomposition, split the objective into cohesive deliverables, each with scope, prerequisites, acceptance criteria, and its own verification. Prefer vertical slices when they reduce integration risk. Keep discovery distinct from implementation commitments.
4. Order the work by dependency, compatibility, and rollout needs. Identify parallelizable work, integration checkpoints, baseline and incremental checks, and recovery steps where relevant.
5. Verify that the plan covers the accepted scope without duplication, hidden dependencies, or unsupported estimates. Identify unresolved prerequisites and decisions that block execution.

## Reference selection

- Use the [planning checklist](references/planning-checklist.md) for risky sequences, compatibility, migrations, or recovery decisions.
- Use the [decomposition checklist](references/decomposition-checklist.md) when slicing a backlog, allocating acceptance criteria, or resolving dependency order.

## Boundaries and result

Planning provides no authorization to edit, stage, install, create tickets, or perform remote actions. Avoid speculative abstractions and unrelated cleanup. Return the requested sequence or work items with outcomes, scope, dependencies, verification, and unresolved blockers.
