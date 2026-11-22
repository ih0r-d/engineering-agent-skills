---
name: release-engineering
description: Review release readiness, prepare version and changelog plans, validate CI and artifacts, and execute approved release workflows without unsafe automation.
---

# Release Engineering

1. Establish the repository's versioning policy, supported release tooling, CI, distribution channels and requested mode: review, prepare, or execute.
2. Read [release-checklist.md](references/release-checklist.md) and relevant project-specific release instructions.
3. **Review:** read-only audit of changes since the previous release, compatibility, tests, build artifacts, provenance, docs and open blockers.
4. **Prepare:** draft changelog/release notes, propose versions, identify commands and validation steps. Do not assume a particular SemVer policy.
5. **Execute:** require explicit user authorization before creating tags, pushing commits, publishing packages/images, or deploying. Prefer existing deterministic CI workflows and dry runs.
6. Report evidence, complete command outcomes, unresolved blockers and next safe actions; never claim a release succeeded without confirmation.
