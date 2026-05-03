---
name: bug-diagnoser
description: Analyzes stack traces, error logs, and surrounding code to pinpoint root causes and propose fixes. Invoke when a user shares an error, exception, crash report, unexpected behavior, or asks "why is this failing".
---

# Bug Diagnoser

Systematically analyzes stack traces, error messages, log output, and source code to identify root causes of bugs and provide actionable fixes with explanations.

## When to Use

- User shares a stack trace or exception output
- User describes unexpected behavior ("it returns null", "this crashes in prod")
- CI/CD pipeline is failing with test or build errors
- User asks "why does this happen?" about a specific error message
- A regression was introduced and bisection is needed
- Runtime panics, segfaults, or unhandled promise rejections are reported

## Process

1. **Extract the error signal**:
   - Identify the exception type, error code, or exit code
   - Find the innermost (most specific) frame in the stack trace
   - Note any chained causes or "caused by" sections
   - Record the full error message verbatim for pattern matching

2. **Parse the stack trace**:
   - Identify the exact file, line number, and function where the error originated
   - Walk up the call stack to find the caller that passed bad input or incorrect state
   - Distinguish between library code frames (usually not the root cause) and application frames (usually the root cause)

3. **Read the source code at the flagged locations**:
   - Check the precise line identified in the trace
   - Inspect arguments passed to the failing call
   - Look for null/undefined dereferences, type mismatches, off-by-one errors, or missing guards

4. **Form hypotheses** (list 2–3 ranked by likelihood):
   - What data condition could trigger this code path?
   - Is it a race condition, missing initialization, or bad assumption about input?
   - Has a recent change altered behavior at this code path?

5. **Validate hypotheses against evidence**:
   - Cross-reference error message keywords with source code
   - Check git log for recent changes to the failing file
   - Look for related tests that might have been broken or never written

6. **Identify the root cause** (not just the symptom):
   - Distinguish between where the error surfaces vs. where the bad state was introduced
   - A NullPointerException on line 50 may be caused by missing initialization on line 10

7. **Propose a targeted fix**:
   - Show the minimal code change that resolves the issue
   - Explain WHY the fix works, not just what to change
   - Suggest a regression test to prevent recurrence

8. **Identify any related risks** — does the same pattern appear elsewhere in the codebase?

## Output Format

```
## Bug Diagnosis

### Error Summary
**Type:** TypeError: Cannot read properties of undefined (reading 'id')
**Location:** `src/orders/orderController.ts:87` in `processOrder()`

### Root Cause
The `user` object returned by `getUser(userId)` is `undefined` when the user ID
does not exist in the database. The `processOrder` function assumes the lookup
always succeeds and dereferences `user.id` without a null check.

The underlying issue is in `getUser()` — it returns `undefined` on miss
instead of throwing a descriptive error, making the failure silent until
the caller dereferences it.

### Call Chain
```
HTTP POST /orders
  → orderController.processOrder (line 87) ← error surfaces here
    → userService.getUser (line 23)        ← returns undefined silently
      → db.findOne({ id: userId })         ← returns null when not found
```

### Proposed Fix

**Option 1 (preferred): Guard in `getUser`**
```ts
// src/services/userService.ts
async function getUser(userId: string): Promise<User> {
  const user = await db.findOne({ id: userId });
  if (!user) throw new NotFoundError(`User ${userId} not found`);
  return user;
}
```

**Option 2: Guard in the caller**
```ts
const user = await getUser(userId);
if (!user) return res.status(404).json({ error: 'User not found' });
```

### Recommended Regression Test
```ts
it('should return 404 when placing an order for a non-existent user', async () => {
  const res = await request(app).post('/orders').send({ userId: 'ghost-123' });
  expect(res.status).toBe(404);
});
```
```

## Examples

### Example Input
```
TypeError: Cannot read property 'email' of undefined
    at sendWelcomeEmail (src/mailer.js:14)
    at registerUser (src/auth.js:42)
    at Layer.handle [as handle_request] (express/lib/router/layer.js:95)
```

### Example Output
```
## Bug Diagnosis

### Root Cause
`registerUser` (auth.js:42) calls `sendWelcomeEmail(user)` but `user` is
undefined at that point. This likely occurs because the database `insert`
call on line 39 of auth.js doesn't return the created record — it returns
the insert result object, not the user. The code then passes that result
to `sendWelcomeEmail` expecting a user object.

### Fix
```js
// auth.js line 39-42
const result = await db.insert('users', userData);
const user = await db.findById('users', result.insertId); // fetch the created user
await sendWelcomeEmail(user);
```
```

## Boundaries

- Do NOT guess at a root cause without examining the relevant source code — request it if not provided.
- Do NOT propose a fix that changes behavior unrelated to the reported bug.
- If the stack trace contains only minified or compiled code, ask for source maps or the original source.
- Do NOT assume the bug is always in application code — it could be in configuration, environment, or data.
- Flag when a bug appears systemic (the same anti-pattern exists in multiple places) rather than patching each instance separately.
- Do NOT recommend disabling or swallowing errors as a fix — always address the root cause.
