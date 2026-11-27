# Maven lifecycle and reactor builds

Load when `pom.xml`, Maven Wrapper, Maven plugins, profiles, or reactor behavior are involved. Confirm the Maven, JDK, plugin, and extension versions used by CI.

- Trace the lifecycle phase actually invoked and plugin goals bound to it. `test` does not ordinarily reach later `verify`-bound integration checks; inspect skip flags, test providers, Failsafe executions, profiles, and plugin configuration before saying a suite ran.
- Distinguish aggregation from inheritance. A POM may list modules for a reactor without being their parent; a parent may supply inherited configuration without aggregating every child. Verify the actual `<modules>` and `<parent>` relationships.
- `dependencyManagement` and imported BOMs constrain versions when a dependency is declared; they do not add that dependency by themselves. `pluginManagement` supplies plugin defaults but does not necessarily schedule an execution. Trace the effective model and phase binding.
- Reactor options such as `-pl` and `-am` change selected projects. Compare a scoped build with the supported root invocation; a local cached SNAPSHOT may conceal a missing reactor edge or wrong module version.
- Profiles can activate by properties, JDK, OS, files, or environment. Record the profiles used by CI and local checks; do not add a profile to a release or publish goal without inspecting its effects.
- Inspect the Maven Wrapper distribution and configured checksum policy. `-o` prevents normal remote dependency resolution but does not make arbitrary plugin code or build extensions harmless.
- Use `help:effective-pom` or `dependency:tree` only with trusted project configuration and available plugins. Avoid logging settings or effective values that may contain credentials.

Sources: [Maven lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html), [Maven multi-module guide](https://maven.apache.org/guides/mini/guide-multiple-modules.html), [Maven dependency mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
