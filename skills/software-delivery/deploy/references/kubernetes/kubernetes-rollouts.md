# Kubernetes rollout review

Load when the repository has Kubernetes manifests or a deployment target is a Kubernetes cluster. Confirm the cluster version, namespace, context, workload controller, and rollout tooling before applying version-sensitive advice.

## Render and preflight

- Inspect the rendered manifests for the target environment, including image digest, replicas, selectors, configuration, service account, resources, probes, and migration jobs. Review the active context and namespace before any cluster command.
- Check a Deployment's rollout strategy and availability limits against the application's ability to run old and new versions concurrently. A rolling update can expose mixed versions; verify API, message, and schema compatibility for that interval.
- Treat startup, liveness, and readiness as different signals: startup gates the other probes during initialization; liveness should detect a condition restart can recover; readiness controls whether a pod receives service traffic. A liveness check coupled to a transient dependency can cause restart cascades.
- Check resource requests and limits against measured startup and steady-state needs. CPU throttling or memory limits can turn an otherwise valid probe threshold into repeated failure.
- Ensure termination handling stops new work and drains or completes in-flight work within the configured grace period. Verify that the process handles the container's termination signal and that pre-stop hooks do not substitute for application shutdown behavior.

## Observe and recover

- Observe rollout status, pod events, readiness, restarts, service endpoints, and representative application signals. A Ready pod or successful controller rollout is not proof of correct user behavior.
- Stop when the approved health threshold or observation window fails. Preserve events and revision identity, then distinguish a bad artifact, bad configuration, scheduling/resource issue, and dependency failure before selecting recovery.
- A controller rollback restores a workload template revision; it does not reverse database writes, external side effects, configuration outside the workload, or incompatible schema changes. Use the pre-agreed forward-recovery path when state cannot be rolled back safely.

Sources: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/), [Pod lifecycle and termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
