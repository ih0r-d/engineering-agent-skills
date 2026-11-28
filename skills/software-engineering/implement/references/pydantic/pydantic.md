# Pydantic validation and serialization boundaries

Load when Pydantic models, settings, validators, or serialization define an API or configuration boundary. Confirm the Pydantic major version; v1 and v2 APIs and behavior differ.

- Distinguish parsing/coercion from strict validation. Test accepted input types and invalid edge cases against the model's configured strictness; annotations alone do not promise that runtime values already have the annotated type.
- Treat validators as executable boundary logic. Keep them deterministic and free of external I/O, and verify field/model ordering assumptions against the pinned Pydantic version.
- Separate input and output models when callers may submit fields that must not be returned. Explicitly inspect serialized output and aliases; serialization settings can alter wire compatibility.
- Check extra-field policy and defaults for configuration and API models. Silently ignoring an unexpected field can hide client typos, while forbidding it can be a deliberate compatibility policy; follow the contract rather than applying one globally.
- Do not assume a copy/update helper performs the same validation as parsing new input. Check the pinned version's documented contract and use an explicit validation entry point when values are untrusted.
- Keep secrets out of reprs, error details, generated schemas, and validation logs. Pydantic types do not replace authorization, database constraints, or domain-level invariants.

Sources: [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), [Validators](https://docs.pydantic.dev/latest/concepts/validators/), [Serialization](https://docs.pydantic.dev/latest/concepts/serialization/), [Strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)
