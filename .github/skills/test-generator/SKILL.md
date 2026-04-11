---
name: test-generator
description: Reads source code and generates unit tests, integration tests, or snapshot tests with appropriate mocking. Invoke when asked to write tests, add test coverage, generate specs, or create test suites for functions, classes, or API endpoints.
---

# Test Generator

Generates comprehensive test suites from source code, including unit tests, integration tests, and snapshot tests. Produces idiomatic tests with proper mocking, setup/teardown, and meaningful assertions for the detected language and test framework.

## When to Use

- User asks to "write tests for this", "add test coverage", or "generate a test suite"
- Coverage reports show untested code paths
- New functions or classes are added without accompanying tests
- User asks for integration tests for API endpoints or database layers
- Snapshot tests are needed for UI components
- User wants to verify edge cases and error conditions are tested

## Process

1. **Detect the language, framework, and existing test toolchain**:
   - JavaScript/TypeScript → Jest, Vitest, Mocha, Jasmine
   - Python → pytest, unittest
   - Go → `testing` package, testify
   - Java → JUnit 5, Mockito
   - Ruby → RSpec, Minitest
   - Check for existing test files to match conventions (describe/it blocks, AAA pattern, etc.)

2. **Read and understand the source**:
   - Identify all public functions, methods, and exported symbols
   - Map input types, return types, and thrown exceptions
   - Trace data dependencies to determine what needs mocking
   - Identify side effects (DB writes, HTTP calls, file I/O)

3. **Design the test plan** before writing:
   - Happy path: normal, valid inputs produce correct output
   - Edge cases: empty inputs, boundary values, max/min, unicode
   - Error cases: invalid inputs, missing required fields, network failures
   - Side-effect verification: confirm DB calls, HTTP requests, or event emissions occurred

4. **Set up mocks and stubs** for all external dependencies:
   - Replace HTTP clients with interceptors (nock, responses, httptest)
   - Mock database calls using in-memory stores or query mocks
   - Stub file system, clocks, and random number generators for deterministic tests

5. **Write tests following AAA (Arrange → Act → Assert)**:
   - Arrange: set up inputs, mocks, and preconditions
   - Act: call the function or trigger the behavior
   - Assert: verify return values, side effects, and error messages

6. **Name tests descriptively** using "it should…" or "given…when…then…" patterns so failures are self-explanatory.

7. **Add setup/teardown** (`beforeEach`/`afterEach`, fixtures, factory functions) to avoid repetition and ensure test isolation.

8. **Verify generated tests compile** by checking syntax and import paths against the project structure.

## Output Format

Produce a complete test file (or files) with:
- Correct imports for the test framework and the module under test
- Grouped test suites (describe blocks or test classes)
- Individual test cases with clear names
- Mock/stub declarations scoped appropriately
- Inline comments explaining non-obvious test logic

```
// tests/userService.test.ts
import { getUserById, createUser } from '../src/userService';
import { db } from '../src/db';

jest.mock('../src/db');

describe('getUserById', () => {
  beforeEach(() => jest.clearAllMocks());

  it('should return the user when found', async () => {
    (db.query as jest.Mock).mockResolvedValueOnce([{ id: 1, name: 'Alice' }]);
    const user = await getUserById(1);
    expect(user).toEqual({ id: 1, name: 'Alice' });
  });

  it('should return null when user is not found', async () => {
    (db.query as jest.Mock).mockResolvedValueOnce([]);
    const user = await getUserById(999);
    expect(user).toBeNull();
  });

  it('should throw when the database errors', async () => {
    (db.query as jest.Mock).mockRejectedValueOnce(new Error('DB down'));
    await expect(getUserById(1)).rejects.toThrow('DB down');
  });
});
```

## Examples

### Example Input
```python
# src/calculator.py
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Example Output
```python
# tests/test_calculator.py
import pytest
from src.calculator import divide

class TestDivide:
    def test_divides_two_positive_numbers(self):
        assert divide(10.0, 2.0) == 5.0

    def test_divides_negative_numbers(self):
        assert divide(-6.0, 3.0) == -2.0

    def test_returns_float(self):
        result = divide(1, 2)
        assert isinstance(result, float)
        assert result == 0.5

    def test_raises_on_zero_divisor(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10.0, 0)

    def test_handles_very_large_numbers(self):
        assert divide(1e308, 1e154) == pytest.approx(1e154)
```

## Boundaries

- Do NOT alter the source file being tested.
- Do NOT generate tests for code that is clearly auto-generated (migrations, protobuf output, etc.).
- Do NOT hardcode credentials, real API keys, or production URLs in test files.
- Do NOT create tests that depend on execution order; each test must be independent.
- If the source function's behavior is ambiguous, generate tests that document the observed behavior and add a comment flagging the ambiguity.
- Limit integration test generation to what can reasonably run in CI without external infrastructure unless a test database or mock server is already configured.
- Do NOT generate tests that require a running production service; use mocks/stubs for all external calls.
