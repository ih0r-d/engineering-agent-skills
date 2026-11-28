---
name: write-spec
description: Draft, review, or update a software specification. Use for durable requirements documents, observable acceptance criteria, traceability, and specification changes with recorded decision status.
---

# Write a Specification

## Workflow

1. Identify the requested document, its audience, and whether to draft, review, or update it. Inspect the project format, existing specification, authoritative requirements, interfaces, and relevant tests.
2. Define the scope, actors, normative requirements, dependencies, exclusions, and constraints. Use the project's requirement identifiers and conventions. Follow explicit technology requirements and distinguish them from possible implementations.
3. Tie each requirement to observable acceptance criteria. Cover relevant normal, boundary, failure, compatibility, and migration behavior. Specify workload and measurement conditions for quality targets. Keep unresolved decisions, proposed rules, and approved requirements distinct.
4. Check that requirements and criteria agree with examples and known contracts. Flag contradictions, missing evidence, and unresolved decisions that block implementation or acceptance.
5. For authorized document updates, revise the requested sections and affected criteria together. Preserve unrelated requirements, identifiers, and decision history. Review the resulting diff and report which decisions are approved or still open.

## Boundaries

Return drafts and review findings in the response unless the user authorizes document edits. Preserve related source, tests, and configuration. A specification does not authorize implementation, architecture selection, or publication. Use requirements clarification when the primary deliverable is resolving stakeholder uncertainty.

## Expected Output

Provide the requested specification, scoped update, or evidence-backed review. Include traceable criteria, decision status, and remaining verification gaps.
