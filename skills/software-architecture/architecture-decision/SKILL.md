---
name: architecture-decision
description: Evaluate architectural alternatives and document architecture decision records (ADRs). Use for explicit technical decisions, decision drivers, trade-offs, consequences, and superseding existing decisions.
---

# Architecture Decision

## Scope

Support a specific architectural decision. Keep complete system designs, architecture audits, and implementation changes in their specialized workflows.

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Evaluate | Compare alternatives and recommend a decision without editing files. |
| Document | Draft or update an ADR within the requested scope. |
| Revisit | Reassess an existing decision against changed drivers or new evidence. |

## Workflow

1. Identify the decision question, stakeholders, current context, constraints, and existing decisions.
2. Establish decision drivers and distinguish mandatory requirements from preferences and assumptions.
3. Compare viable alternatives, including the current approach when relevant, against the same drivers.
4. Identify benefits, costs, risks, reversibility, and consequences. Load the ADR reference when drafting or revisiting a record.
5. Recommend an option with supporting evidence, or identify the evidence required to decide.
6. Record the decision status, rationale, consequences, validation criteria, and revisit triggers using the repository's existing ADR convention.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [ADR guidance](references/adr-guide.md) | Comparing alternatives, drafting a decision record, or superseding a previous decision. |

When asked to draft a reusable ADR, start from [the ADR template](assets/adr-template.md), adapting status and sections to local conventions.

## Constraints

- Do not invent benchmarks, stakeholder approval, or decision history.
- Treat a recommendation as proposed until authorized decision makers accept it.
- Preserve historical decisions and link superseding records according to local conventions.
- Do not implement decisions or modify unrelated files without authorization.

## Expected Output

Provide the decision question, context, drivers, alternatives, recommendation or recorded decision, status, rationale, consequences, verification criteria, and unresolved questions.
