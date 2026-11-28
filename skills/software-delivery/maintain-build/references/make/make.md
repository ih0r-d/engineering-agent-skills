# GNU Make dependency graphs

Load when a `Makefile`, generated target, parallel build, or shell recipe is involved. Confirm the Make implementation; GNU-specific behavior and flags are not automatically portable to BSD or other Make variants.

- Identify the default target and directory from which the project invokes Make. Model file outputs with prerequisites that affect them; mark action-only targets `.PHONY` so a same-named file does not suppress the action.
- Use prerequisites to express required ordering and parallel dependencies. A serial success does not prove correctness under `make -j`; inspect shared outputs and missing edges.
- Check automatic variables and shell expansion separately. Make uses `$@`, `$<`, and `$$` for shell variables; recipe lines commonly run in separate shells unless configured otherwise. A standalone `cd` line does not change the directory of the next recipe line.
- Trace failures through recipe prefixes (`-`), shell operators, recursive Make, and exit codes. Avoid masking a failing command with later successful commands.
- Inspect included Makefiles, `$(shell ...)`, recursive calls, and included-file remakes before using `-n`; expansion and recursive cases can still execute commands. Test a harmless target in an isolated fixture.
- Check quoting and command portability in the recipe's actual shell. Keep path arguments separate and preserve behavior on supported GNU/Linux and macOS environments.

Sources: [GNU Make manual](https://www.gnu.org/software/make/manual/make.html), [GNU Make recipe execution](https://www.gnu.org/software/make/manual/html_node/Execution.html)
