# Java module, framework and generated-code boundaries

## Dependencies and runtime identity

- Separate Maven/Gradle project dependencies, Java module exports, and runtime loaders. A public class may be concealed by an unexported JPMS package. `opens` permits deep reflection and has a different effect from `exports`. Confirm readability, exports, transitive exposure and service declarations under the actual module path before widening access.
- When a plugin fails to cast a value to a type with the same fully qualified name, compare the defining class loaders of the value and the expected class, and inspect artifact contents and dependency trees. Put genuinely shared interfaces in the intended parent loader and check shading or duplicate JARs before changing visibility. Test through the real plugin loader, since an ordinary classpath test can mask the failure.
- For service-loading failures check provider metadata, shading merges, module `uses` and `provides`, and the thread context class loader when the lookup uses it. Verify the final artifact in its packaging layout.

## Framework proxies and lifecycle

- Identify where framework advice runs and the proxy type actually selected. In Spring proxy mode, a call such as `this.store()` can bypass transactional advice even when the target method is annotated. Class-based proxies also have subclassing restrictions for final types and methods. AspectJ weaving follows different interception rules.
- Trace callers through container-managed beans, interceptor ordering and resource scope before moving or changing methods. Verify transaction rollback or security behavior through the configured public entrypoint. Inspect reflective constructors, persistence mapping and serialization defaults before rewriting classes as records or tightening visibility.
- Track whether instances are singleton, request-scoped, pooled or constructed directly. Test competing requests when mutable fields persist across invocations.

## Generated sources and names

- Trace generated output to its schema, annotation metadata, processor or template. Determine whether names such as `arg0` were emitted by generation or appear because reflection lacks compiled parameter metadata. Check `javap -v` on the relevant artifact, compiler `-parameters` and the downstream consumer before changing naming policy.
- Reproduce type-name collisions by compiling generated sources with the shipped imports and classpath. An emitted `Date` can collide with both `java.sql.Date` and `java.util.Date`, or a generated type can shadow `java.lang.String`. Correct the generator's symbol/import handling and qualify the conflicting type where appropriate. Test one collision and one ordinary case.
- Check stable ordering, repeated generation, imports, null/default semantics, generic mappings and source baselines. Update generator inputs or templates, regenerate using the existing entrypoint and compile downstream consumers. Compare snapshots where they encode a real compatibility contract.

Framework reference for proxy behavior. [Spring AOP proxying](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)
