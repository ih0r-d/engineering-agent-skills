# Helm release review

Load when `Chart.yaml`, Helm values, or Helm release commands are part of the deployment. Confirm the Helm major/minor version and chart API compatibility; command flags and defaults can change between releases.

- Inspect chart metadata, dependencies, values schema, environment overrides, hooks, and rendered manifests. Render the same chart version and values that the approved pipeline will use; do not assume repository defaults equal production values.
- Review the output of `helm template` or the project's existing render step before applying. Rendered output can contain Secret data; store it carefully and avoid pasting it into logs or reports.
- Record release name, namespace, chart version, application image digest, and effective values identity. Avoid an unpinned chart reference that can resolve to a different version during retry.
- Read upgrade/rollback options from the installed Helm version's help and official docs. Wait and automatic rollback flags can change behavior and do not reverse database or external side effects. A failed upgrade may leave hook effects or resources that require inspection.
- Inspect release history and current status before retrying or rolling back. Confirm which revision is active and whether a rollback target remains compatible with current data and configuration.
- Treat `helm upgrade`, `helm rollback`, and install commands against a real cluster as deployment actions requiring authorization. Prefer local rendering and static checks during review.

Sources: [Helm charts](https://helm.sh/docs/topics/charts/), [Helm template](https://helm.sh/docs/helm/helm_template/), [Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/), [Helm rollback](https://helm.sh/docs/helm/helm_rollback/)
