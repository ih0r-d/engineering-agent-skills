# Python state ownership

- Trace mutable state created in defaults, class attributes, closures, and caches. Allocate per-call state inside the function when omitted arguments must be independent.
- Preserve the ownership contract of explicitly supplied objects. A check for an omitted value must preserve intentional empty values and their identity.
- Exercise repeated calls and explicit inputs through the public entrypoint. Verify exceptions, mutations and resource cleanup as part of the caller-visible contract.
