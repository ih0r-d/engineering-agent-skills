---
name: release-engineering
description: Audit release readiness or prepare versions, changelogs, release notes, and artifact and CI validation. Use for compatibility, publishing checks, provenance, or rollback planning before a release.
---

# Release Engineering

1. Default to review or preparation. Identify the intended commit, last shipped release for the channel, version policy, distribution targets and existing CI release workflow. Check local evidence first and record missing or stale release information.
2. Read [readiness and authorization](references/release-checklist.md) for versioning, release notes, gates and rollback. Read [artifact verification](references/artifact-verification.md) for the relevant Maven, Python or container channel.
3. In review mode, inspect changes and gates without edits. In prepare mode, draft release notes, version changes or workflow fixes only as requested. In verification mode, inspect existing artifacts and run safe local checks after evaluating build hooks and CI profiles. Use existing release automation and scoped fixes.
4. Require explicit authorization for the specific tag, push, publishing destination, secret rotation or production release trigger. Permission to prepare or verify gives no authority for those actions. Before authorized execution, confirm the commit, version, channel, approved effects and existing pipeline. Verify the published identity before reporting success and inspect for partial publication before retrying.
5. Report readiness and blockers with severity, source location, affected artifact or consumer, mitigation and verification. Record the commit, baseline, artifacts, gate outcomes and unverified steps. Store complete non-sensitive logs locally.

Avoid publishing experiments and competing release pipelines. Honor distribution-specific immutability and preserve a viable recovery path.
