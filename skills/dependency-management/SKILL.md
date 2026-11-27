---
name: dependency-management
description: Review or update software dependencies, manifests, lockfiles, and transitive resolution. Use for dependency compatibility, version conflicts, upgrade planning, and reproducible dependency changes.
---

# Dependency Management

## Workflow

1. Identify the ecosystem, package manager version, manifests, lockfiles, supported runtimes, and dependency policy.
2. Inspect the resolved dependency graph and distinguish direct from transitive dependencies. Establish the actual conflict, advisory, or upgrade requirement.
3. Check official release notes, compatibility constraints, and affected usage. Load the dependency reference for resolution and upgrade decisions.
4. Select the smallest supported change that addresses the requirement. Explain any lockfile or transitive changes before applying authorized edits.
5. Use the existing package manager and verification commands. Compare resolution and relevant behavior before and after the change.
6. Report unresolved compatibility risks and checks unavailable due to network, registry, or environment constraints.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/dependency-checklist.md) | Task-specific decisions require additional guidance. |

## Constraints

- Review without edits unless dependency changes are explicitly requested.
- Do not replace package managers, widen upgrade scope, delete lockfiles, or disable integrity checks as a default fix.
- Do not install from untrusted registries or execute unreviewed package lifecycle hooks.
- Do not infer compatibility or vulnerability remediation from version numbers alone.
- Leave dedicated security assessments to security review and build graph issues to build automation.

## Expected Output

Report dependency identity, resolved versions, reason for change, compatibility evidence, manifest and lockfile effects, verification, and remaining risks.
