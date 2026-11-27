# Performance Analysis Checklist

Apply selectively to the task and available evidence.

## Measurement selection

| Concern | Useful evidence |
| --- | --- |
| Latency | Distribution and relevant percentiles with sample count and window. |
| Throughput | Completed work per unit time at stated concurrency and error rate. |
| CPU | Utilization, sampled stacks and runnable work. |
| Memory | Allocation rate, retained objects, GC and process memory where relevant. |
| I/O | Wait time, queue depth, operation rates and dependency latency. |
| Contention | Lock waits, blocked threads and queue saturation. |

## Benchmark discipline

- Record runtime, hardware or resource limits, configuration, dataset and workload.
- Compare equivalent conditions; separate warmup from steady-state where appropriate.
- Repeat measurements and report variability instead of claiming significance from one run.
- Check error rates and correctness alongside performance.
- Treat profiler overhead and synthetic workload differences as limitations.
