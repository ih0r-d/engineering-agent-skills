# JUnit Jupiter test behavior

Load when the project uses JUnit Jupiter annotations, extensions, parameterized tests, or lifecycle callbacks. Confirm the JUnit Platform/Jupiter version and build-engine configuration before relying on features or defaults.

- Read the configured test engine and discovery filters before interpreting a passing build. A source file can compile but not be discovered by the runner, or a tag/profile can exclude the changed test.
- Keep each test's setup close to its assertions. Check instance lifecycle before storing mutable state in test fields; changing to a class-scoped test instance can share state across methods.
- Use parameterized tests for a meaningful input matrix with readable case names. Avoid generating huge duplicate cases that obscure which contract failed.
- Use an extension when it owns a real reusable lifecycle or integration boundary. Prefer the project's existing extension registration style and verify callback ordering when cleanup or transaction behavior depends on it.
- Test exceptions through the public operation and assert the relevant type, cause, and observable state. Avoid asserting every message detail unless the message is a supported contract.
- For asynchronous or concurrent behavior, synchronize on the observable condition with bounded waits and clean up executors. Arbitrary sleeps create slow and flaky tests.

Source: [JUnit User Guide](https://docs.junit.org/current/user-guide/). Check the version-matched guide because the current documentation endpoint was unavailable during this audit.
