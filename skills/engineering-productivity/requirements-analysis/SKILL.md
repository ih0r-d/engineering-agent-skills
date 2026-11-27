---
name: requirements-analysis
description: Analyze stakeholder needs, business rules, constraints, and acceptance criteria before implementation. Use for clarifying ambiguous requirements and defining verifiable scope.
---

# Requirements Analysis

## Workflow

1. Identify the requested outcome, stakeholders, authoritative requirements, and affected workflows. Read only relevant existing contracts.
2. Separate confirmed requirements, assumptions, constraints, and unresolved decisions. Identify contradictory requirements and missing failure behavior.
3. Define observable acceptance criteria, including boundaries and negative cases. Ask focused questions only where uncertainty changes the outcome; otherwise label assumptions.
4. Prioritize requirements and identify dependencies, exclusions, and decision owners. Load the reference for ambiguous or conflicting requirements.
5. Check that each acceptance criterion traces to a requirement and that no solution has been assumed without justification.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/requirements-checklist.md) | Task-specific decisions require additional guidance. |

## Constraints

- Do not invent stakeholder approval, targets, or business rules.
- Do not turn requirements analysis into architecture selection, implementation planning, or code changes.
- Avoid duplicating existing requirements or expanding scope without approval.
- Stop at unresolved decisions that prevent a reliable contract.

## Expected Output

Return confirmed requirements, acceptance criteria, assumptions, exclusions, and blocking questions. Distinguish proposals from approved requirements.
