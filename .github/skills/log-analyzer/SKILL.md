---
name: log-analyzer
description: Parses structured or unstructured application logs to surface error trends, anomaly spikes, and actionable insights. Invoke when asked to analyze logs, find errors in log output, investigate a production incident, identify patterns in log data, or summarize what happened in a time window.
---

# Log Analyzer

Parses structured (JSON, logfmt) and unstructured application logs to identify error trends, anomaly spikes, performance degradation patterns, and actionable insights — with a focus on operational intelligence and incident investigation.

## When to Use

- User shares log output and asks "what went wrong?"
- Investigating a production incident or outage
- High error rates are reported and root cause is unknown
- User asks to "find errors in these logs" or "summarize what happened"
- Anomaly detection is needed (spike in error rate, latency increase)
- Security events need to be identified (auth failures, unusual access patterns)

## Process

1. **Identify the log format**:
   - **Structured JSON**: parse fields like `level`, `message`, `timestamp`, `error`, `trace_id`
   - **logfmt**: `key=value` pairs, parse as structured
   - **Apache/Nginx access logs**: `$remote_addr - - [$time] "$request" $status $bytes`
   - **Syslog / journald**: `<priority>timestamp host process[pid]: message`
   - **Unstructured**: apply pattern matching and regex extraction

2. **Establish the time range and baseline**:
   - Identify the earliest and latest timestamps in the log
   - Count total log volume per minute/hour to establish baseline
   - Note any obvious time-based patterns (spikes, gaps, silent periods)

3. **Extract and count errors by type**:
   - Group by error message, exception class, or HTTP status code
   - Count occurrences and calculate error rate (errors / total requests or events)
   - Rank error types by frequency
   - Flag error rate increases compared to prior baseline period

4. **Identify anomaly spikes**:
   - Time windows with >2x normal error rate
   - Sudden appearance of a new error type
   - Latency percentiles (P99, P95) exceeding thresholds
   - Specific user IDs, IPs, or services appearing disproportionately

5. **Trace correlated events**:
   - Group log lines by `trace_id`, `request_id`, or `session_id` to reconstruct request flows
   - Find the sequence of events leading to an error
   - Identify which service or function in the call chain first logged the error

6. **Detect security events**:
   - Repeated authentication failures from the same IP (brute force)
   - Access to sensitive paths (admin, `.env`, config files)
   - Unusual HTTP methods or oversized request payloads
   - Token/session reuse anomalies

7. **Produce a structured summary** with timeline, top errors, and recommended actions.

## Output Format

```
## Log Analysis Report

**Log range:** 2024-03-15 09:00 UTC → 2024-03-15 11:30 UTC (2.5 hours)
**Total events:** 284,312
**Error rate:** 3.2% (baseline: 0.4%) — **8x elevated**

---

### Timeline
- `09:00–09:47` — Normal traffic (~1,800 req/min, 0.4% errors)
- `09:47` — 🔴 Error spike begins: `ConnectionError: DB connection pool exhausted`
- `09:47–10:15` — 28 minutes of degraded service (18% error rate)
- `10:15` — Error rate returns to baseline (likely pool expansion or traffic drop)
- `10:15–11:30` — Normal operations

---

### Top Errors (09:47–10:15 window)

| Rank | Error | Count | % of errors |
|------|-------|-------|-------------|
| 1 | `ConnectionError: DB pool exhausted` | 2,847 | 64% |
| 2 | `Timeout: downstream /api/inventory 30s` | 891 | 20% |
| 3 | `ValidationError: missing field 'quantity'` | 412 | 9% |

---

### Root Cause Analysis
The DB connection pool exhaustion at 09:47 correlates with a deployment at 09:45
(seen in logs: `[INFO] New deployment: v2.3.1`). The new version likely introduced
a connection leak or reduced the pool size. The inventory timeout errors are
a cascade effect — DB slowness caused the inventory service to time out,
generating secondary errors.

---

### Recommended Actions
1. Roll back to v2.3.0 or hot-patch the connection pool configuration
2. Add alerting on DB pool exhaustion (currently no alert exists)
3. Investigate `ValidationError` on `quantity` field — unrelated to the incident
   but represents a pre-existing issue requiring a separate fix
```

## Examples

### Example Input
```
2024-03-15T09:47:12Z ERROR ConnectionError: DB connection pool exhausted at getUser (db.js:45)
2024-03-15T09:47:13Z ERROR ConnectionError: DB connection pool exhausted at getUser (db.js:45)
2024-03-15T09:47:13Z WARN  Request timeout after 30s: GET /api/orders/123
[... 3000 more similar lines ...]
2024-03-15T10:15:02Z INFO  Health check passed. DB connections: 5/20 available
```

### Example Output
```
28-minute incident starting at 09:47 UTC.
Primary cause: DB connection pool exhaustion (64% of errors).
Secondary cascade: /api/orders timeouts due to DB unavailability (20%).

Incident resolved at ~10:15 UTC when pool recovered.
Recommend: add pool monitoring alert, review recent deployment for connection leaks.
```

## Boundaries

- Do NOT attempt to access live log streams or external logging services — only analyze log content provided in the conversation.
- Do NOT reveal PII found in logs (email addresses, user IDs, IP addresses) beyond what is necessary for the analysis — generalize where possible.
- If logs are truncated or sampled, note that findings may not represent the complete picture.
- Do NOT make definitive root cause claims without corroborating evidence — use qualified language ("likely", "correlates with").
- If log volume is too large to fully analyze in context, prioritize the error-dense time windows and note the sampling approach.
- Do NOT generate queries against logging services (Splunk, Datadog, Loki) unless the user provides the query interface and credentials are not required.
