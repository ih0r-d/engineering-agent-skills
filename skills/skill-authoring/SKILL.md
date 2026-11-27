---
name: skill-authoring
description: Create, review, or refactor portable Agent Skills. Use when defining skill scope, activation conditions, workflows, references, scripts, or specification compliance; combine with domain skills when their expertise is relevant.
---

# Skill Authoring

## Workflow

1. Classify the request as review, planning, or implementation. Inspect only relevant skills, instructions, and source evidence; expand scope when findings justify it.
2. Define one recurring capability, its positive triggers, near misses, and boundaries with adjacent skills. Preserve identifiers and existing contracts when revising.
3. Write a user-intent description and a concise common-path workflow with defaults, risk-specific constraints, practical gotchas, authorization, verification, and expected output.
4. Add focused references only for specialized detail; link them directly and state a task or symptom that should trigger loading. Keep critical common-path gotchas here.
5. Validate format, resources, links, and catalog/evaluation consistency. Add targeted regression cases and separate structural checks from behavior evaluation.

## Reference selection

- Read the [authoring checklist](references/authoring-checklist.md) when assessing scope, context budget, disclosure, resource design, or quality.
- For toolkit maintenance or the official/repository requirement distinction, consult `docs/skill-authoring.md` from the repository root.
- For behavioral and routing cases in this toolkit, consult `evals/README.md` from the repository root.

## Constraints and gotchas

- Apply official frontmatter and naming constraints; do not invent mandatory headings or client-specific fields.
- Advisory size targets are not gates. Preserve necessary expertise and never claim behavioral effectiveness from syntax checks alone.
- Prefer existing tools. Add scripts only for reusable deterministic tasks, document side effects and dependencies, and test them. Do not add empty resources or unnecessary dependencies.
- Preserve consumer policy, unrelated changes, and explicit authorization boundaries. Do not investigate or modify other skills without task scope requiring it.

## Verification and output

Run the narrowest relevant checks, then required repository gates. For routing changes, cover positive activation, near misses, and composition boundaries. Compare equivalent runs with and without the skill before claiming behavioral improvement. Report responsibility, trigger boundaries, changed files, checks and results, and unresolved behavioral evidence.
