# Quarkus application behavior

Load when a Quarkus BOM, `quarkus.*` configuration, ArC CDI, Quarkus REST, or Quarkus native build is present and relevant. Confirm Quarkus platform and extension versions; supported behavior and defaults are extension-specific.

- Distinguish build-time-fixed configuration from runtime-overridable settings. Changing a build-time property requires rebuilding the application; verify the effective value at the phase where the extension consumes it.
- Trace CDI bean discovery, scopes, qualifiers, alternatives, and build profiles. Quarkus performs build-time augmentation and does not implement every portable CDI extension mechanism; test behavior with the actual Quarkus build rather than assuming a plain Spring/CDI container model.
- For REST endpoints, determine whether execution is on an event-loop or worker thread. Blocking database or filesystem work on an event loop can starve unrelated requests; use the framework's supported blocking annotations/dispatch and verify extension-specific rules.
- Check configuration profiles and test resources against the production build profile. A dev/test success can miss production-only build-time configuration or extension behavior.
- For native failures, use the Native Image reference and verify the produced executable. Do not assume a JVM-mode Quarkus test covers native reachability or initialization behavior.
- Prefer extension diagnostics and supported observability endpoints. Avoid adding extensions or switching reactive/blocking models solely to silence a thread warning without establishing the execution path.

Sources: [Quarkus configuration](https://quarkus.io/guides/config-reference), [Quarkus CDI reference](https://quarkus.io/guides/cdi-reference), [Quarkus REST](https://quarkus.io/guides/rest/)
