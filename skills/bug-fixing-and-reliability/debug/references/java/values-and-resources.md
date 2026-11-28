# Java value and resource ownership

- Confirm the configured target release before using newer language features or library APIs.
- Carry the returned value of transformations on immutable values, such as `String.strip()`, to the next caller. Preserve intentional side effects, such as adding to a set even when the returned membership flag is unused.
- Assign responsibility for closing each stream or resource. Use try-with-resources for owned resources. Preserve caller-owned resources and test cleanup after partial acquisition or failure.
- Preserve public overload resolution, exceptions and observable lifecycle behavior. Verify the normal entrypoint and affected consumers on the supported release.
