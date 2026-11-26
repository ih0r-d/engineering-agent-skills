---
name: skill-name
description: Describe what the skill does and when agents should use it.
---

# Skill Title

Briefly describe the skill's purpose and intended outcome.

## Scope

- Define the primary responsibility.
- Identify applicable tasks.
- Identify exclusions and responsibility boundaries.

## Operating Modes

| Mode | Purpose | Authorization |
| --- | --- | --- |
| Review | Inspect and report findings | Read-only |
| Fix | Apply scoped corrections | Explicit authorization |
| Verify | Execute applicable checks | No source changes |

## Workflow

1. Establish the task scope and relevant context.
2. Inspect the implementation, contracts, and available evidence.
3. Load relevant references when additional guidance is needed.
4. Perform authorized actions within the established scope.
5. Verify the result using applicable checks.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Topic guidance](references/topic.md) | Additional domain-specific guidance is required |

## Constraints

- Respect the consuming project's instructions.
- Preserve applicable compatibility contracts.
- Avoid unrelated changes and unnecessary dependencies.
- Distinguish verified evidence from assumptions.
- Do not perform unauthorized actions.

## Verification

- Establish the relevant baseline.
- Run applicable existing checks.
- Compare expected and observed behavior.
- Report failed, skipped, and unverified checks.

## Expected Output

- Findings or implemented changes.
- Supporting evidence.
- Verification commands and results.
- Remaining risks and limitations.