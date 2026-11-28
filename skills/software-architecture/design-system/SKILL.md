---
name: design-system
description: Design software architecture, define API contracts, or evaluate and record an architecture decision. Use for proposed component boundaries, data ownership, system trade-offs, consumer compatibility, and ADRs.
---

# Design System

## Workflow

1. Identify the requested deliverable, stakeholders, requirements, current constraints, and decision authority. Record assumptions and missing workload or operational evidence.
2. Establish component and data ownership, external interfaces, and deployment boundaries. Follow explicit user technology requirements and inspect relevant design documents, manifests, dependencies, and configuration for the technology and version in scope. Use generic design criteria and project conventions where specialized evidence or guidance is missing.
3. Use only references relevant to the deliverable and evidenced technology. Compare viable alternatives against the same requirements, including the current approach where applicable.
4. Evaluate relevant quality attributes, failure propagation and recovery, compatibility and migration, ownership of invariants, and operational cost. Prefer the simplest option that meets the requirements.
5. Validate the design against representative interactions, failure scenarios, and measurable criteria. Distinguish proposed changes from decisions accepted by authorized stakeholders.

## Deliverables and references

| Deliverable | Guidance and observable output |
| --- | --- |
| System proposal | Use the [design checklist](references/design-checklist.md) for alternatives, consistency, failure scenarios, or quality attributes. Use the [system design template](assets/system-design-template.md) for a structured deliverable. Provide boundaries, responsibilities, interactions, data flows, trade-offs, and validation criteria. |
| API or event contract | Use [API contracts](references/api-contracts.md) for schemas, errors, compatibility, idempotency or other interface semantics. Define consumer-visible operations, authorization, examples and migration behavior. |
| Architecture decision | Use the [ADR guide](references/adr-guide.md) for comparison, decision status or supersession, and the [ADR template](assets/adr-template.md) if an ADR is requested. Record drivers, alternatives, rationale, consequences and revisit criteria. Preserve historical decisions and follow the project's ADR convention. |

Use [Java design trade-offs](references/java/design-tradeoffs.md) only when a design decision depends on Java subtype contracts, patterns, or Stream semantics.

## Boundaries

Return proposed designs, contracts, and ADRs in the response unless the user authorizes document edits. When recording or superseding an ADR, preserve the historical decision and record acceptance only with evidence of approval. Use architecture review to assess an existing system. Implementation, breaking changes, publication, and infrastructure changes require separate authorization.
