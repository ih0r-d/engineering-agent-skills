# FastAPI request and dependency lifecycle

Load when a FastAPI app, `Depends`, Pydantic request/response models, or ASGI endpoint behavior is in scope. Confirm FastAPI, Starlette, Pydantic, and server versions; dependency cleanup and test behavior can be version-sensitive.

- Trace the dependency graph from route parameters through sub-dependencies, security dependencies, overrides, and cleanup. A yielded dependency owns a lifecycle; verify whether its resource remains open through response serialization or streaming when that matters.
- Treat request models as input parsing and validation, not authorization. Enforce caller permissions and domain invariants separately. Review response models and serialization for accidental disclosure of internal fields.
- In `async def` routes, directly invoked synchronous blocking work runs on the event-loop thread unless explicitly offloaded. A synchronous route or dependency may be run through the framework's threadpool, but arbitrary helper calls do not automatically become non-blocking.
- Use lifespan startup/shutdown for process-wide clients and pools, and request dependencies for request-scoped resources. Close both on normal shutdown and failed startup; tests should exercise lifespan explicitly when the application depends on it.
- Use dependency overrides and controlled async clients for route tests. Verify overridden dependencies are reset so test state does not leak between cases.
- Treat background tasks as in-process work tied to application lifecycle, not as a durable queue. Use a separately managed job system when delivery, retries, or persistence are required.
- Check upload size limits, validation behavior, exception mappings, and OpenAPI compatibility at the actual boundary. Avoid logging raw bodies, tokens, or validation input that may contain sensitive values.

Sources: [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [Concurrency and async](https://fastapi.tiangolo.com/async/), [Lifespan events](https://fastapi.tiangolo.com/advanced/events/), [Testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
