# Java type and value contracts

Load when changing public value types, generic APIs, equality, sorting, or polymorphic hierarchies.

- Choose records for transparent data carriers whose components define the value contract. A record is only shallowly immutable: mutable components can still change, and generated equality follows component equality. Defensively copy mutable inputs when the contract requires ownership isolation.
- Use sealed hierarchies when the permitted subtype set is intentionally bounded. Check source compatibility for downstream implementors and keep the set compatible with the project's module/package constraints.
- `equals` and `hashCode` must use the same stable value components. Never mutate a field used for hashing while an object is a key in a hash-based collection. Test equal instances, unequal instances, and mutation boundaries.
- `Comparable` ordering should be consistent with equality when used with sorted sets/maps unless the difference is explicit. A comparator returning zero collapses keys in a `TreeSet`/`TreeMap`, even when `equals` says they differ.
- Java generics are invariant: `List<Dog>` is not a `List<Animal>`. Use `? extends T` for producer/read inputs and `? super T` for consumer/write inputs where that supports the actual API. Do not wildcard every type by default.
- Generic type arguments are erased at runtime. Do not expect `instanceof List<String>` or reflective inspection to recover an ordinary runtime type argument. Preserve necessary type tokens or explicit metadata at boundaries.
- Prefer domain types that make invalid states harder to express, but avoid wrappers that only rename a primitive without a distinct invariant or API benefit.

Check the configured `--release` before using records, sealed types, or newer syntax. Sources: [Java SE API](https://docs.oracle.com/en/java/javase/21/docs/api/), [JLS type system](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html), [Collections contracts](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collection.html).
