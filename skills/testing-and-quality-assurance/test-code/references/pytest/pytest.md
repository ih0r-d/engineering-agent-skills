# pytest fixtures and parametrization

Load when a Python project uses pytest fixtures, plugins, parametrization, monkeypatching, or fixture cleanup. Inspect `pyproject.toml`/pytest config, `conftest.py`, plugins, and supported pytest versions.

- Follow fixture scope and dependency edges. Function scope usually isolates mutable test state; broader scopes reuse objects and can leak mutations or resources between tests.
- Keep fixture setup and teardown symmetric. A `yield` fixture only reaches post-yield cleanup if setup advances to the yield; use context managers or finalizers carefully for partially acquired resources.
- Prefer parametrization for a small set of distinct contract cases with readable IDs. Keep setup data local to each case and avoid Cartesian-product explosion without a reason.
- Use `monkeypatch` or narrowly scoped mocks at the lookup site used by the code under test. Restore environment, imports, clocks, and working directories between cases.
- Treat `autouse` fixtures and plugin hooks as hidden global setup. Inspect collection and fixture output when a test behaves differently alone versus in the full suite.
- Use markers and `-k`/node selection according to repository configuration. A targeted run can omit required fixtures or integration markers; report the actual selection.
- Avoid `xfail` or broad skips as a permanent response to an unexplained failure. Preserve strictness and an issue/condition that will reveal when the limitation changes.

Sources: [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [Parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html), [Monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html), [Flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html)
