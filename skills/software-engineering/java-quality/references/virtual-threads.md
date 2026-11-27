# Virtual threads

Load for Java 21+ server workloads using many blocking I/O tasks, or when diagnosing pinning, resource exhaustion, and thread-local assumptions.

- Virtual threads improve scalability for high concurrency dominated by blocking waits; they do not make CPU-bound code execute faster. Bound the scarce resource (database connections, remote service capacity, memory), not virtual thread count alone.
- Use one virtual thread per task when the task model fits and the runtime supports it. Do not pool virtual threads merely to limit concurrency; use a semaphore or resource-specific pool for that limit.
- Keep request state and cleanup scoped to task lifetime. Thread locals work but can multiply memory at high concurrency; prefer explicit parameters or scoped context where supported.
- JDK 21 virtual threads can pin carrier threads in some synchronized/native blocking paths. Confirm the runtime version and use JFR or supported diagnostics before rewriting synchronization. Pinning behavior evolves across JDK releases.
- Preserve interruption and cancellation semantics. A cheap thread is still work that consumes CPU, sockets, memory, and downstream capacity.
- Verify library support, thread-affinity assumptions, and observability integrations before enabling virtual threads in a framework. Compare throughput, tail latency, and resource saturation under representative concurrency.

Java 21's `ScopedValue` is a preview API; do not recommend it as stable unless the application's JDK release and preview configuration explicitly allow it.

Sources: [Oracle Virtual Threads guide](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html), [JEP 444](https://openjdk.org/jeps/444), [ScopedValue Java 21 API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ScopedValue.html).
