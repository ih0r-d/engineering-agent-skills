# Python packaging and verification

## Establish the installed contract

Locate `pyproject.toml`, legacy metadata if used, lock or constraints files, CI matrices and the configured virtual environment. Check `requires-python`, build backend, extras, platform markers, console script targets and package discovery. A dependency used by runtime code must be available to the installed consumer. A test or editable environment can hide missing metadata, files or imports.

For distribution changes, inspect existing wheel and sdist contents and metadata and exercise imports and entrypoints from outside the checkout. Use a disposable environment and pre-existing artifacts or cached build requirements. Build isolation can fetch dependencies. Disabling it is appropriate only if the required build backend and dependencies are installed and that difference is recorded. Avoid changing the lockfile or resolving new dependencies during review.

## Choose the checks

| Evidence needed | Candidate check |
| --- | --- |
| Syntax on the minimum supported Python | Use that interpreter with the repository's compile check or `ast.parse` on selected files for a syntax-only probe. A newer interpreter can accept syntax the minimum cannot. Parsing does not execute imports. |
| Ruff lint and format | Use the configured version and roots. Examples are `ruff check path/to/file.py` and `ruff format --check path/to/file.py`. Preserve exclude behavior for explicitly named paths when the project requires `--force-exclude`. Keep autofix off in review. |
| Types | Use the configured `pyright` or `python -m mypy` invocation, virtual environment, configuration and package roots. Preserve broader type-check scope where imports or protocols cross the diff. A missing stub or misconfigured path is different evidence from a verified type contract failure. |
| Behavior | Use the repository's pytest launcher and selected node IDs or modules, such as `python -m pytest tests/test_api.py::test_missing_input`. Inspect conftest, plugin and test imports for side effects. Collection imports code. Use a test that checks the public result or failure, with fakes at external boundaries where needed. |

Note which conditions a check covered, including interpreter version, dependency groups and module roots. An analyzer can be unavailable without blocking targeted runtime or source-based verification.

References. [Ruff configuration](https://docs.astral.sh/ruff/configuration/), [Pyright configuration](https://microsoft.github.io/pyright/#/configuration), [mypy configuration](https://mypy.readthedocs.io/en/stable/config_file.html), [pytest import behavior](https://docs.pytest.org/en/stable/explanation/pythonpath.html), [Python packaging metadata](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
