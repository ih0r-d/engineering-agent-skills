# Dependency Checklist

| Concern | Check |
| --- | --- |
| Resolution | Actual selected versions, dependency paths, constraints, and overrides. |
| Compatibility | Runtime, public API, binary compatibility, and platform requirements. |
| Reproducibility | Lockfile policy, registry identity, hashes, and frozen installation. |
| Upgrade scope | Smallest supported version change and affected transitive dependencies. |
| Security | Official advisory applicability, affected versions, and remediation evidence. |

## Gotchas

- A declared version is not necessarily the resolved version.
- A lockfile regeneration may change unrelated transitive packages; inspect the diff.
- A patch release is not proof of compatibility.
- Package installation can execute lifecycle code; inspect effects and use isolated environments where appropriate.
- Do not claim an advisory is resolved without checking the actual selected version and relevant evidence.

## Official guidance

- [Maven dependency mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
- [Gradle dependency management](https://docs.gradle.org/current/userguide/dependency_management.html)
- [Python packaging guide](https://packaging.python.org/)
- [npm package-lock documentation](https://docs.npmjs.com/cli/configuring-npm/package-lock-json)
