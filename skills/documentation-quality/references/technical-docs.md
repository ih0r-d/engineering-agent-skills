# Technical and maintainer documentation

- Describe architecture at meaningful boundaries: modules, contracts, data flow, ownership, lifecycle, concurrency, failures, and observability when relevant.
- Explain why non-obvious design decisions exist, alternatives and tradeoffs. Don't paraphrase every class or method.
- Keep design docs aligned with actual implementation and current CI/build constraints.
- Separate stable invariants from exploratory ideas; distinguish existing behavior from future plans.
- Prefer focused diagrams, ADRs and links to exact reference implementations when that reduces ambiguity.
- Keep contributor paths reproducible, with clear testing and module build instructions.
