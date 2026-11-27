# Efficiency Checklist

| Area | Candidate optimization |
| --- | --- |
| Instructions | Remove duplicated rules; keep necessary defaults and gotchas. |
| Resources | Load only task-relevant references. |
| Tool calls | Reuse valid evidence for unchanged inputs and conditions. |
| Logs | Summarize relevant diagnostics while preserving safe full evidence when required. |
| Output | Return the requested deliverable without repeated prose. |

## Measurement

Use provider-reported usage or an appropriate tokenizer. Separate input, output, cached and other token categories when exposed. Compare equivalent task configurations and score correctness before efficiency. Record model, settings, sample size and measurement limitations. If token data is unavailable, label any estimate and avoid claiming measured savings.

## Gotchas

- Fewer output tokens may hide an incomplete deliverable.
- Cache discounts, reasoning tokens and provider pricing can change the relationship between usage and cost.
- Compression must preserve code semantics, identifiers and failure evidence.
- Optional optimizers need separate compatibility and behavioral evidence.
