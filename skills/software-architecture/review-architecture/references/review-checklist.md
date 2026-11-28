# Architecture Review Checklist

Apply this checklist selectively according to the review scope, system requirements, and available evidence.

## Review Evidence

| Source | Purpose |
| --- | --- |
| Architecture documentation | Identify intended structure and decisions. |
| Source structure | Verify component responsibilities and boundaries. |
| Dependency graphs | Identify coupling and dependency direction. |
| Deployment configuration | Establish runtime and infrastructure boundaries. |
| API and event contracts | Verify integration and compatibility assumptions. |
| Tests and operational evidence | Establish observable behavior and known limitations. |

Do not assume that documented architecture matches deployed behavior.

## Quality Attributes

| Attribute | Review criteria |
| --- | --- |
| Maintainability | Cohesion, coupling, dependency direction, and change isolation. |
| Reliability | Failure isolation, recovery, and dependency resilience. |
| Performance | Evidence of latency, throughput, and resource constraints. |
| Scalability | Capacity limits and independently constrained workloads. |
| Security | Trust boundaries, authorization, sensitive data, and privileges. |
| Availability | Critical dependencies and recovery capabilities. |
| Testability | Observable contracts and independently verifiable behavior. |
| Operability | Deployment, monitoring, diagnostics, and recovery. |
| Evolvability | Compatibility, migration boundaries, and extension costs. |

Evaluate only attributes relevant to the system's requirements.

## Component Boundaries

- Identify unclear or overlapping responsibilities.
- Inspect dependency direction and circular dependencies.
- Identify shared mutable state and ownership conflicts.
- Evaluate whether integration contracts isolate implementation changes.
- Identify coupling between deployment and business responsibilities.
- Verify that boundaries reflect actual change and failure patterns.

## Data Ownership and Consistency

- Identify authoritative data sources.
- Verify ownership of business invariants.
- Inspect cross-component writes and shared storage dependencies.
- Evaluate transaction and consistency boundaries.
- Identify duplicate processing and partial-update risks.
- Assess schema evolution and migration compatibility.

## Reliability and Operational Risks

| Risk | Evaluate |
| --- | --- |
| Single point of failure | Criticality, redundancy, and recovery requirements. |
| Failure propagation | Isolation, timeouts, and dependency behavior. |
| Unbounded retries | Retry limits, resource exhaustion, and duplicate effects. |
| Partial updates | Consistency, compensation, and recovery. |
| Deployment coupling | Independent change requirements and compatibility. |
| Missing observability | Ability to identify and diagnose relevant failures. |
| Resource saturation | Capacity assumptions and protective limits. |

Establish the triggering conditions and affected system outcomes before reporting a finding.

## Technical Debt

Distinguish:

- Confirmed architectural defects.
- Deliberate trade-offs.
- Historical constraints.
- Unverified risks.
- Improvement opportunities.

Architectural complexity is not automatically a defect. Evaluate its maintenance and operational costs against the requirements it satisfies.

## Finding Classification

| Severity | Criteria |
| --- | --- |
| Critical | Credible risk of catastrophic system failure, irreversible data loss, or severe security compromise. |
| High | Material risk to a critical requirement or system operation. |
| Medium | Significant maintainability, reliability, or evolution cost within a limited scope. |
| Low | Localized architectural weakness with limited demonstrated impact. |

Adjust severity according to evidence, likelihood, affected consumers, and operational context.

Do not assign high severity solely because a preferred architectural pattern is absent.

## Mitigation and Verification

- Prefer the smallest change that addresses the established architectural risk.
- Compare mitigation costs, benefits, and compatibility effects.
- Identify dependencies and prerequisites.
- Define measurable acceptance criteria.
- Recommend targeted tests, prototypes, or operational measurements where evidence is missing.
- Preserve existing architecture when it adequately satisfies the requirements.