---
name: error-handler-advisor
description: Reviews code paths and suggests robust error handling — retries, fallbacks, circuit breakers, and user-friendly messages. Invoke when asked to improve error handling, add retries, implement fallbacks, review exception handling, or make error messages more user-friendly.
---

# Error Handler Advisor

Reviews application code paths for missing, incomplete, or fragile error handling and recommends robust patterns — retries with exponential backoff, fallbacks, circuit breakers, graceful degradation, and user-friendly error messages.

## When to Use

- User asks to "improve error handling" or "add retries"
- Code has bare `catch(e) {}` blocks or re-throws without context
- An API or service call has no fallback if it fails
- User asks about circuit breakers, bulkheads, or graceful degradation
- Production incidents are caused by unhandled errors or cascading failures
- User wants to make error messages more informative without leaking internals

## Process

1. **Audit existing error handling** for these anti-patterns:
   - **Silent swallowing**: `catch (e) {}` or `catch (e) { return null; }` with no logging
   - **Over-broad catch**: catching `Exception` or `Error` when only specific errors should be caught
   - **Re-throwing without context**: `throw e` loses the stack trace; use `throw new Error('context', { cause: e })`
   - **Missing finally**: resources (DB connections, file handles) not released on error
   - **Leaking internals**: stack traces or internal paths returned to API clients
   - **No timeout**: external service calls with no timeout — can hang indefinitely
   - **No retry**: transient network errors not retried
   - **No fallback**: critical path fails completely when a non-critical dependency is unavailable

2. **Classify each error type** that can occur:
   - **Transient** (retriable): network timeouts, rate limit (429), service unavailable (503)
   - **Permanent** (not retriable): bad request (400), not found (404), auth failure (401/403)
   - **Unknown**: unhandled/unexpected errors — log, alert, return generic 500

3. **Recommend retry patterns** for transient errors:
   - Exponential backoff: start at 100ms, double each attempt, cap at 30s
   - Jitter: add random offset to prevent thundering herd
   - Max retries: 3–5 for most cases; specify retry budget
   - Only retry idempotent operations (GET, DELETE) or operations with idempotency keys

4. **Recommend circuit breaker** for repeated downstream failures:
   - Closed → Open after N consecutive failures (or failure rate > threshold)
   - Open → reject calls immediately for a cooldown period (30s–60s)
   - Half-Open → allow a probe request; if successful, close the circuit

5. **Recommend fallbacks** for graceful degradation:
   - Return cached data when the live source fails
   - Return a default/empty state rather than an error when appropriate
   - Disable a non-critical feature rather than failing the entire request

6. **Standardize error responses**:
   - API errors should return a consistent JSON structure
   - Include: `status`, `code` (machine-readable), `message` (human-readable), `requestId` (for support)
   - Never include stack traces in production API responses

7. **Ensure errors are observable**:
   - Log at the appropriate level (WARN for handled/expected, ERROR for unexpected)
   - Include context: user ID, request ID, operation name, input parameters (sanitized)
   - Emit metrics/alerts for error rate thresholds

## Output Format

For each issue found, provide:

```
### Issue: Silent Error Swallowing
**Location:** `src/services/emailService.ts:34`
**Severity:** High

**Current:**
```ts
try {
  await sendWelcomeEmail(user);
} catch (e) {
  // silently ignored
}
```

**Problem:** If email sending fails, the error is lost. The caller has no idea
the email was never sent. This also makes debugging impossible.

**Recommended Fix:**
```ts
try {
  await sendWelcomeEmail(user);
} catch (e) {
  // Email is non-critical — log and continue, but don't fail registration
  logger.warn({ err: e, userId: user.id }, 'Welcome email failed — will not retry');
  metrics.increment('email.welcome.failed');
}
```

---

### Issue: No Retry on Transient Failures
**Location:** `src/clients/inventoryClient.ts:89`

**Recommended Pattern:**
```ts
import { retry } from 'async-retry'; // or implement manually

const stock = await retry(
  async () => {
    const res = await fetch(`${INVENTORY_URL}/stock/${productId}`);
    if (res.status === 503) throw new Error('Service unavailable'); // retriable
    if (!res.ok) throw Object.assign(new Error('Inventory error'), { bail: true }); // not retriable
    return res.json();
  },
  { retries: 3, factor: 2, minTimeout: 200, maxTimeout: 5000 }
);
```
```

## Examples

### Example Input
```python
def get_user_profile(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    data = response.json()
    return data['profile']
```

### Example Output
```python
import time
import logging

logger = logging.getLogger(__name__)

def get_user_profile(user_id: str, max_retries: int = 3) -> dict:
    """Fetch user profile with retry on transient errors."""
    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"https://api.example.com/users/{user_id}",
                timeout=5  # always set a timeout
            )
            if response.status_code == 404:
                return None  # not found — don't retry
            response.raise_for_status()
            data = response.json()
            return data.get('profile')  # safe .get() instead of direct key access

        except (requests.Timeout, requests.ConnectionError) as e:
            last_error = e
            if attempt < max_retries - 1:
                backoff = 0.2 * (2 ** attempt)
                logger.warning("Retrying get_user_profile (attempt %d): %s", attempt + 1, e)
                time.sleep(backoff)

    logger.error("get_user_profile failed after %d attempts: %s", max_retries, last_error)
    raise RuntimeError(f"Could not fetch profile for user {user_id}") from last_error
```

## Boundaries

- Do NOT add retry logic to non-idempotent operations (POST, state-mutating calls) without adding idempotency keys.
- Do NOT recommend catching `BaseException` / `Throwable` / `panic` unless there's a very specific reason.
- Do NOT add circuit breakers to every call — reserve for high-volume calls to potentially unreliable dependencies.
- Do NOT return raw exception messages to API clients — sanitize and log; return a generic message externally.
- Do NOT add retries that could amplify load on an already-overloaded downstream service — always use backoff + jitter.
- If the error handling strategy requires a specific library (e.g., `resilience4j`, `tenacity`, `async-retry`), check if it's already in the project's dependencies before recommending.
