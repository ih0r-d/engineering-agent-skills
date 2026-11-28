# System Design Checklist

Use this checklist selectively according to the system's requirements and risk profile.

## Requirements

| Area | Questions |
| --- | --- |
| Functional | What capabilities must the system provide? |
| Workload | What traffic, data volume, and growth are expected? |
| Performance | What latency and throughput targets apply? |
| Availability | What interruptions can consumers tolerate? |
| Recovery | What recovery time and data loss are acceptable? |
| Security | What trust boundaries and access restrictions apply? |
| Operations | What deployment, monitoring, and support capabilities exist? |
| Cost | What infrastructure and maintenance constraints apply? |

Distinguish confirmed requirements from estimates and assumptions.

## Architecture Alternatives

| Approach | Consider when |
| --- | --- |
| Modular monolith | Components can share deployment and operational boundaries. |
| Distributed services | Independent scaling, ownership, or deployment provides measurable value. |
| Synchronous communication | Consumers require an immediate response. |
| Asynchronous communication | Processing can be deferred or workloads need decoupling. |
| Relational storage | Transactions, constraints, and structured relationships are central. |
| Non-relational storage | Access patterns or data models justify a different storage approach. |
| Caching | Repeated reads or expensive computations justify consistency and invalidation costs. |

These approaches are not mutually exclusive. Select them according to requirements rather than architectural trends.

## Component Boundaries

- Define each component's responsibility.
- Identify dependencies and integration contracts.
- Identify authoritative data sources.
- Establish ownership of state and business invariants.
- Avoid circular dependencies where practical.
- Identify deployment and scaling boundaries.

## Reliability and Failure Handling

| Scenario | Evaluate |
| --- | --- |
| Dependency failure | Timeouts, fallback behavior, and failure propagation. |
| Transient failure | Bounded retries, backoff, and retry safety. |
| Duplicate requests | Idempotency and duplicate processing. |
| Partial failure | Consistency, compensation, and recovery. |
| Resource exhaustion | Capacity limits, backpressure, and load shedding. |
| Data loss | Backup, restoration, and recovery procedures. |
| Deployment failure | Compatibility, rollback, and recovery boundaries. |

Apply only mechanisms justified by the identified failure scenarios.

### Distributed consistency choices

- Keep a modular monolith when one deployment and transactional boundary meet ownership and scaling needs. A service boundary adds network failure, deployment coordination, observability, and data consistency work; independent deployment or ownership must justify that cost.
- Identify the owner of each invariant and authoritative record. A bounded context is useful when domain language, rules, and change ownership actually differ; drawing a service boundary around every entity is not a design method.
- When a database update and message publication must stay consistent, explicitly address the dual-write failure window. A transactional outbox can atomically record the state change and event for later delivery, but adds relay, duplicate delivery, ordering, retention, and operational work.
- Assume an at-least-once delivery path can redeliver unless the contract proves otherwise. Make consumer effects idempotent using a stable event/operation identity and durable deduplication where required; do not assume a retry is safe merely because the request timed out.
- Use bounded retries with backoff only for transient failures and idempotent operations. Coordinate timeout budgets across layers and avoid retry multiplication that overloads a failing dependency.
- Evolve schemas and APIs so old and new consumers can coexist for the rollout window. Verify expand-and-contract steps and compatibility against deployed consumers before removing old fields or data.

These patterns are options for specific consistency and failure requirements, not default prerequisites for distributed systems.

Further reading: [AWS transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

## Security

- Identify trust boundaries.
- Define authentication and authorization responsibilities.
- Classify sensitive data and its storage requirements.
- Identify secret management and access-control requirements.
- Evaluate relevant attack surfaces.
- Define audit requirements.

## Observability

Identify relevant signals:

- Request latency and throughput.
- Error rates and dependency failures.
- Resource utilization and saturation.
- Queue depth and processing delays.
- Business-level outcomes.
- Recovery and deployment events.

Select signals that support measurable requirements and operational decisions.

## Design Verification

- Trace representative use cases across component boundaries.
- Verify ownership and consistency assumptions.
- Evaluate relevant failure and recovery scenarios.
- Compare alternatives against explicit requirements.
- Identify assumptions requiring prototypes or benchmarks.
- Record unresolved questions and validation criteria.

Do not present an untested design assumption as an established result.
