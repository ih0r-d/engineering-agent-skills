# Java language and API review

## Contracts and compatibility

- Separate the JDK running the build from the configured target release and the supported runtime. Check `--release` or equivalent toolchain settings before suggesting records, sealed types, pattern matching or newer library APIs. A newer compiler can accidentally allow calls absent on the deployment JDK if the build constrains only bytecode level.
- For published changes, compare source overload resolution, erased JVM signatures, checked exceptions, annotation defaults and behavior. Inspect reflection, serialization and generated clients before renaming parameters or members. Where applicable, compile a consumer against the new API and run an already compiled consumer against the new artifact.
- Verify JavaDoc against actual validation, exceptions, nullability, units, mutation, ownership, blocking, thread safety and lifecycle when callers need them. For example, document whether closing a wrapper also closes a caller-provided stream. Resolve links and run configured doclint on the supported JDK for changed public docs.
- Make defensive copies only when justified by the contract. An unmodifiable view still reflects mutations of its backing collection, and an immutable outer list can contain mutable elements. Test both mutation through the returned object and mutation through the original input.

## Runtime behavior

| Signal | Establish the failure |
| --- | --- |
| Ignored return value | `name.strip();` discards a new value if the original string is used afterward. `seen.add(id);` can intentionally discard the boolean when membership is the sole goal. Read the return and side-effect contract and test the value the next caller sees. |
| Initialization immediately overwritten | Trace every branch and exceptional path. An unused allocation can be removed if its timing and effects are irrelevant. A constructor or initializer can validate input, acquire a resource or register a callback. Preserve required effects and definite assignment. |
| Resource crosses an API boundary | Identify who opens, closes and can still use the resource after a failed call. Use try-with-resources for owned `AutoCloseable` resources, including I/O-backed streams. Check partial acquisition and suppressed exceptions. Test whether exceptional paths close exactly the owned resources. |
| Exception translation | Preserve causes and intentional fallback. Investigate dropped interrupts and asynchronous failures hidden in unobserved futures. Propagate interruption when the interface supports it, or restore the flag when handling an interrupt without propagation. Exercise failure with the real public entrypoint. |
| Static mutable state or read-modify-write | Check publication, safe visibility, compound operations and lifetime across tests and class loaders. `ConcurrentHashMap` still permits duplicate work in a separate get-then-put sequence. Use atomic map operations only if their value-creation and retry semantics fit. Test ordering with latches or barriers rather than sleeps. |
| Asynchronous execution | Trace executor ownership, rejection, cancellation and timeout behavior. A timeout while waiting can leave work running, and thread-local state may be missing on another executor. Check who observes errors and shuts down owned executors. |

Trace existing invariants before proposing a new abstraction. Escalate a warning when it affects a reachable behavior, a supported compatibility promise or an explicit project gate.
