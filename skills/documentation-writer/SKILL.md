---
name: documentation-writer
description: Generates inline docstrings, README sections, and API reference docs from source code and function signatures. Invoke when asked to document code, write a README, add docstrings, create API docs, or explain what a function or module does.
---

# Documentation Writer

Generates accurate, well-structured documentation from source code — including inline docstrings, README sections, API reference pages, and changelog entries — tailored to the detected language and documentation standard.

## When to Use

- User asks to "document this function", "write a README", or "add docstrings"
- Public APIs lack documentation and onboarding is difficult
- A new module, package, or service has been created
- CI checks for documentation coverage are failing
- User wants to generate API reference docs for publishing
- Code was written without comments and needs to be understood by new contributors

## Process

1. **Determine the documentation target** from context:
   - **Inline docstrings**: individual functions, methods, or classes
   - **Module/package docs**: top-level overview of a file or package
   - **README**: project-level introduction, setup, usage, contributing
   - **API reference**: all exported symbols with params, returns, and examples
   - **Changelog**: summarize changes between versions

2. **Detect the language's documentation standard**:
   - Python → Google style, NumPy style, or reStructuredText (check existing docstrings)
   - JavaScript/TypeScript → JSDoc (`@param`, `@returns`, `@example`, `@throws`)
   - Go → GoDoc (plain sentences starting with the symbol name)
   - Java/Kotlin → Javadoc (`@param`, `@return`, `@throws`)
   - Rust → `///` doc comments with `# Examples` sections
   - Ruby → YARD

3. **Read the full source carefully**:
   - Understand what the function actually does, not just what it's named
   - Note all parameters, their types, and valid ranges
   - Identify return values and their types
   - Catalog exceptions, errors, or edge case behaviors
   - Note any side effects (mutations, I/O, external calls)

4. **Write the documentation**:
   - Start with a one-sentence summary (imperative mood: "Returns the user…", "Validates and stores…")
   - Add a longer description if the behavior is non-obvious
   - Document every parameter with type and description
   - Document the return value and all possible exception types
   - Include at least one usage example for public-facing APIs
   - Note deprecation warnings, version availability, or platform constraints if applicable

5. **For READMEs**, include sections:
   - Project title and one-line description
   - Badges (build status, coverage, npm/PyPI version if applicable)
   - Features list
   - Prerequisites and installation
   - Quick start / usage examples
   - Configuration reference
   - API reference (or link to generated docs)
   - Contributing guide
   - License

6. **Verify accuracy** — every documented param must exist in the signature; every documented exception must be reachable in the code.

## Output Format

### Inline Docstring (Python, Google style)
```python
def calculate_discount(price: float, discount_pct: float) -> float:
    """Apply a percentage discount to a price.

    Args:
        price: The original price in USD. Must be non-negative.
        discount_pct: Discount as a percentage (0–100).

    Returns:
        The discounted price, floored to two decimal places.

    Raises:
        ValueError: If ``price`` is negative or ``discount_pct`` is
            outside the range [0, 100].

    Example:
        >>> calculate_discount(100.0, 20.0)
        80.0
    """
```

### JSDoc (TypeScript)
```ts
/**
 * Fetches a paginated list of users matching the given filter.
 *
 * @param filter - Query parameters to filter users by.
 * @param filter.role - Optional role to restrict results to.
 * @param options - Pagination options.
 * @param options.page - 1-based page number. Defaults to `1`.
 * @param options.limit - Results per page (max 100). Defaults to `20`.
 * @returns A promise resolving to a paginated result with `data` and `total`.
 * @throws {UnauthorizedError} If the caller lacks the `users:read` permission.
 *
 * @example
 * const result = await listUsers({ role: 'admin' }, { page: 2, limit: 10 });
 * console.log(result.data); // User[]
 */
```

## Examples

### Example Input
```go
func Retry(fn func() error, maxAttempts int, delay time.Duration) error {
    for i := 0; i < maxAttempts; i++ {
        if err := fn(); err == nil {
            return nil
        } else if i < maxAttempts-1 {
            time.Sleep(delay)
        } else {
            return err
        }
    }
    return nil
}
```

### Example Output
```go
// Retry calls fn up to maxAttempts times, pausing delay between attempts.
// It returns nil as soon as fn succeeds, or the last error if all attempts fail.
// A delay of 0 retries immediately without pausing.
//
// Example:
//
//	err := Retry(fetchData, 3, 500*time.Millisecond)
//	if err != nil {
//	    log.Fatal("all retries exhausted:", err)
//	}
func Retry(fn func() error, maxAttempts int, delay time.Duration) error {
```

## Boundaries

- Do NOT fabricate behavior — only document what the code actually does.
- Do NOT add documentation to private/unexported symbols unless explicitly requested.
- Do NOT generate marketing copy — documentation should be precise and technical.
- Do NOT include implementation details that are subject to change in public-facing API docs.
- If a function has unclear or ambiguous behavior, flag it with a `// TODO: clarify behavior` comment rather than guessing.
- Keep README sections factual — do not promise features that don't exist in the provided code.
- Do NOT overwrite existing accurate documentation; only add or supplement where coverage is missing.
