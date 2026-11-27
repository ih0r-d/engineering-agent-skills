---
name: deployment
description: Plan, review, or verify software deployment and rollout procedures. Use for environment promotion, rollout strategies, runtime readiness, migrations, rollback, and deployment verification.
---

# Deployment

## Workflow

1. Identify the target environment, approved artifact identity, deployment mechanism, current version, dependencies, and operational constraints.
2. Inspect existing deployment configuration and evidence. Identify readiness checks, migration compatibility, state ownership, and failure signals.
3. Choose the least complex rollout strategy that meets availability and recovery requirements. Load the rollout reference for migration and rollback decisions.
4. Define preflight checks, rollout checkpoints, stop conditions, recovery actions, and post-deployment verification.
5. Execute only specifically authorized actions against confirmed targets; otherwise return the plan. Stop when a gate fails or the environment differs from the approved plan.
6. Verify actual artifact identity, health, and representative behavior before reporting success.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/rollout-checklist.md) | Task-specific decisions require additional guidance. |

## Constraints

- Default to planning or read-only review. Do not deploy, roll back, migrate data, or modify live infrastructure without explicit authorization.
- Never assume rollback is safe after irreversible schema or data changes.
- Do not expose credentials or use production data in test environments.
- Do not invent successful health checks or operational metrics.
- Keep artifact publication with release engineering and pipeline implementation with CI/CD.

## Expected Output

Report target, artifact, rollout steps, gates, failure thresholds, recovery plan, verification evidence, and remaining risks.
