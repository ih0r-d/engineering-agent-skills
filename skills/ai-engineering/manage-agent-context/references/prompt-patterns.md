# Prompt Patterns

| Failure | Candidate change |
| --- | --- |
| Ambiguous deliverable | Specify outcome and observable acceptance criteria. |
| Inconsistent structure | Define a minimal output contract and validate it externally when possible. |
| Conflicting instructions | Remove conflicts and clarify priority within the permitted instruction layer. |
| Untrusted input | Delimit data and specify how it may be used; enforce tool permissions outside the prompt. |
| Repeated edge-case failure | Add a representative example or explicit rule only when it addresses evidence. |

## Gotchas

- Delimiters alone do not guarantee prompt-injection resistance.
- Examples may bias unrelated outputs; test near misses.
- Structured output instructions are not a substitute for schema validation.
- Avoid claiming better performance without a comparable evaluation.
