---
name: performance-profiler
description: Interprets profiling output (flame graphs, heap dumps, perf reports) and highlights the top bottlenecks with optimization advice. Invoke when asked to analyze performance data, interpret a flame graph, diagnose slow code, reduce CPU or memory usage, or find hot paths.
---

# Performance Profiler

Interprets CPU profiles, heap dumps, flame graphs, and runtime metrics to identify the top performance bottlenecks and provide actionable, prioritized optimization recommendations.

## When to Use

- User shares a flame graph, `perf` report, pprof output, or profiler snapshot
- Application latency or CPU usage is higher than acceptable thresholds
- Memory usage grows over time (potential memory leak)
- User asks "why is this slow?" or "what's consuming the most CPU/memory?"
- Load testing reveals specific endpoints or functions as bottlenecks
- GC pressure or event loop lag is impacting throughput

## Process

1. **Identify the profiling format and runtime**:
   - Node.js: V8 CPU profile (JSON), `clinic flame`, `0x` flamegraph, heap snapshot
   - Python: `cProfile`/`pstats` output, `py-spy` SVG, `memray` reports
   - Go: `pprof` CPU/memory profile, `go tool pprof` text output
   - JVM: JFR recording, VisualVM snapshot, async-profiler flamegraph
   - Native: Linux `perf record`/`perf report`, Instruments (macOS)
   - Ruby: `stackprof` output, `rbspy`

2. **Parse the top consumers** from the profile:
   - For CPU profiles: identify functions with the highest **self time** (on-CPU, not waiting on callees) and highest **total time** (cumulative including callees)
   - For heap profiles: identify allocation sites with the most bytes retained vs. allocated
   - For flame graphs: find the widest frames (most time spent) — especially wide leaves

3. **Categorize bottlenecks**:
   - **CPU-bound**: tight loops, expensive algorithms, redundant recomputation → optimize algorithm, add caching, parallelize
   - **I/O-bound**: blocking disk/network calls in hot paths → make async, batch, prefetch
   - **Memory**: large object allocations, object leaks, excessive GC → pool objects, fix leaks, reduce allocation rate
   - **Contention**: lock contention, mutex hotspots → reduce lock scope, use lock-free structures
   - **GC pressure**: high allocation rate causing frequent GC pauses → object pooling, reduce allocations

4. **Rank findings by impact** — estimate the % of total time or bytes each bottleneck represents.

5. **Propose concrete optimizations** for the top 3–5 bottlenecks:
   - Show the current code (if available) and the optimized version
   - Explain the mechanism of improvement (e.g., "reduces O(n²) to O(n log n)")
   - Estimate the expected improvement if possible

6. **Check for common runtime-specific anti-patterns**:
   - Node.js: synchronous fs calls, `JSON.parse` on large payloads in event loop, unresolved promises accumulating
   - Python: CPython GIL contention in CPU-bound multithreaded code, list comprehensions on large datasets vs. generators
   - Go: goroutine leaks, channel operations in tight loops, interface boxing allocations
   - JVM: autoboxing, string concatenation in loops, excessive object creation in hot paths

7. **Recommend profiling tooling improvements** if the current data is insufficient for diagnosis.

## Output Format

```
## Performance Analysis Report

**Profile type:** CPU Flame Graph (Node.js, 30s capture under load)
**Total samples:** 15,420

---

### Top Bottlenecks

| Rank | Function | Self % | Total % | Category |
|------|----------|--------|---------|----------|
| 1 | `processPayload` (src/worker.js:44) | 34% | 58% | CPU-bound |
| 2 | `JSON.parse` (built-in) | 22% | 22% | CPU-bound |
| 3 | `getFromDatabase` (src/db.js:112) | 18% | 18% | I/O wait |

---

### Finding 1: Redundant JSON Parsing (34% → potentially 10%)
`processPayload` calls `JSON.parse(JSON.stringify(obj))` to deep-clone objects.
This is extremely expensive at high throughput.

**Fix:** Use a structured clone or a purpose-built deep-clone library:
```js
// ❌ Current — expensive serialization round-trip
const copy = JSON.parse(JSON.stringify(data));

// ✅ Fix — use structuredClone (Node 17+) or lodash cloneDeep
const copy = structuredClone(data);
```
**Estimated saving:** ~24% CPU reduction based on profile weight.

---

### Finding 2: Synchronous Database Calls Blocking Event Loop
`getFromDatabase` uses the synchronous sqlite3 API, blocking the event loop
for up to 18ms per call under load.

**Fix:** Migrate to the async API or use `better-sqlite3` with worker threads
to keep the event loop free.
```

## Examples

### Example Input
```
Python cProfile output (sorted by cumulative time):
   ncalls  tottime  cumtime  filename:lineno(function)
   100000    8.234   21.456  process.py:34(transform_record)
   100000    0.123   13.222  validate.py:12(validate_schema)
  1000000   12.100   12.100  {method 'match' of 're.Pattern'}
```

### Example Output
```
## Analysis

**Top bottleneck: regex compilation in hot path (12.1s / 56% of total)**

`validate_schema` (called 100,000 times) recompiles regex patterns on every call.
`re.match(pattern_string, ...)` recompiles the pattern each invocation.

**Fix:** Compile patterns once at module load:
```python
# ❌ Current — recompiles on every call
def validate_schema(value):
    return re.match(r'^[a-z0-9_]+$', value)

# ✅ Fix — compile once
_PATTERN = re.compile(r'^[a-z0-9_]+$')

def validate_schema(value):
    return _PATTERN.match(value)
```
**Estimated saving:** 10–12 seconds (eliminating repeated compilation overhead).
```

## Boundaries

- Do NOT recommend premature optimization — only optimize code that shows up in the actual profile.
- Do NOT suggest algorithmic rewrites without reviewing the actual function code.
- If profile data is ambiguous or incomplete, state what additional data would be needed for a confident diagnosis.
- Do NOT recommend disabling GC, using unsafe memory access, or other dangerous low-level optimizations without strong justification and caveats.
- Always measure before and after optimization — recommend adding benchmarks if they don't exist.
- Do NOT assume the bottleneck is always in application code — it may be in the database, network, or infrastructure.
