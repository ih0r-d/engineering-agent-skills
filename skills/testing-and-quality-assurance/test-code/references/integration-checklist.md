# Integration Testing Checklist

## Boundary verification

| Boundary | Relevant evidence |
| --- | --- |
| Database | Schema constraints, transaction semantics, migrations, persistence, and cleanup. |
| HTTP or RPC | Serialization, status or error contracts, timeouts, and compatibility. |
| Messaging | Delivery semantics, duplicate handling, ordering, and recovery. |
| Consumer contract | Representative provider and consumer expectations across versions. |

## Environment and lifecycle

- Use isolated databases, namespaces, or temporary resources with synthetic inputs.
- Inspect existing test commands for image pulls, network calls, credentials, and destructive effects.
- Obtain authorization before provisioning external resources or starting workloads with material side effects.
- Use bounded readiness checks rather than arbitrary sleeps.
- Make cleanup safe even when assertions or setup fail; avoid deleting unrelated resources.
- Record participant versions and configuration needed to reproduce results.
- Distinguish a mocked contract check from an executed real integration test.
