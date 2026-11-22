# Release checklist

- Compare the intended release commit against the last official tag, including user-visible changes and API compatibility.
- Determine the project's actual versioning and branch policy; do not infer major/minor/patch blindly.
- Confirm required tests, integration checks, formatter/linter/static analysis, dependency checks and platform baselines.
- Validate README, installation examples, changelog, upgrade steps and known incompatibilities.
- Inspect artifact coordinates, hashes, signing/provenance/SBOM when required by the actual distribution channel.
- Confirm CI release workflow and secrets exist without printing or accessing secret values unnecessarily.
- Separate preparation from irreversible actions: tags, pushes, packages, container registries and deployments.
- Use existing build/release automation; avoid introducing a second competing publishing pipeline.
