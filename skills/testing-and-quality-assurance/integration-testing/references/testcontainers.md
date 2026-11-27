# Testcontainers integration tests

Load when tests use Testcontainers to verify behavior against a real database, broker, or service container. Confirm Testcontainers, test framework, Docker-compatible runtime, and CI runtime availability before running.

- Use a real container when the tested contract depends on database dialect, protocol behavior, or service configuration that an in-memory substitute cannot establish. Keep unit logic tests independent of the container runtime.
- Pin an intentional image version or digest according to repository policy. Record the service and image version with test failures; a floating tag can change behavior without a source change.
- Wait for application readiness, not merely container process creation. Prefer service-specific health or log conditions with bounded timeouts; arbitrary sleeps make tests slow and flaky.
- Isolate database/schema and input data per test or test class. Static shared containers reduce startup cost but state must be reset deterministically. Do not share mutable containers across parallel tests unless the framework and setup explicitly support it.
- In Testcontainers' JUnit Jupiter integration, static `@Container` fields are shared for a test class and instance fields are restarted per test method. The integration documentation states parallel JUnit execution is unsupported; verify current version guidance before enabling it.
- Ensure cleanup covers failed setup and assertions. Inspect mapped ports, credentials, logs, and temporary volumes for sensitive data and lifecycle leaks. Do not configure reusable containers as a default shortcut around test isolation.
- Check whether CI permits a container daemon, image pulls, privileged execution, and network access. Report these prerequisites instead of silently replacing the real service with a mock.

Sources: [Testcontainers for Java: JUnit Jupiter](https://java.testcontainers.org/test_framework_integration/junit_5/), [Waiting for containers](https://java.testcontainers.org/features/startup_and_waits/), [General requirements](https://java.testcontainers.org/supported_docker_environment/)
