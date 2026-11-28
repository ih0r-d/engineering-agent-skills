---
name: review-architecture
description: Assess existing software architecture against requirements, quality attributes, and operational constraints. Use for architecture audits, component boundaries, coupling, data ownership, scalability, reliability, and architectural risk assessment.
---

# Review Architecture

## Scope

Assess existing architectural structures, decisions, dependencies, and system-wide risks.

| Responsibility | Workflow |
| --- | --- |
| Assess existing architecture | Architecture review |
| Design a new system | System design |
| Review implementation changes | Code review |
| Improve code structure | Refactoring |

## Workflow

1. Establish the review objective, system boundaries, requirements, and architectural constraints.
2. Inspect relevant architecture documentation, source structure, dependency graphs, deployment configuration, and integration contracts. Follow explicit technology requirements first, then establish applicable platform and framework versions from the available evidence. Use the review checklist and project conventions where technology evidence or specialized guidance is missing.
3. Compare documented architecture with observable implementation and deployment behavior.
4. Identify component responsibilities, dependencies, data ownership, and trust boundaries.
5. Load relevant review guidance according to the affected quality attributes.
6. Evaluate architectural risks, failure propagation, compatibility, operational complexity, and maintainability.
7. Distinguish confirmed architectural defects from assumptions and improvement opportunities.
8. Prioritize findings by impact, likelihood, and evidence.
9. Recommend proportionate mitigations and practical verification steps.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Architecture review checklist](references/review-checklist.md) | Assessing architectural boundaries, quality attributes, failure scenarios, or technical debt. |

## Constraints

- Keep architecture assessment read-only. Changes to design documents, code, or infrastructure require separate authorization.
- Evaluate architecture against actual requirements rather than architectural preferences.
- Do not treat architectural patterns as universally applicable.
- Do not recommend migrations, additional services, or infrastructure without demonstrated benefits.
- Distinguish documented behavior from verified implementation and runtime behavior.
- Do not invent performance measurements, dependencies, or production incidents.
- Keep implementation changes and architectural redesign outside the review unless explicitly authorized.

## Expected Output

Summarize the reviewed architecture, scope, and available evidence.

For each actionable finding, report:

- Severity and architectural location.
- Affected requirement or quality attribute.
- Supporting evidence.
- Failure scenario or practical impact.
- Recommended mitigation and trade-offs.
- Verification criteria.

Separate confirmed findings, unverified risks, and improvement opportunities.

If no actionable findings are established, report the review limitations.
