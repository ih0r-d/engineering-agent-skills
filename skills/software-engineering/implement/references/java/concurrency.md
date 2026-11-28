# Java concurrency and ownership

Use this reference for data races, stale reads, unsafe publication, deadlocks, executor lifecycle, or cancellation bugs. Confirm the target JDK and use the Java Memory Model for language-level claims.

## State and visibility

- Identify shared mutable state and every read/write. `volatile` provides visibility and ordering for accesses to that variable; it does not make compound read-modify-write operations atomic.
- Establish a happens-before edge through monitor unlock/lock, volatile write/read, thread start/join, or a documented concurrent abstraction. Do not infer safety from likely CPU behavior or a test passing once.
- Prefer immutable values and ownership confinement. If sharing is required, choose one synchronization strategy and keep compound invariants inside its boundary.
- A thread-safe collection protects its documented operations, not a multi-call protocol such as `contains` followed by `add`. Use atomic methods or external synchronization.

## Locks and executors

- Keep lock scope small but include the whole invariant. Document lock order when paths acquire multiple locks; inspect callbacks and blocking calls while holding a lock.
- For `wait`, use a loop around the predicate because wakeups do not guarantee the condition. Prefer higher-level queues, latches, or conditions when they express the protocol directly.
- Bound executor queues and concurrency when input volume can grow. Define ownership, shutdown, rejection, task exception observation, and timeout behavior. Avoid creating an unbounded thread per request.
- On interruption, stop or propagate when possible. If an API cannot propagate `InterruptedException`, restore the interrupt flag and exit the operation promptly.
- For `CompletableFuture`, inspect which executor runs each continuation, where exceptions are observed, and whether cancellation reaches underlying work. Cancellation of a wrapper does not prove the external operation stopped.

## Diagnosis

Write a small stress or deterministic synchronization test around the invariant. A passing stress test is not a proof of race freedom. Use thread dumps for blocked states, JFR for contention and scheduling, and the configured JVM diagnostics before proposing synchronization changes. Measure throughput and tail latency under representative load.

Sources: [JLS Chapter 17](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html), [Java concurrency package](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html).
