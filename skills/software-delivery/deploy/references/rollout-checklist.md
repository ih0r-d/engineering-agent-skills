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
- For a schema change, use expand-and-contract when old and new application versions must coexist: add compatible schema first, deploy code that tolerates both forms, migrate data in bounded observable steps, then remove obsolete schema only after old consumers are gone. Adapt the sequence to the database and availability constraints; destructive changes need a separately verified recovery plan.
- Define observable success and failure thresholds before rollout, including representative consumer behavior and a bounded observation window. Stop on a failed gate and preserve artifact, revision, and environment identity for diagnosis.
- After deployment, verify actual traffic reaches the expected revision and that errors, latency, saturation, and key business outcomes remain within the agreed limits. A successful command or healthy process is not sufficient evidence.
- Choose rollback versus roll-forward based on data and external side effects. Rollback is useful only when the old application remains compatible with current state; otherwise use a tested forward correction and explicitly communicate the decision.

## Gotchas

- Running processes are not proof of readiness or correctness.
- Rolling back an image does not restore a migrated database.
- A successful deployment command is not proof that traffic reaches the expected revision.

## Official guidance

- [Kubernetes deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
