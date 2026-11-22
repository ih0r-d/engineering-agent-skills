# Java Quality — evidence-based rubric

Apply only criteria relevant to the reviewed scope. Project formatter, public API policy and build configuration remain authoritative.

## Naming and semantics

- Names should express intent and units where relevant. Methods that mutate, block, perform IO or initialize resources must not masquerade as cheap queries.
- Investigate vague identifiers (`arg0`, `arg2`, `tmp`, `obj`, `data1`, `result2`) in handwritten and generated code. Distinguish source-level names from bytecode reflection fallbacks, framework-required names and valid short local notation.
- For generated identifiers, trace source language metadata, AST conversion, generator templates and Java `-parameters`; repair the originating layer.
- Treat public/API parameter renames with care when reflection, serialization, source compatibility or external tooling depend on names.

## Methods, objects and complexity

- Flag mixed responsibilities, hard-to-follow branching, misleading boolean control flags, hidden side effects, unjustified overloads, needless duplication and long-lived mutable state **when there is concrete maintenance impact**.
- Prefer clear operations, guard clauses, and meaningful boundaries; avoid 1-line helper explosions and fixed line-count thresholds.
- Use `static` for behavior independent of instance identity or lifecycle, instance methods for owned state and polymorphism. Avoid mutable global registries and speculative patterns.
- Do not force records, streams, `var`, inheritance, DI or interfaces for fashion. Use modern Java when it improves actual comprehension within the configured Java baseline.

## API, exceptions and resources

- Check source, binary and behavioral compatibility, annotation metadata/defaults, Maven goal parameters, published generated APIs and configuration semantics.
- Narrow accidental exposure of internals while respecting existing consumers. Check that ownership, close behavior, thread-safety, nullability and failure modes are explicit.
- Preserve original exception causes, interrupt status and concurrency invariants. Do not hide failures or change recovery behavior as part of a style cleanup.

## JavaDoc and comments

- Document meaningful public/protected API contracts: assumptions, validation, exceptions, nullability, ownership, lifecycle and concurrency where applicable.
- Fix outdated and contradictory comments. Do not add prose that merely paraphrases an obvious method or line.
- Follow the repository's language rules for identifiers, comments and documentation.

## Generators and language tooling

- Treat generated Java as a user-facing artifact. Inspect names, imports, stable ordering, source layout, primitive/generic/container mappings and compile-time diagnostics.
- Fix generators rather than generated results. Compare golden snapshots and compile/run downstream consumers when output changes.
- Prefer established language parsers over duplicated regex grammars. Distinguish syntax acceptance from semantic/static compatibility and runtime behavior.

## Tests, tooling and contributors

- Tests need meaningful names, reliable fixtures, high-signal assertions and representative negative cases. Use real integration paths where mocks would conceal the contract.
- Existing Spotless/Checkstyle, SpotBugs, Revapi, SonarQube and CI results are evidence, not a substitute for design judgment. Do not weaken suppressions, quality gates or tests to pass.
- Aim for reproducible clean-checkout builds, actionable errors, accurate docs and focused PRs. Do not introduce dependencies or abstractions without users and a demonstrated advantage.
