# Distribution artifact verification

Start from existing local artifacts or approved CI evidence tied to the candidate commit. Record package identity, version, digest and origin. Confirm reproducibility under the project's supported inputs when it is a stated requirement. Confirm that signatures or attestations identify the expected source, trusted builder, target and digest. A checksum can establish file identity against a trusted expected value and cannot establish origin by itself.

| Channel | Inspect and verify |
| --- | --- |
| Maven | Check artifact coordinates, resolved POM and dependency scopes, parent and module versions, classifiers, signatures, checksums and staging policy where required. Inspect JARs and compile a smoke consumer using the intended JDK and a disposable or cached dependency environment. Verify published APIs and source or JavaDoc artifacts when required. Inspect bound tasks before using `verify`. `install` writes to the local Maven repository and `deploy` targets a remote repository. |
| Python | Check distribution name normalization, version and wheel tags, contents and metadata such as `Requires-Python`, dependencies, entry points and license files where applicable. Compare the wheel and sdist coverage. Run configured local metadata checks, such as `python -m twine check dist/*` if installed, and install the selected local wheel in a disposable environment using cached dependencies. Exercise imports and console commands outside the checkout. A release can pass editable-install tests while missing package data in the wheel. |
| Containers | Verify repository, candidate tags and immutable digest, manifest platforms, image configuration and required runtime behavior. Confirm SBOM, vulnerability policy and provenance against the candidate digest when required. Promote tested content through the existing pipeline. Confirm that mutable tags point to the intended digest after an approved change. Daemon and registry inspection have different side effects and access requirements. |

Prefer artifacts built once and verified before promotion. Select local non-publishing commands that match this repository's tooling and avoid creating a second pipeline for a one-off release.

References. [Maven lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html), [Python packaging flow](https://packaging.python.org/en/latest/flow/), [Twine commands](https://twine.readthedocs.io/en/stable/), [Docker build attestations](https://docs.docker.com/build/metadata/attestations/)
