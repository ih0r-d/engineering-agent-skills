---
name: token-optimization
description: Measure and reduce avoidable token consumption in AI engineering workflows while preserving task correctness. Use for verbose instructions, repetitive context, tool output, and response efficiency.
---

# Token Optimization

## Workflow

1. Identify the workload, model, tokenizer or reported usage, and correctness requirements. Establish a comparable baseline when measurements are available.
2. Locate redundant instructions, repeated reads, unnecessary reference loading, oversized tool output, and verbose responses.
3. Choose a narrow optimization that preserves governing instructions, evidence, authorization boundaries, and required deliverables. Load efficiency guidance when comparing usage or compacting output.
4. Compare representative tasks before and after under equivalent conditions. Use skill evaluation for systematic behavioral comparisons.
5. Report actual token usage, correctness, tool calls, latency, and costs only where measured. Revert or revise optimizations that degrade outcomes.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/efficiency-checklist.md) | Comparing usage or reducing repetitive context and output. |

## Constraints

- Do not remove critical constraints, diagnostics, exact identifiers, or required explanations to reduce token counts.
- Do not equate character counts with model tokens or token savings with cost savings.
- Do not install compression tools, proxies, or external services without authorization.
- Do not repeatedly rerun unchanged checks or hide failed checks in summaries.

## Expected Output

Report the baseline, targeted redundancy, proposed change, measured efficiency and correctness results, and unverified assumptions.
