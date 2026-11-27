# Java design trade-offs

Load when a review proposes a new abstraction, inheritance hierarchy, pattern, or stream-based transformation. Start from the invariant and callers, not a pattern catalog.

- Treat SOLID as design prompts, not mechanical rules. Separate responsibilities when they change for independent reasons; add an extension seam when a real variation is expected; keep subtypes behaviorally substitutable; narrow interfaces to actual consumers; and depend on stable policy boundaries where this reduces change coupling.
- Prefer composition when behavior can be delegated without inheriting state or lifecycle constraints. Inheritance is useful when subtype behavior is genuinely substitutable and the base contract is stable; overriding implementation details can make future changes unsafe.
- Use a Strategy when callers need to select among independent algorithms, an Adapter when an incompatible boundary must be translated, a Decorator when behavior can be layered around a stable interface, and a Builder when construction has meaningful optional/invariant complexity. A single branch or constructor is not automatically a pattern problem.
- Keep domain types and interfaces when they protect an invariant, enable independent substitution, or express a public contract. Remove wrappers, factories, and generic frameworks that only rename one call or anticipate unsupported variation.
- Java Stream behavioral functions should be stateless and non-interfering. Do not place required mutations in intermediate operations or assume encounter order for parallel pipelines; use an explicit loop or terminal operation when state changes are the purpose.
- Evaluate the least complex alternative against the actual failure mode, testability, lifecycle, and compatibility requirements. A design-pattern name does not justify additional indirection by itself.

Sources: [Java Stream package specification](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html), [Java Language Specification](https://docs.oracle.com/javase/specs/jls/se21/html/index.html)
