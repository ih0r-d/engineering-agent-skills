# Branching and history workflows

Load when selecting a branch model, integrating a change, resolving a conflict, or maintaining release lines. Follow the repository's documented policy and hosting protections.

## Choose the local model

- Prefer the strategy already used by the repository. Trunk-based workflows keep integration frequent and branches short-lived; they rely on fast validation and can use feature flags for incomplete work.
- GitFlow-style long-lived development, release, and hotfix branches can suit repositories that support parallel release trains, but increase merge and maintenance work. Use them only when release ownership and branch lifecycle are explicit.
- Feature branches and pull requests are a collaboration mechanism, not a complete release strategy. Check how default-branch protection, required checks, and release automation interact with the chosen pattern.

## Integrate changes safely

- Merge preserves branch topology and is appropriate when the repository records integration history. Rebase replays commits onto a new base and changes their IDs; use it for private/unpublished work when policy permits, never as a silent rewrite of shared history.
- Cherry-pick creates a new commit applying a selected change. Use it for a deliberate backport or isolated fix, then record the source commit and verify the target branch's behavior. It does not automatically keep the branches synchronized.
- Resolve conflicts using surrounding invariants and tests, not a blanket "ours" or "theirs" choice. Inspect the full resolved diff and rerun checks for the affected contracts.
- Prefer a revert commit to undo a change already shared through protected history. Reverting a merge requires selecting the mainline parent and can affect future merges; inspect history and repository guidance first.
- Before creating a release or hotfix branch, confirm supported lines, branch naming, ownership, and backport policy with the repository's release process.

## Pull request readiness

Check intended base branch, commit scope, task identifier rules, review state, required checks, generated files, and migration or release notes. A green local check does not satisfy hosted required checks. Do not bypass protection or rewrite shared history to make a branch appear ready.

Sources: [Git branching](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows), [Git merge](https://git-scm.com/docs/git-merge), [Git rebase](https://git-scm.com/docs/git-rebase)
