---
name: code-reviewer
description: Performs automated code review with inline comments, flags anti-patterns, and suggests improvements against style guides. Invoke when asked to review code, check a pull request, audit code quality, or find issues in a file or diff.
---

# Code Reviewer

Automated code review skill that provides inline feedback, flags anti-patterns, identifies bugs, and suggests concrete improvements aligned with language-specific style guides and best practices.

## When to Use

- User asks to "review this code", "check my PR", or "audit this file"
- A pull request diff is provided and feedback is requested
- User wants to ensure code meets team style guides before merging
- User asks for a second opinion on implementation choices
- Code quality gates are failing and root cause is unclear
- User wants to identify potential bugs before shipping

## Process

1. **Identify the language and framework** from file extensions, imports, or explicit context. Note any relevant style guide (ESLint config, `.editorconfig`, `pyproject.toml`, `golangci.yml`, etc.).

2. **Parse the full scope of changes** — read the entire file or diff, not just the changed lines, to understand surrounding context, imports, and data flow.

3. **Run through the review checklist** for each function/block:
   - Correctness: Does the logic match the stated intent? Are edge cases handled?
   - Naming: Are variables, functions, and classes named clearly and consistently?
   - Complexity: Is cyclomatic complexity high? Can it be simplified?
   - Duplication: Is logic copy-pasted from elsewhere? Extract shared helpers.
   - Error handling: Are errors caught, logged, and handled gracefully?
   - Security: Any injection risks, untrusted input used unsafely, secrets in code?
   - Performance: Any N+1 queries, unnecessary loops, or expensive operations in hot paths?
   - Tests: Are new code paths covered? Are existing tests updated?
   - Documentation: Are public APIs, complex logic, and non-obvious decisions documented?

4. **Categorize each finding** by severity:
   - 🔴 **Blocker** — must be fixed before merge (bug, security issue, data loss risk)
   - 🟡 **Warning** — should be addressed (style violation, missing error handling, test gap)
   - 🟢 **Suggestion** — nice to have (readability, minor optimization, alternative approach)
   - 💬 **Nit** — trivial style/formatting issue

5. **Write inline comments** referencing specific line numbers or code snippets.

6. **Provide a summary section** with an overall verdict (Approve / Request Changes / Needs Discussion), a count of findings by severity, and 2–3 high-level themes observed across the review.

7. **Suggest concrete fixes** — don't just flag problems; show corrected code snippets where possible.

## Output Format

```
## Code Review Summary
**Verdict:** Request Changes | Approve | Needs Discussion
**Findings:** 🔴 2 blockers · 🟡 3 warnings · 🟢 5 suggestions · 💬 2 nits

### Key Themes
- Error handling is inconsistent across service layer methods
- Several functions exceed 50 lines and could be decomposed
- Missing input validation on user-facing endpoints

---

### Inline Findings

#### `src/users/userService.ts` — Line 42
🔴 **Blocker: SQL Injection Risk**
The `userId` parameter is interpolated directly into the query string.
```ts
// ❌ Current
const q = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Fix
const q = `SELECT * FROM users WHERE id = ?`;
db.query(q, [userId]);
```

#### `src/utils/formatDate.ts` — Line 17
🟡 **Warning: No null check before `.toISOString()`**
If `date` is `null` or `undefined`, this will throw at runtime.
...
```

## Examples

### Example Input
```
Review this Python function:

def get_user(user_id):
    result = db.execute("SELECT * FROM users WHERE id = " + user_id)
    return result[0]
```

### Example Output
```
## Code Review Summary
**Verdict:** Request Changes
**Findings:** 🔴 1 blocker · 🟡 1 warning

#### Line 2
🔴 **Blocker: SQL Injection**
String concatenation into a SQL query allows injection attacks.
✅ Fix: Use parameterized queries — `db.execute("SELECT * FROM users WHERE id = %s", (user_id,))`

#### Line 3
🟡 **Warning: IndexError if user not found**
`result[0]` raises IndexError if the query returns no rows.
✅ Fix: Return `result[0] if result else None` and handle the None case in the caller.
```

## Boundaries

- Do NOT rewrite entire files unless explicitly asked — provide targeted inline feedback only.
- Do NOT assume a style guide exists if none is provided; fall back to community defaults (PEP 8, Airbnb, Google style, etc.).
- Do NOT flag third-party library internals or auto-generated files.
- Do NOT run code or attempt execution — analysis is static only.
- Do NOT make subjective architectural decisions on behalf of the team (e.g., "you should use microservices").
- Limit review depth to files/diffs explicitly provided; do not speculatively fetch other files unless they are directly referenced and relevant.
- Keep nit count reasonable — avoid overwhelming feedback with trivial formatting issues if blockers are present.
