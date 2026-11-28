# API Contract Design

## Protocol Selection

| Approach | Consider when |
| --- | --- |
| HTTP resource API | Consumers interact with resources using HTTP semantics. |
| RPC | Consumers invoke explicit typed operations. |
| GraphQL | Consumers need flexible selection of related data. |
| Events | Producers and consumers require asynchronous interaction. |

Prefer existing protocols unless requirements justify a change.

## Contract Checklist

- Define required and optional fields, types, formats, defaults, nullability, and validation.
- Define errors, authentication, resource-level authorization, and observable side effects.
- Use stable ordering and continuation semantics for pagination when required.
- Set appropriate request, response, and resource consumption limits.
- Avoid exposing secrets or internal implementation details in errors.

## HTTP Semantics

Respect method safety, idempotency, caching, and status semantics. GET retrieves a representation; POST submits data for processing; PUT replaces target state; PATCH applies partial modifications; DELETE removes the association with the target resource.

## Reliability and Compatibility

| Concern | Evaluate |
| --- | --- |
| Duplicate requests | Idempotency scope, concurrent retries, and side effects. |
| Concurrent updates | Conflict detection and lost updates. |
| Dependency failure | Timeouts, error propagation, and retry safety. |
| Long-running operations | Status tracking and observable completion. |
| Field removal, rename, or type change | Existing consumer dependencies and migration. |
| New required request field | Existing requests that omit the field. |
| Optional fields or new enum values | Strict parsing and exhaustive consumer handling. |
| Error changes | Consumer retry and recovery behavior. |

Do not assume additive changes are universally compatible or promise exactly-once execution without supporting guarantees.

## Verification

Validate representative schemas, invalid inputs, authorization, duplicate requests, concurrent updates, and existing consumer compatibility. Use existing contract tests where available and label unexecuted checks.

## Standards

- [HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest)
- [GraphQL Specification](https://spec.graphql.org/)
- [gRPC Documentation](https://grpc.io/docs/)
