# Static analysis and IDE inspection review

Load when analyzing compiler, IDE, Maven/Gradle, or local analyzer output.

- Prioritize correctness: ignored return values, incorrect nullability, impossible branches, dead code, incomplete cleanup, missing close, concurrency hazards, swallowed interrupts, and accidental API misuse.
- Treat duplicate-code reports as starting points: determine whether fragments represent shared business logic or intentionally separate concerns. Avoid premature abstraction solely to silence CPD.
- Check suspicious variable assignments (`Value value = null`, overwritten locals), unnecessary allocations, unused private declarations, unreachable branches, and needless mutable static fields. Confirm semantics with call sites.
- Verify reports with actual configuration and versions. Error Prone typically requires integration with the Java compiler; ArchUnit requires compiled classes and project-specific architecture rules; PMD/CPD may be run by Maven goals or standalone tooling.
- Prefer existing project tooling and local CLI commands; do not change pom.xml, build.gradle, CI, or quality profiles just to run a one-off audit without approval.
- Run quick, scoped checks before expensive full scans; keep raw logs locally, summarize actionable findings with evidence and the smallest fix.
- Respect intentional suppression when justified, but never add new suppressions blindly.
