# Observability signals and service objectives

Load when setting or reviewing service health indicators, alerting, production diagnostics, or performance objectives. Use the organization's service ownership and incident policy; there is no universal SLO threshold.

- Define an SLI with its service boundary, eligible event population, good/bad event rule, and measurement window. Choose an outcome meaningful to consumers, such as successful requests or latency within a contract, rather than a metric that only reflects process activity.
- Let service owners and stakeholders set SLO targets and windows from user requirements and operational capacity. Do not invent a 99.x target or error-budget policy when none is documented.
- Measure latency distributions with sample count and window; averages can hide tail behavior. Compare equivalent routes, regions, versions, and workload cohorts. Include correctness and error rate alongside throughput.
- Use metrics for aggregate trends and alerting, traces for request path and dependency timing, and logs for event details. Correlate by stable trace/request identifiers while limiting sensitive values and high-cardinality labels.
- Keep metric dimensions bounded. User IDs, raw URLs, exception messages, and arbitrary request values can create unbounded cardinality or expose sensitive data. Prefer route templates and controlled dimensions.
- If an SLO exists, relate alert conditions to meaningful error-budget consumption and actionable response. A dashboard threshold alone is not an alert policy; alert only when someone can take a defined action.
- Record instrumentation gaps, sampling, missing data, clock skew, and population exclusions. Observed telemetry is evidence with limits, not complete visibility into every request.

Sources: [Google SRE Workbook: alerting on SLOs](https://sre.google/workbook/alerting-on-slos/), [OpenTelemetry metrics](https://opentelemetry.io/docs/concepts/signals/metrics/), [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/)
