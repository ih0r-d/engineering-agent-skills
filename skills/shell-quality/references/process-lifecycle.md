# Shell process and trap lifecycle

Load when a script starts background work, handles signals, manages temporary files, or must preserve a failing status through cleanup.

- Record each background PID immediately and `wait` for every owned job. Define whether one failure cancels peers, whether all results are collected, and which status is returned. A successful launch is not successful completion.
- A trap runs in the shell's current context, so cleanup state must be initialized before installing it. Quote and validate the exact owned temporary path; never derive broad cleanup paths from an unchecked variable.
- Preserve the original exit status explicitly when an EXIT trap performs cleanup. A cleanup command can otherwise replace the status that explains why the script failed.
- Handle INT, TERM, and HUP only when the script has defined safe interruption behavior. Terminate and reap owned children where appropriate; avoid trapping uncatchable signals or claiming cleanup on abrupt termination.
- Use `mktemp` with a form supported by the required macOS and GNU environments. Do not assume GNU-only flags such as `--tmpdir` on BSD systems; probe actual platform support from the project contract.
- Do not use `kill 0` as generic cleanup: it can signal the caller's process group. Track only child processes the script owns.
- Disable or narrowly scope `set -x` around credentials and secret-bearing arguments. Traces are output data and may be retained in CI logs.

Test with stubs that record PIDs, arguments, signal delivery, and exit codes. Include early failure, interruption, cleanup failure, and successful completion.

References: [Bash manual](https://www.gnu.org/software/bash/manual/), [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html).
