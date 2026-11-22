# Build system review

## Maven
- Verify effective plugin and dependency versions, build phases, module order, reactor behavior, profiles and reproducibility.
- Check consumer builds from clean checkout, plugin invocation, dependency resolution and quality gates without assuming cached SNAPSHOT artifacts.

## Gradle
- Prefer wrapper and configuration-cache-safe patterns where applicable; inspect task dependencies, dependency locking, toolchains and publication boundaries.

## Makefile
- Inspect target names, dependencies, phony targets, recipe shell, variables, quoting, parallelism and exit-code propagation. Avoid destructive default targets.

## Taskfile
- Check Taskfile schema/version, task dependencies, status checks, variables, includes, platform assumptions, command quoting and dry-run behavior. Do not assume every `cmd` uses Bash.

## Across tools
- Scripts invoked from build tasks should also follow `shell-quality` where relevant.
- Keep local developer workflows approachable and preserve existing CI contracts.
