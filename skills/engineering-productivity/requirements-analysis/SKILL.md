---
name: requirements-analysis
description: Clarify requirements and draft, review, or update a software specification. Use for stakeholder needs, business rules, scope, constraints, and verifiable acceptance criteria.
---

# Requirements Analysis

## Workflow

1. Identify the requested mode and deliverable. Gather the intended outcome, stakeholders, decision owners, authoritative requirements, and relevant existing specifications, interfaces, and tests. Follow the project's specification format when available.
2. Define in-scope and excluded behavior, actors, inputs and outputs, business rules, dependencies, and constraints. Separate confirmed requirements, proposals, assumptions, and open decisions. Distinguish mandated technologies from candidate solutions.
3. Resolve contradictions with the authorized decision owner where possible. Ask focused questions when uncertainty materially changes the outcome. Mark unresolved requirements and their impact on implementation or acceptance.
4. Draft or review a specification with prioritized requirements and observable acceptance criteria. Cover normal use, boundary conditions, failures, and compatibility or migration where relevant. Specify measurement conditions for quality targets and retain project identifiers and decision history when revising.
5. Verify that each criterion traces to a requirement, each requirement can be checked, and contracts and examples agree. Record the evidence, proposed changes, approval status, and decisions that still block implementation.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Requirements checklist](references/requirements-checklist.md) | Requirements conflict, failure cases are unclear, or a specification needs a completeness and traceability check. |

## Constraints

- Do not invent stakeholder approval, targets, or business rules.
- Keep elicitation, proposals, and reviews read-only. Edit the specification only when requested and limit changes to the agreed document scope. Architecture, planning, implementation, and external publication require their own authorization.
- Avoid duplicating existing requirements or expanding scope without approval.
- Stop at unresolved decisions that prevent a reliable contract.

## Expected Output

Return the requested analysis, specification, or review findings. Include confirmed requirements, acceptance criteria, assumptions, exclusions, blocking questions, and the status of proposed decisions.
