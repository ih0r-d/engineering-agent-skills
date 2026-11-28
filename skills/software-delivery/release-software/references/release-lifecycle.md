# Release lifecycle and artifact promotion

Load when preparing a release candidate, choosing a version, or moving a verified artifact between environments.

## Candidate and version

- Establish the source commit, target channel, support line, intended consumers, and repository version policy before selecting a version. Do not infer the shipped baseline from the highest local tag alone.
- Apply Semantic Versioning only when the project declares a stable public API governed by SemVer. A breaking public API change increments major, compatible functionality increments minor, and compatible fixes increment patch. Pre-1.0 projects, private APIs, and distribution channels may define different policies; follow their documented contract.
- Use prerelease identifiers such as `rc` only when they are part of the established channel policy. A release candidate is a candidate artifact that still needs the release gates; its name alone does not establish readiness.
- Update the project's canonical version source and changelog using its established process. Summarize user-visible changes, compatibility impact, required migration, support changes, and known limitations. Do not claim fixes or security properties without evidence.

## Readiness and immutable promotion

- Verify the intended commit passed required quality gates for the actual release matrix, including supported runtimes and packaging targets. Distinguish skipped, stale, and missing jobs from passing evidence.
- Build a candidate once where the pipeline supports it. Record artifact coordinates or image digest, source revision, build identity, and required signatures or provenance. Promote the same verified artifact between environments instead of rebuilding it with environment-specific source or dependencies.
- Confirm every downstream consumer's compatibility window, including schema and protocol compatibility during mixed-version operation. A passing unit suite does not establish upgrade or rollback compatibility.
- For a failed or partial release, inspect which identities were tagged, uploaded, or made visible before retrying. Prefer a corrective release or documented registry recovery when an immutable artifact cannot be replaced.
- Keep release and deployment outcomes separate: an artifact may be valid and published while the environment rollout is not yet approved or complete.

## Recovery record

Record the candidate commit, version/channel, artifact identities, completed and skipped gates, publishing state, recovery owner, and remaining actions. Treat tags, pushes, signing, publishing, and production workflow dispatch as distinct authorized operations.

Sources: [Semantic Versioning 2.0.0](https://semver.org/), [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations)
