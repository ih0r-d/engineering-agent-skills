# Architecture Decision Records

## Decision Drivers

| Driver | Evaluate |
| --- | --- |
| Requirements | Functional and quality attribute needs. |
| Compatibility | Consumer contracts and migration constraints. |
| Operations | Deployment, recovery, observability, and support. |
| Cost | Infrastructure, implementation, and maintenance effort. |
| Risk | Failure modes, security, uncertainty, and reversibility. |

Compare alternatives against the same drivers. Mark unknown evidence explicitly; avoid invented scores or measurements.

## ADR Structure

Use the repository's existing format. If none exists, the following sections are sufficient for most decisions:

- Title and status.
- Context and decision question.
- Decision drivers and constraints.
- Considered alternatives and trade-offs.
- Decision or recommendation and rationale.
- Positive and negative consequences.
- Validation criteria and revisit triggers.
- Related or superseded decisions when applicable.

## Decision Lifecycle

| Status | Meaning |
| --- | --- |
| Proposed | Recommendation awaiting approval. |
| Accepted | Decision approved by the responsible authority. |
| Superseded | Replaced by a later decision; retain the historical rationale. |
| Rejected | Considered but not adopted, where the local convention records it. |

Use local status conventions. Do not infer acceptance from an implementation or change the historical rationale to fit a later outcome.

## Verification

Identify measurable acceptance criteria, unresolved assumptions, migration or rollback considerations, and the evidence needed to revisit the decision. Distinguish planned checks from executed checks.
