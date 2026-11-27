# Rollout Checklist

| Strategy | Consider when |
| --- | --- |
| Recreate | Downtime is explicitly acceptable. |
| Rolling | Old and new instances can coexist safely. |
| Blue-green | Parallel environments and a controlled traffic switch are feasible. |
| Canary | Representative traffic and meaningful comparison signals are available. |

## Preflight and recovery

- Confirm the artifact digest, target environment, configuration, dependencies, and authorization.
- Define readiness and business-level checks with a bounded observation window.
- Verify backward and forward compatibility for mixed-version operation.
- Separate reversible application changes from irreversible data changes. Establish backup and recovery evidence when needed.
- Define stop and rollback criteria before execution. If rollback is unsafe, plan a compatible forward recovery.
- Inspect partial rollout state before retrying; avoid duplicate effects.

## Gotchas

- Running processes are not proof of readiness or correctness.
- Rolling back an image does not restore a migrated database.
- A successful deployment command is not proof that traffic reaches the expected revision.

## Official guidance

- [Kubernetes deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
