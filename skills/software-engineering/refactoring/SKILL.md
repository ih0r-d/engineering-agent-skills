---
name: refactoring
description: Improve the structure of existing code while preserving observable behavior. Use for scoped simplification, consolidation, or separation of responsibilities with a behavior baseline.
---

# Refactoring

## Workflow

### Establish Scope

1. Name the concrete maintenance problem and the smallest useful scope.
2. Identify public entrypoints, callers, and boundaries that constrain the change.
3. Record the behavior they depend on, including inputs, outputs, errors, side effects, and ordering where relevant.
4. Use available language-specific guidance for compatibility and idioms.

### Establish Baseline

1. Establish the baseline with the relevant existing tests and focused examples.
2. Run applicable tests before editing and distinguish pre-existing failures from regressions.
3. Add a narrowly scoped characterization test if the current checks miss behavior the change could alter.

**Stop before changing the code if source, contracts, or verification still leave behavior preservation uncertain. Report what evidence is missing.**

### Apply Changes

1. Make small, reversible edits.
2. Consolidate duplication when the code represents the same responsibility and should change for the same reason.
3. Preserve public APIs, compatibility, and observable behavior within the approved scope.

### Verify Behavior

1. Inspect affected callers and rerun the baseline checks.
2. Compare behavior at the same boundaries, including any newly characterized cases.
3. Treat a changed result, error, or side effect as a regression unless the user separately authorized that behavior change.
4. Resolve regressions within scope or report the point where you stopped.

## Constraints

- Leave files untouched when the request asks for a proposal or review only.
- Keep feature work, intentional bug fixes, architectural migrations, unsupported performance optimizations, dependency upgrades, and unrelated cleanup in their own scopes.

## Expected Output

Report:

- The concrete maintenance problem.
- Structural changes.
- Preserved contracts.
- Executed commands and results.
- Remaining behavior risks.

Call out separately authorized functional changes distinctly from structural work.