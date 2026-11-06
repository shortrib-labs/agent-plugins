# Code discipline

- Use test-driven development for all new behavior. Write the failing test first, watch it fail, then implement. If you find yourself implementing before testing, stop and write the test. Refactors of code that already has tests rely on those tests as the safety net.
- Treat test output as signal. When a test fails, read the application code before touching the test; changing a test needs a concrete, cited reason. Test output must be clean, with no stray errors or warnings.
- Mocks are fine for external dependencies in tests.
- Fix lint and compiler warnings in the code. Don't raise thresholds or disable rules project-wide. A per-line suppression needs a written justification.
- Comments explain why, not what. Preserve existing comments and update them when the code changes; remove one only when it is provably false.
