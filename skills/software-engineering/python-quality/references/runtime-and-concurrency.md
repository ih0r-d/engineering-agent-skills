# Python runtime and concurrency behavior

Load when object aliasing, retained memory, thread safety, CPU parallelism, or event-loop interaction is part of the issue. Identify the Python implementation, exact version, and whether it is a free-threaded build before making runtime claims.

## Objects and memory

- Names refer to objects; assignment does not copy a mutable object. Trace aliases across defaults, class attributes, closures, caches, and returned collections. Test whether changing one reference unexpectedly changes another caller's value.
- Distinguish Python language guarantees from CPython implementation behavior. CPython commonly uses reference counting plus cyclic garbage collection, but object destruction timing and immediate resource release are not portable contracts. Use explicit context managers or `close()` for resources.
- When memory grows, compare retained object counts and allocation sites over equivalent workloads. `tracemalloc` tracks Python allocations, not all native allocations or memory owned by C extensions. RSS alone does not identify a Python object leak.

## Threads and processes

- Choose concurrency by workload and runtime: threads commonly overlap blocking I/O; processes provide separate interpreters and can use multiple CPU cores at the cost of startup, serialization, and process lifecycle. Benchmark representative work before increasing parallelism.
- The traditional CPython GIL limits simultaneous execution of Python bytecode in a process, but not all native extension work. Optional free-threaded CPython builds began in 3.13 and support status is version/build dependent; do not assume the default interpreter is free-threaded or that every extension is safe for it.
- Do not infer atomicity of multi-step operations from the GIL. Protect shared invariants with synchronization or ownership confinement. Process-pool arguments and results must satisfy serialization and importability constraints.
- Bound submitted work and define executor shutdown, cancellation, and exception observation. A future timeout stops waiting; it does not necessarily stop the underlying callable.

## Async boundaries

- An event loop runs Python callbacks cooperatively. A blocking call or CPU-heavy callback stalls other tasks on that loop; use an async API or a bounded executor for appropriate blocking work.
- Keep each task and future owned by the event loop that created it. Use documented thread-safe loop submission APIs to cross thread boundaries; do not manipulate loop-owned tasks from another thread.
- Check Python-version support before using newer asyncio task or timeout APIs. For task lifetime and cancellation behavior, also load the asyncio reference.

Sources: [Python data model](https://docs.python.org/3/reference/datamodel.html), [Python memory management FAQ](https://docs.python.org/3/faq/programming.html#how-does-python-manage-memory), [Free-threaded Python FAQ](https://docs.python.org/3/howto/free-threading-python.html), [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html), [asyncio and threading](https://docs.python.org/3/library/asyncio-threading.html)
