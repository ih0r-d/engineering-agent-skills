# Release readiness and authorization

## Establish the release

- Identify the candidate commit and compare it with the most recent shipped baseline for the same channel and support branch. Confirm tag conventions and provenance from local metadata, recorded artifacts or CI evidence. A convenient local tag can describe a different branch, a prerelease or an unpublished build. State the baseline confidence when evidence is stale.
- Inspect actual user-visible and compatibility changes across public interfaces, CLI flags, configuration, protocols, data formats, platform support and dependencies. Apply the project's version policy. Under SemVer for a declared stable public API, breaking changes require a major bump, compatible new functionality a minor bump and compatible fixes a patch bump. Account for prereleases, pre-1.0 policy and channel-specific ordering.
- Make release notes scannable by upgrades, user-facing changes and fixes. Tie migration steps, changed defaults and support changes to actual behavior. Cross-check version sources, changelog range and published documentation links.

## Establish the gates and recovery

- Check CI jobs against the intended commit, matrix and release event. Distinguish skipped gates, stale runs and passing required jobs. Review trigger filters, artifact handoff and pinned inputs, protected environments, least-privilege credentials, signing, and attestations where the project uses them. Verify credential wiring without reading values.
- Identify which artifacts and services can be rolled back. Roll back running workloads to a known digest if the deployment supports it and data/schema changes allow it. An immutable published package might need a corrective release or a registry-supported yank. Describe actions for each partial-failure point and identify who can perform them.
- Treat tags, pushes, publishing, secret rotation and production workflow dispatch as separate external actions requiring explicit authorization for their actual effects. Check the command and any Git hooks or CI triggers. A Maven deploy phase or a registry-changing preflight still publishes even if called during prep. Use reviewed local alternatives.
- After authorized execution, check CI outcomes and the actual published identities, attestations and platform variants. On failure, inspect which steps already took effect before deciding if existing automation can resume.

Example finding. A passing pull request suite lacks the release job's packaging matrix, so native wheel variants remain unverified for the intended commit. Verify configured non-publishing artifact jobs or inspect their emitted metadata before marking the release ready.

References. [Semantic Versioning](https://semver.org/), [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations)
