# Python typing contracts

Load when a public annotation, generic helper, protocol, overload, or narrowing decision changes.

- Treat annotations primarily as a static contract. They do not validate untrusted runtime values unless a framework or explicit validator evaluates them.
- Use the narrowest useful structural contract. `Protocol` is appropriate when callers need behavior without inheritance; avoid creating a protocol for one implementation detail with no independent consumer.
- Preserve variance semantics: mutable containers generally cannot safely widen element types because callers may write values. Read-only interfaces such as `Sequence[T]` permit broader use when the function only reads.
- Type variables should express a real relationship between inputs and outputs. If two values vary independently, using one shared type variable falsely promises they are the same type.
- Narrow at input boundaries with runtime checks or validation. `cast()` only informs the checker; `assert` can be disabled and is not input validation.
- Check overloads against runtime dispatch and ensure the implementation accepts every declared overload. Exercise representative callers with the repository's pinned checker.
- Avoid widening APIs to `Any` to silence a diagnostic. Find the untyped boundary or add a precise adapter when that improves the contract.

Use syntax supported by the declared minimum Python version. Generic syntax introduced in Python 3.12 is not a drop-in replacement when older runtimes are supported.

Sources: [Typing generics specification](https://typing.python.org/en/latest/spec/generics.html), [Python data model](https://docs.python.org/3/reference/datamodel.html), [Python typing](https://docs.python.org/3/library/typing.html).
