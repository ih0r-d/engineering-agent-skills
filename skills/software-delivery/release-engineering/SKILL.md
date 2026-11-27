---
name: release-engineering
description: Audit release readiness or prepare versions, changelogs, release notes, and artifact and CI validation. Use for compatibility, publishing checks, provenance, or rollback planning before a release.
---

# Release Engineering

## Operating Modes

Default to review or preparation.

| Mode | Responsibility |
| --- | --- |
| Review | Inspect changes and release gates without edits. |
| Preparation | Draft release notes, version changes or workflow fixes only as requested. |
| Verification | Inspect existing artifacts and run safe local checks after evaluating build hooks and CI profiles. |

## Workflow

1. Identify the intended commit, last shipped release for the channel, version policy, distribution targets and existing CI release workflow.
2. Check local evidence first and record missing or stale release information.
3. Load relevant references according to the release task and distribution channel.
4. Inspect changes, artifacts and release gates within the selected operating mode.
5. Use existing release automation and scoped fixes.
6. Before authorized release execution, confirm the commit, version, channel, approved effects and existing pipeline.
7. Verify the published identity before reporting success and inspect for partial publication before retrying.
8. Store complete non-sensitive logs locally.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Readiness and authorization](references/release-checklist.md) | Preparing versions, release notes, gates or rollback plans. |
| [Artifact verification](references/artifact-verification.md) | Verifying artifacts for the relevant Maven, Python or container channel. |
| [Release lifecycle](references/release-lifecycle.md) | Establishing a release candidate, applying a version policy, or promoting an immutable artifact. |
| [Hotfixes and backports](references/hotfix-and-backport.md) | Releasing an urgent correction or maintaining the fix across supported release lines. |

## Authorization

**Permission to prepare or verify does not authorize release execution.**

Require explicit authorization for the specific operation:

- Creating a release tag.
- Pushing changes or tags.
- Publishing to a distribution destination.
- Rotating secrets.
- Triggering a production release.

## Constraints

- Avoid publishing experiments and competing release pipelines.
- Honor distribution-specific immutability.
- Preserve a viable recovery path.

## Expected Output

Report release readiness and blockers, including:

- Severity and source location.
- Affected artifact or consumer.
- Mitigation and verification.

Record the commit, baseline, artifacts, gate outcomes and unverified steps.
