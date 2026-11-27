---
name: engineering-handoff
description: Prepare or review engineering handoffs using verified repository state, completed work, decisions, checks, risks, and next actions. Use for transferring ownership or resuming interrupted technical work.
---

# Engineering Handoff

## Workflow

1. Identify the recipient, purpose, and handoff scope. Inspect current repository state and relevant change history when available.
2. Summarize completed work and decisions with evidence, including revision identifiers and affected contracts when known.
3. Record executed checks and actual results separately from skipped, failed, or unverified checks. Load the reference for incomplete or risky work.
4. Identify unfinished work, blockers, prerequisites, and a safe next action. Preserve unrelated changes and highlight partial operations.
5. Check that the recipient can locate evidence and resume without relying on unstated context.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/handoff-checklist.md) | Task-specific decisions require additional guidance. |

## Constraints

- Do not invent completion, test outcomes, approvals, or commit hashes.
- Do not disclose credentials, private logs, or sensitive data.
- Do not commit, push, deploy, or modify implementation merely to prepare a handoff.
- Avoid copying full logs or unrelated history; cite relevant evidence and summarize.

## Expected Output

Return current state, completed changes, decisions, verification, remaining risks, blockers, and next actions.
