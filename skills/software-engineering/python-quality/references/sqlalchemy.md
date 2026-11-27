# SQLAlchemy session and transaction lifecycle

Load when SQLAlchemy sessions, ORM state, async database access, query counts, or transaction behavior are in scope. Confirm SQLAlchemy major version and dialect; 1.x, 2.x, sync, and async usage differ.

- Scope a `Session` or `AsyncSession` to one unit of work and do not share it concurrently across threads or asyncio tasks. It owns an identity map and transaction state, not just a stateless query facade.
- Make commit/rollback and close ownership explicit. A context manager can close resources; transaction framing should roll back on exceptions. Do not commit in a low-level helper if the caller owns a larger atomic unit.
- Understand autoflush and flush-before-query behavior when a query appears to persist or observe changes earlier than expected. Flush sends SQL within the transaction; it does not commit.
- After commit, ORM objects may be expired and require a live session to refresh. Avoid returning lazy ORM state to serialization code after session closure; map to a DTO or define the loading boundary explicitly.
- Reproduce N+1 queries with SQL logging or query instrumentation and representative collections. Choose loader strategies per use case; joined loading of collections can multiply rows and interact poorly with pagination.
- Distinguish database isolation, SQLAlchemy transaction scope, and application request scope. A session transaction does not make external messages or HTTP calls atomic with database writes.
- Test dialect-specific constraints, isolation, and locking against the production database family when those semantics matter. SQLite tests do not prove behavior of a different production database.

Sources: [SQLAlchemy Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), [Relationship loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html), [Asyncio extension](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
