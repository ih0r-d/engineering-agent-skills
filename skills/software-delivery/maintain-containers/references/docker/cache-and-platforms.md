# Container build cache and platform behavior

Load when builds are slow, cache changes affect correctness, or an image behaves differently across architectures.

- The build context is an input boundary. Check `.dockerignore` and Dockerfile-specific ignore files against all `COPY` and `ADD` paths; a file outside the context cannot be copied by a relative path. Keep secrets and irrelevant generated trees out of context.
- Order stable dependency descriptors before frequently changing source only when doing so preserves build semantics. Cache mounts can accelerate package downloads but are not part of the resulting image; builds must remain correct with an empty cache.
- BuildKit cache mounts and secret mounts have builder-specific behavior. Inspect the configured frontend and builder; do not assume every legacy builder supports the same options.
- Multi-platform manifests may select different base-image variants. Verify architecture-specific packages, native extensions, and executable formats on each promised target. A successful amd64 build does not establish arm64 runtime correctness.
- Pinning a base image digest fixes that base reference, not package repository state or arbitrary downloads. Pair reproducibility with an explicit update and vulnerability-response policy.
- Compare image size only for the same target platform and inputs. Check runtime dependencies, certificates, timezone data, user identity, and entrypoint before removing files from final stages.

Validate config without exposing interpolated secrets. Build or start services only when authorized, using an isolated project, ports, volumes, and cache scope.

Sources: [Docker build context](https://docs.docker.com/build/concepts/context/), [Docker build best practices](https://docs.docker.com/build/building/best-practices/), [Multi-platform builds](https://docs.docker.com/build/building/multi-platform/), [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/).
