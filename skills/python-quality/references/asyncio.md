# Asyncio task lifecycle

Load when work is scheduled concurrently, cancellation is involved, timeouts are unreliable, or latency rises despite async APIs.

## Ownership and failure

- Calling an `async def` function creates a coroutine object; it does not schedule it. Await it or create a task whose owner retains, awaits, and observes its result.
- Prefer `asyncio.TaskGroup` for related tasks that share a lexical lifetime and should be awaited together. It cancels sibling tasks after a child fails and reports grouped failures; use it only on supported Python versions.
- For independently managed background tasks, retain strong references, observe exceptions, and define shutdown/drain behavior. Do not fire-and-forget a task that owns a request, file, or client resource.
- Treat cancellation as control flow. `CancelledError` should normally propagate after `finally` cleanup. Suppressing it can break structured cancellation and timeout behavior.
- Put a timeout around the awaited operation that must be bounded. Cancellation requests do not guarantee that blocking native code or a remote operation stops; make cleanup and idempotency explicit.

## Event loop boundaries

- Synchronous CPU work and blocking I/O stall every task on that loop. Use an async API, a bounded thread executor for blocking I/O, or a process/interpreter strategy for CPU work after measuring.
- Bound queues and concurrent requests to prevent memory growth under backpressure. A semaphore limits active work but does not bound tasks already created.
- Test cancellation and failure with `asyncio.Event` or controlled fakes, not sleeps. Assert task completion and resource closure after cancellation.
- Async generators and context managers also need deterministic closure when consumers stop early.

Version-sensitive APIs and cancellation details vary. Check the application's supported Python version before recommending `TaskGroup`, timeout contexts, or newer task features.

Sources: [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html), [asyncio development guide](https://docs.python.org/3/library/asyncio-dev.html), [contextlib](https://docs.python.org/3/library/contextlib.html).
