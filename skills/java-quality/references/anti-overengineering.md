# Minimal-change and anti-overengineering policy

- Preserve existing architecture, ownership boundaries, behavior, and external contracts.
- Prefer one necessary correction over a new service, factory, framework, interface, or abstraction.
- Do not split cohesive methods solely to meet arbitrary line counts.
- Do not replace clear loops with streams, patterns, builders, or records unless they demonstrably improve comprehension.
- Reuse existing domain concepts and tested interfaces before inventing new names or extension points.
- Avoid changes to unrelated files, generated output, public APIs, or build configuration without specific reason.
- Add the smallest focused regression test that proves the defect is fixed, including negative/edge cases.
- Keep review and fixes separate. Don't edit during read-only review.
