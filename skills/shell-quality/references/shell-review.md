# Shell review reference

- Quote expansions and paths where required; use arrays in Bash for argument lists, not unsafe string concatenation.
- Review word splitting, globbing, pipelines, exit status propagation, subshell behavior, traps, signal handling, and cleanup.
- `set -euo pipefail` is context-dependent: understand conditional commands, unset variables and legitimate non-zero statuses before applying it.
- Check portable syntax for the declared interpreter. Do not introduce `mapfile`, associative arrays or GNU-only flags into macOS Bash 3.2 scripts without justification.
- Use `mktemp` safely, verify prerequisites, provide informative errors, and keep irreversible operations behind explicit opt-in.
- Use `shellcheck` for substantive defects, `shfmt` for formatting when project config permits, and execution tests in isolated directories for installers.
