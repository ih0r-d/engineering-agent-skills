# Test Strategy Checklist

## Risk-to-test mapping

| Risk | Candidate verification |
| --- | --- |
| Pure business rule | Unit tests for boundaries and invariants. |
| Serialization or persistence | Integration tests against representative implementations. |
| Consumer contract | Contract tests and compatibility checks. |
| Critical user journey | Targeted end-to-end verification. |
| Capacity or recovery | Controlled workload or failure experiments. |

## Coverage and gates

- Record the requirement, scenario, expected outcome, test level, and evidence needed.
- Include negative inputs, permissions, concurrency, and recovery when relevant.
- Treat line coverage as an indicator, not proof of correctness; examine branches and missing assertions.
- Separate fast deterministic checks from slower environment-dependent checks.
- Define pass criteria, ownership, prerequisites, and handling of flaky tests; do not silently waive failures.
- Identify residual risks and explicitly deferred scenarios.
