# Spring transaction behavior

Load when `@Transactional` appears ineffective, rollback differs from expectation, or data access crosses several service calls.

- Confirm transaction management is enabled and the object is a container-managed bean. Direct construction bypasses container advice.
- In default proxy mode, only calls entering through the proxy are intercepted. Self-invocation such as `this.write()` does not start a second advised transaction; move the boundary to a collaborating bean or use an explicitly chosen alternative mode.
- Identify proxy strategy, method visibility, finality, and the actual caller. JDK proxies expose interfaces; class-based proxies rely on subclassing. Check framework version because visibility behavior and proxy defaults may differ.
- Inspect propagation, isolation, timeout, read-only hints, and transaction manager selection against the actual data source. An annotation alone does not prove which resource participates.
- Verify rollback rules against exception types. By default, unchecked exceptions and errors trigger rollback; checked exceptions do not unless configured. Do not catch and suppress an exception inside the boundary if rollback is required.
- Avoid external network calls while holding a database transaction unless the consistency requirement justifies the lock and connection lifetime. A database transaction does not make an HTTP side effect atomic.
- Test through the proxied service entrypoint and inspect committed state from a separate transaction. A test-managed transaction can mask production commit/rollback behavior.

Sources: [Spring declarative transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html), [Spring proxying mechanisms](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html).
