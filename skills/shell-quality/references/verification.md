# Shell verification cases

Run syntax checking with the applicable interpreter, such as `bash -n path/to/script.sh` or `sh -n path/to/script.sh`. Run each file separately. Use installed `shellcheck -s bash path/to/script.sh` or `shellcheck -s sh path/to/script.sh` when the shebang does not establish the dialect. Inspect configured source paths and directives for coverage. Use `shfmt -d path/to/script.sh` for a configured check. Syntax, lint and style checks leave runtime behavior unverified.

Use a temporary working directory with representative input. Put executable stubs on a fixture `PATH` when the script calls external processes. Ensure stubs record individual arguments and return controlled statuses. Inspect absolute paths and inherited environment first, since PATH alone cannot intercept every command.

| Case | Expected observable result |
| --- | --- |
| Input path contains whitespace, `*` or a leading dash | The command receives the intended single operand. When deliberately matching files, unmatched patterns cause the documented result. |
| Producer fails while the consumer exits zero | The script preserves the failure when downstream work depends on a complete producer result. |
| Missing destination or failed directory change | Exit is nonzero and a sentinel outside the fixture survives. |
| Command fails after temporary directory creation | Owned temporary files are removed and the caller receives the failure status. |
| Quoted directory plus deliberate glob | Files in the intended directory match. A blanket additional quote around the entire expression would break the match. |

Test the exact supported interpreter and utility implementation for a portability claim. Keep full fixture output locally and report the smallest reproduced behavior.

References. [ShellCheck](https://github.com/koalaman/shellcheck), [shfmt](https://github.com/mvdan/sh), [Bash pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)
