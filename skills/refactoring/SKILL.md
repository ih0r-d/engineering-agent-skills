---
name: refactoring
description: Improve the structure of existing code while preserving observable behavior. Use for scoped simplification, consolidation, or separation of responsibilities with a behavior baseline.
---

# Refactoring

1. Name the concrete maintenance problem and the smallest useful scope. Identify public entrypoints, callers, and boundaries that constrain the change. Record the behavior they depend on, including inputs, outputs, errors, side effects, and ordering where relevant. Use available language-specific guidance for compatibility and idioms.
2. Establish the baseline with the relevant existing tests and focused examples. Run applicable tests before editing and distinguish pre-existing failures from regressions. Add a narrowly scoped characterization test if the current checks miss behavior the change could alter. If source, contracts, or verification still leave behavior preservation uncertain, stop before changing the code and report what evidence is missing.
3. Make small, reversible edits. Consolidate duplication when the code represents the same responsibility and should change for the same reason. Preserve public APIs, compatibility, and observable behavior within the approved scope. Keep feature work, intentional bug fixes, architectural migrations, unsupported performance optimizations, dependency upgrades, and unrelated cleanup in their own scopes.
4. Inspect affected callers and rerun the baseline checks. Compare behavior at the same boundaries, including any newly characterized cases. Treat a changed result, error, or side effect as a regression unless the user separately authorized that behavior change. Resolve regressions within scope or report the point where you stopped.

Report the maintenance problem, structural changes, preserved contracts, executed commands and results, and any remaining behavior risks. Call out separately authorized functional changes distinctly from structural work. Leave files untouched when the request asks for a proposal or review only.
