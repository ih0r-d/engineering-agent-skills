---
name: skill-authoring
description: Create or improve portable Agent Skills definitions, descriptions, workflows, and resources. Use for skill scope, activation boundaries, progressive disclosure, and specification compliance.
---

# Skill Authoring

## Workflow

1. Inspect the requested task, existing skills, consumer constraints, and official specification. Identify a recurring failure or missing expertise before introducing a skill.
2. Choose one coherent responsibility and define positive and near-miss requests. Preserve existing identifiers and contracts when revising a skill.
3. Write a task-specific description and concise operational instructions. Include concrete defaults, failure modes, authorization boundaries, and verification.
4. Move substantial specialist guidance into directly linked resources; explain when each is needed. Load the authoring reference when deciding resource or script boundaries.
5. Run the existing specification and repository checks. Record behavioral tests needed to demonstrate improvement; use the skill evaluation workflow for live comparisons.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/authoring-checklist.md) | Deciding scope, resource structure, or script boundaries. |

## Constraints

- Do not impose proprietary mandatory fields or headings, copy unlicensed content, or introduce agent-specific dependencies into portable instructions.
- Do not create empty resources, repeat generic model knowledge, or add scripts without a concrete repeatable task.
- Do not edit existing skills outside the authorized scope or claim that syntax validation proves activation quality.

## Expected Output

Report the responsibility, activation boundaries, files changed, validation results, and remaining behavioral evidence.
