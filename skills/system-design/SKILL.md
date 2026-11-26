---
name: system-design
description: Design software systems, services, and components from functional and non-functional requirements. Use for system boundaries, component responsibilities, data flows, scalability, reliability, and integration design.
---

# System Design

## Scope

Design systems and components based on explicit requirements, constraints, and expected workloads.

Keep existing architecture assessments, detailed API contracts, and formal architecture decisions within their specialized workflows.

## Workflow

1. Identify the business objective, stakeholders, functional requirements, non-functional requirements, and technical constraints.
2. Establish system boundaries, external dependencies, expected workloads, and existing integration contracts.
3. Identify missing requirements and distinguish confirmed information from assumptions.
4. Compare viable architectural alternatives against the requirements and constraints.
5. Define component responsibilities, communication patterns, data ownership, and critical data flows.
6. Evaluate reliability, scalability, security, consistency, observability, and operational complexity.
7. Identify failure scenarios, recovery requirements, and deployment boundaries.
8. Validate the proposed design against representative use cases and measurable requirements.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [System design checklist](references/design-checklist.md) | Evaluating architectural alternatives, quality attributes, failure scenarios, or design completeness. |

## Design Principles

| Principle | Guidance |
| --- | --- |
| Simplicity | Prefer the least complex architecture that satisfies the requirements. |
| Cohesion | Group responsibilities that change for the same reason. |
| Coupling | Minimize unnecessary dependencies between components. |
| Data ownership | Define authoritative data sources and ownership boundaries. |
| Reliability | Design for relevant failure scenarios and recovery requirements. |
| Evolvability | Preserve reasonable extension and migration paths. |
| Observability | Identify signals required to understand system behavior. |

## Constraints

- Respect existing technology, infrastructure, and organizational constraints.
- Justify architectural complexity with concrete requirements.
- Do not introduce distributed systems, additional services, or infrastructure without a demonstrated need.
- Do not invent workload measurements or validated performance results.
- Keep proposals separate from approved implementation decisions.
- Do not modify implementation or infrastructure without explicit authorization.

## Expected Output

Present the proposed design with:

- Requirements, constraints, and assumptions.
- System boundaries and component responsibilities.
- Component interactions and data flows.
- Architectural alternatives and trade-offs.
- Quality attributes and failure scenarios.
- Validation criteria and unresolved questions.

Use diagrams and tables where they improve understanding.