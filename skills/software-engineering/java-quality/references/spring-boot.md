# Spring Boot application behavior

Load when Spring Boot starters, `@SpringBootApplication`, `application.yml`, Actuator, or Boot test slices are present and relevant to the reported behavior. Confirm the Boot and Spring Framework versions before relying on defaults.

- Diagnose auto-configuration from the actual runtime classpath and conditions report. A dependency can cause configuration to activate; inspect the condition evaluation before excluding an auto-configuration or adding replacement beans.
- Trace configuration source and precedence for the property in question. `@ConfigurationProperties` gives structured binding and validation opportunities; check binding validation and active profiles rather than assuming a file value won over environment or command-line input.
- Keep environment-specific credentials outside packaged defaults. Do not expose Actuator endpoints or configuration values broadly; review endpoint exposure, authentication, roles, and sensitive health details.
- Health, liveness, and readiness answer different operational questions. Ensure readiness represents ability to accept traffic and does not become an expensive dependency fan-out; verify the actual endpoint is exposed and mapped as deployment probes expect.
- For bean lifecycle or test-slice issues, inspect application context creation, component-scan roots, profile activation, auto-configuration imports, and test overrides. A focused slice does not load the same context as a full application test.
- Use Boot's condition report, configuration binding diagnostics, and Actuator only in the approved environment. Avoid dumping effective configuration when it may include secrets.

Sources: [Spring Boot auto-configuration](https://docs.spring.io/spring-boot/reference/using/auto-configuration.html), [Externalized configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html), [Actuator endpoints and health](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html)
