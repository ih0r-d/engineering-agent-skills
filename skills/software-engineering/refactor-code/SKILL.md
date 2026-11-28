---
name: refactor-code
description: Improve existing code structure while preserving observable behavior. Use for scoped simplification, consolidation, or separation of responsibilities with a behavior baseline.
---

# Refactor Code

## Workflow

1. Confirm the maintenance problem, edit scope, public entrypoints, and affected callers. Record behavior to preserve, including outputs, errors, side effects, ordering, and compatibility.
2. Follow explicit technology requirements first. Inspect relevant source, manifests, and configuration for the language, framework, and versions that constrain the change. Load a specialized reference only when it fits the evidenced stack and concern. Otherwise use the project conventions and this workflow.
3. Run applicable baseline checks and identify pre-existing failures. Add narrowly scoped characterization coverage if existing checks miss important behavior. Stop before edits when the baseline or caller contracts cannot establish behavior preservation.
4. Make small, reversible changes. Consolidate logic when it owns the same rule and changes for the same reason. Preserve public interfaces and generated or reflective consumers when relevant.
5. Inspect the diff and affected callers. Rerun baseline and characterization checks at the same boundaries. Resolve regressions within scope or report remaining gaps. Report actual checks, preserved contracts, and remaining risks.

## Reference selection

- Use [minimal Java changes](references/java/anti-overengineering.md) when assessing Java duplication, cohesion, extraction, or unnecessary abstractions.

## Boundaries

Keep proposals and reviews read-only. Treat changed behavior as a regression unless the user separately authorizes it. Keep feature work, intentional defect correction, dependency upgrades, and broad migrations outside structural edit scope.

When the client supports subagents and the task permits delegation, delegate only independently verifiable work with disjoint edit scope or a read-only brief. The primary agent owns shared contracts, the final diff and integrated checks. Use one sequential edit path for overlapping work or when delegation is unavailable or unauthorized.
