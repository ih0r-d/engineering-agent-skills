# Mockito test doubles

Load when a Java unit test uses Mockito stubs, spies, argument matchers, or interaction verification. Check the repository's Mockito version and JUnit integration.

- Mock a boundary whose behavior needs control, such as a remote client or clock. Prefer real simple values and domain objects; mocking the unit under test or every collaborator makes the test follow implementation structure instead of behavior.
- Stub only behavior the scenario needs. An unstubbed call may return a default value, so assert the result and inspect failures rather than assuming the mock will fail fast.
- Verify interactions only when they are part of the contract, such as one idempotent message publication. Avoid verifying incidental call order, private decomposition, or every getter.
- Use argument captors when the outgoing value itself matters. Keep assertions on captured values explicit and avoid broad matchers that can accept invalid input.
- Spies call real methods by default; stubbing a spy can invoke the method during setup. Check the version-matched Mockito API for safe stubbing syntax and prefer a small fake when partial mocking obscures behavior.
- Avoid `lenient` stubbing as a blanket fix for unused stubs. Remove unrelated setup or make the scenario's interaction explicit.

Sources: [Mockito project](https://github.com/mockito/mockito), [Mockito API documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html)
