# Python-specific review rubric

- Correctness: mutable defaults, accidental shared state, iteration/mutation hazards, exception context, resource cleanup, asyncio cancellation, and timezone semantics where relevant.
- Types: explicit public contracts, Optional and narrowing correctness, type-checker compatibility, and alignment between annotations and runtime behavior.
- API: stable signatures, meaningful names, compatibility, deterministic imports, side effects and error contracts.
- Maintainability: cohesion, readable control flow, minimal duplication, useful data boundaries, no speculative abstractions.
- Testing: meaningful pytest cases with negative paths, monkeypatching limited to actual boundaries, no hidden external network dependencies.
- Tools: use project Ruff, Pyright/mypy, pytest and packaging checks; avoid imposing blanket rules or changing formatter configuration without permission.
