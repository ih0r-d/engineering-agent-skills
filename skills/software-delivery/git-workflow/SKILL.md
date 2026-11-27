---
name: git-workflow
description: Plan or perform scoped Git workflows, atomic commits, Conventional Commits, task identifiers, branches, pull requests, and conflict resolution. Use for repository history and change organization.
---

# Git Workflow

## Workflow

1. Inspect repository instructions, current branch, status, staged diff, and relevant history. Identify the requested Git operation and existing commit policy.
2. Separate unrelated changes and propose atomic commit boundaries. Inspect both staged and unstaged changes before staging anything.
3. Use the repository's commit format; when none exists, default to Conventional Commits. Load the commit conventions reference for types, scopes, and task identifiers.
4. For explicitly authorized operations, stage only intended paths or hunks, inspect the staged diff, run applicable checks, and commit. For conflicts, preserve both sides' intended behavior and verify the resolution.
5. Report actual commit hashes and remaining changes. Stop on failed hooks, ambiguous ownership, or unexpected history changes.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/commit-conventions.md) | Task-specific decisions require additional guidance. |
| [Branching and history](references/branching-and-history.md) | Selecting or reviewing branch, merge, rebase, revert, cherry-pick, or pull request workflows. |

## Constraints

- Never stage, commit, switch branches, merge, rebase, push, tag, or change remotes without authorization for the relevant operation.
- Do not use destructive reset, forced checkout, force push, or bypass hooks as a default remedy.
- Preserve unrelated user changes and never include credentials or generated caches accidentally.
- Do not invent task IDs, claim checks passed without execution, or silently rewrite shared history.
- Keep release version selection and publication in release engineering.

## Expected Output

Provide the proposed or executed operation, commit message, included scope, checks, and resulting Git state. Report unresolved conflicts or blockers.
