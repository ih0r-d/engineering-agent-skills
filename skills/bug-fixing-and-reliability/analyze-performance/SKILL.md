---
name: analyze-performance
description: Analyze software performance using measurements, profiling, workload characteristics, and resource usage. Use for latency, throughput, CPU, memory, I/O, contention, and scalability bottlenecks.
---

# Analyze Performance

## Workflow

1. Establish the performance objective, affected workload, environment, and current evidence.
2. Define representative inputs, measurement boundaries, and relevant metrics before comparing results.
3. Inspect available telemetry and use existing safe profiling or benchmark tools when appropriate.
4. Identify candidate bottlenecks across CPU, memory, I/O, contention, dependencies, and workload characteristics.
5. Validate hypotheses with controlled comparisons; account for warmup, caching, concurrency, and measurement variability.
6. Recommend proportionate changes and define repeatable verification against the baseline.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed checklist](references/measurement-checklist.md) | Additional guidance is needed for performance baselines, profiling, bottleneck evidence, and benchmark design. |
| [Observability and SLOs](references/observability-and-slos.md) | Selecting service health indicators, reviewing alerting, or interpreting SLI/SLO and error-budget evidence. |

## Constraints

- Do not invent measurements or infer a bottleneck from a single ambiguous metric.
- Do not run uncontrolled load tests or attach intrusive profilers to production without authorization.
- Keep implementation changes outside analysis unless explicitly requested.
- Preserve correctness, resource limits, and compatibility when evaluating optimization.

## Expected Output

Report workload and environment, measurement method, baseline and observed results, supported bottlenecks, trade-offs, proposed verification, and measurement limitations.
