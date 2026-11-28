# Hotfixes and backports

Load when correcting a released line, preparing an urgent patch, or applying a fix to multiple maintained versions.

- Confirm impact, affected supported versions, mitigation status, and the smallest verified correction. A temporary mitigation changes exposure or impact; it does not establish that the defect is permanently corrected.
- Identify the repository's supported branch model and release owner. Do not create a release branch or choose a target version from convention alone. Record why each maintained line needs the fix.
- Fix the current development line first when its code is the authoritative correction, then backport the minimal semantic change to each supported branch. Cherry-pick only when histories and the repository's policy make that safe; otherwise apply an equivalent targeted patch and preserve traceability to the original fix.
- Resolve conflicts by re-evaluating the intended behavior against the older line's APIs and invariants. Do not blindly take one side or copy unrelated refactoring from the newer branch.
- Run the regression test and compatibility checks on every target line. A test passing on the current branch does not establish that an older branch has equivalent behavior or dependencies.
- Build and identify each patch artifact independently. Keep versioning, changelog, support policy, and release gates consistent with that line; verify source commit and artifact digest before delivery.
- After an urgent release, ensure the correction is present on the forward development line and any other supported lines. Track omitted branches explicitly with a reason and owner.

Do not deploy or publish a hotfix solely because it is urgent. Preserve the applicable release and production authorization gates, and record any explicitly approved emergency exception.

Sources: [Git cherry-pick](https://git-scm.com/docs/git-cherry-pick), [Git revert](https://git-scm.com/docs/git-revert), [Semantic Versioning](https://semver.org/)
