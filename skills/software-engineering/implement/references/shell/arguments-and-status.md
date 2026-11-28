# Shell argument and status changes

- Confirm the interpreter from the caller, shebang, and configured runner. Keep the required Bash version or POSIX sh contract.
- Preserve argument boundaries with quoted expansions. Forward arguments with `"$@"` and keep intentionally matched glob patterns outside quoted path prefixes. Exercise spaces, empty operands, and leading dashes.
- Check command status at the point where later work depends on success. Abort before relative filesystem changes when a directory change fails. Preserve the primary failure through cleanup.
- Restrict cleanup to the verified paths and processes the script owns. Inspect side effects before running it. Use temporary paths and command stubs to check arguments, exit status, and cleanup under the supported interpreter.
