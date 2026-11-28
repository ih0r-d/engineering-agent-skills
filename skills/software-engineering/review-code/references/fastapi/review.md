# FastAPI review criteria

- Trace the changed route through its dependencies and cleanup. Identify who owns request-scoped resources and whether an exception or streaming response can outlive the intended resource scope. Confirm the FastAPI and Starlette versions before relying on cleanup timing.
- In an async route or dependency, inspect directly invoked synchronous database or file calls. Check where each runs and whether it blocks unrelated requests. Make the effect reachable from the changed entrypoint before reporting it.
- Where the route creates asyncio tasks, trace who awaits their results, observes failures, and closes resources on cancellation. Use controlled events for timing-sensitive verification.
- Check that changed request validation, authorization, and response serialization still enforce the route's public contract. Verify success and failure through existing route tests with representative dependencies.
