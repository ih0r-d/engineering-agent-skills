# JPA and Hibernate persistence behavior

Load when query counts, lazy state, entity updates, locks, or transaction boundaries are in question. Confirm Jakarta Persistence and ORM versions first; provider behavior and defaults vary.

## Persistence context and ownership

- Distinguish transient, managed, detached, and removed entities. Dirty checking applies to managed state; a detached object's mutation is not automatically persisted. `merge` copies detached state into a managed instance and returns that managed instance—do not assume the passed object becomes managed.
- Bound persistence-context lifetime to a deliberate unit of work. Long-lived contexts accumulate managed state and can return stale in-memory values; clear or close them according to framework ownership.
- Keep entity operations inside the transaction and persistence context that owns them. Accessing lazy associations after closure can fail or trigger work at a surprising boundary.
- Avoid treating database flush as commit. Flush sends pending SQL; transaction completion determines commit or rollback.

## Query count and fetch plans

- Reproduce N+1 with representative collection sizes and capture SQL/query counts. Eager mappings do not guarantee one joined query; providers may issue secondary selects.
- Choose fetch plans for a use case using projections, entity graphs, batch fetching, or targeted joins. Fetch joins over several to-many relationships can multiply rows and memory. Combining collection fetches with paging can distort page boundaries; inspect generated SQL and result semantics.
- Do not access associations in serializers, logging, or view mapping without making their load requirements explicit. This can create hidden queries or fail outside the transaction.
- Assert both returned data and query counts where performance is part of the contract. Avoid brittle exact counts when provider version changes legitimately alter SQL shape.

## Concurrency and transactions

- Use optimistic version fields when conflicting writes should be detected rather than silently overwritten. Retry only when the operation is safe to repeat and a bounded retry policy is justified.
- Pessimistic locks hold database resources and can deadlock or reduce throughput. Inspect transaction boundaries, lock order, indexes, timeout behavior, and concurrent callers.
- A service-level transaction does not make an external message or HTTP call atomic with the database. Use an outbox or other documented consistency pattern when that invariant is required.
- Test with the production database family when SQL dialect, locking, isolation, or constraint behavior is material. In-memory substitutes do not establish those contracts.

Sources: [Hibernate ORM user guide](https://docs.hibernate.org/orm/current/userguide/html_single/), [Hibernate ORM documentation index](https://hibernate.org/orm/documentation/), [Spring transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html).
