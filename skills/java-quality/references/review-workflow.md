# Review and cleanup workflow

## Prepare

1. Determine intent and scope: `read-only review`, `targeted fixes`, or `explicit broad cleanup`.
2. Read applicable `AGENTS.md`, module instructions, formatter, public API policy and relevant tests.
3. Inspect staged/unstaged/untracked changes; protect unrelated work. Identify generator-owned outputs.
4. Choose evidence thresholds: prioritize failures and compatibility risks over aesthetic preferences.

## Review

Inspect correctness/security; API and consumer compatibility; ownership/concurrency; generated artifacts; naming and cohesion; JavaDoc; duplication/dependencies; tests and contributor experience. Read implementations and usages before calling something an issue.

Finding format:

`P1 | src/main/java/.../Foo.java:42 | Evidence -> Impact -> Smallest safe fix -> Required verification`

Use P0 for confirmed serious correctness/security, P1 for meaningful maintainability/API risk, P2 for localized clarity with real impact. If nothing material is found, report that outcome.

## Fix only when authorized

1. Select a small related set of confirmed findings and establish behavioral invariants.
2. Implement focused fixes. Preserve published contracts; do not alter unrelated code or manually edit generated source.
3. Add/adjust regression tests for behavior; update documentation if public meaning changes.
4. Verify relevant module tests first, then applicable quality/API/consumer gates.
5. Recheck `git diff --check`, test results, changed-file scope and unrelated user work. Report known blockers honestly.

## Negative tests for this skill

- `arg2` in generated Java: trace source metadata/bytecode before renaming.
- A cohesive 90-line method: do not split based solely on length.
- A short method with unsynchronized static mutable state: flag the actual safety risk.
- A harmless conventional loop `i`: do not rename it merely to lengthen the identifier.
- A review-only request: report findings but do not change files.
- A dirty repository: never stage, overwrite, reformat or commit unrelated modifications.
