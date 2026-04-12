---
name: load-test-script-generator
description: Generates load testing scripts for k6, Locust, or JMeter from an OpenAPI spec or recorded traffic, including ramp-up scenarios. Invoke when asked to create load tests, write performance tests, generate k6 scripts, simulate traffic, or test API capacity.
---

# Load Test Script Generator

Generates realistic, production-equivalent load testing scripts for k6, Locust, or JMeter from OpenAPI specifications, recorded HTTP traffic, or natural-language descriptions — including ramp-up profiles, realistic think times, authentication, and meaningful assertions.

## When to Use

- User asks to "create load tests", "write a k6 script", or "simulate traffic"
- API capacity or breaking point needs to be determined before a launch
- Performance SLAs need to be verified (p99 latency < 200ms, 1000 RPS target)
- A deployment change may impact performance and regression testing is needed
- User provides an OpenAPI spec and wants load tests generated for all endpoints
- Production traffic patterns need to be replayed or simulated

## Process

1. **Identify the target tool** from context or recommend:
   - **k6** (default for most cases): JavaScript DSL, great for developers, excellent CI integration, detailed metrics
   - **Locust**: Python, highly customizable, good for complex user flow simulation
   - **JMeter**: Java GUI + XML DSL, enterprise standard, extensive protocol support
   - **Artillery**: JavaScript/YAML, simpler scenarios, good for API testing

2. **Gather test parameters**:
   - Target base URL and authentication method (API key, Bearer token, Basic auth)
   - Target RPS or virtual user (VU) count
   - Test duration and ramp-up profile
   - Acceptable thresholds: P95/P99 latency, error rate, throughput
   - Specific endpoints or user flows to test

3. **Parse the input** (OpenAPI spec, HAR file, curl commands, or description):
   - Extract endpoints, methods, path/query parameters, and request body schemas
   - Identify required headers and authentication
   - Note endpoints with different load characteristics (read-heavy vs. write-heavy)

4. **Design the load profile** (ramp-up → steady state → scale-down):
   - **Smoke test**: 1–5 VUs for 30s to verify the script works
   - **Load test**: ramp to target load, hold for 5–10 minutes, ramp down
   - **Stress test**: gradually increase beyond target until error rate spikes
   - **Spike test**: sudden burst to 10× normal load for 1 minute
   - **Soak test**: target load for 1–4 hours to detect memory leaks or degradation

5. **Add realistic behavior**:
   - **Think time**: `sleep(Math.random() * 2 + 1)` between requests (1–3s)
   - **Data variation**: parameterize requests with a data set (user IDs, search terms)
   - **Session simulation**: login, perform actions, logout (realistic user flow)
   - **Correlation**: extract tokens/IDs from responses and use in subsequent requests

6. **Add assertions/checks**:
   - HTTP status code is as expected (200, 201, etc.)
   - Response body contains expected fields
   - Response time under threshold
   - Define `thresholds` that cause the test to fail if SLAs are breached

7. **Add parameterization** so the script can be run for different environments/load levels via env vars.

## Output Format

### k6 Script
```javascript
// load-tests/api.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const productLatency = new Trend('product_request_duration');

// Test configuration — override with K6_VUS, K6_DURATION env vars
export const options = {
  stages: [
    { duration: '1m', target: 10 },   // Ramp up to 10 VUs over 1 minute
    { duration: '5m', target: 50 },   // Ramp up to target load
    { duration: '10m', target: 50 },  // Hold at target load
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],          // Error rate < 1%
    http_req_duration: ['p(95)<500'],        // 95th percentile < 500ms
    http_req_duration: ['p(99)<1000'],       // 99th percentile < 1s
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';
const API_KEY = __ENV.API_KEY;

// Test data — rotate through to simulate realistic access patterns
const TEST_PRODUCT_IDS = ['prod_001', 'prod_002', 'prod_003', 'prod_004', 'prod_005'];

export default function () {
  const productId = TEST_PRODUCT_IDS[Math.floor(Math.random() * TEST_PRODUCT_IDS.length)];

  // GET /products/:id
  const res = http.get(`${BASE_URL}/products/${productId}`, {
    headers: { 'X-API-Key': API_KEY, 'Content-Type': 'application/json' },
  });

  productLatency.add(res.timings.duration);
  errorRate.add(res.status !== 200);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'has product id': (r) => r.json('id') === productId,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(Math.random() * 2 + 1); // 1-3 second think time
}
```

## Examples

### Example Input
```
Generate k6 load tests for our checkout API:
POST /api/orders — create order (authenticated, JWT Bearer)
GET /api/orders/:id — fetch order status
Target: 200 concurrent users, p99 latency < 1s, error rate < 0.5%
```

### Example Output (summary)
```
load-tests/checkout.k6.js

Stages:
  0–2 min:  ramp 0→200 VUs
  2–12 min: hold at 200 VUs
  12–14 min: ramp 200→0 VUs

User flow per VU:
  1. POST /api/orders (with randomized order data from 100-item dataset)
  2. Extract orderId from response
  3. GET /api/orders/:orderId (using correlated ID from step 1)
  4. sleep(1-3s)

Thresholds (test fails if breached):
  http_req_failed < 0.5%
  http_req_duration p(99) < 1000ms

Run commands:
  # Smoke test
  k6 run --vus 2 --duration 30s load-tests/checkout.k6.js

  # Full load test
  BASE_URL=https://staging.api.example.com \
  JWT_TOKEN=$TOKEN \
  k6 run load-tests/checkout.k6.js
```

## Boundaries

- Do NOT run load tests against production without explicit confirmation — always default to a staging/test environment.
- Do NOT hardcode authentication tokens in script files — always read from environment variables.
- Do NOT generate tests that create unrealistic traffic patterns (e.g., 0 think time, all identical requests) — real-world variance is essential.
- Do NOT set thresholds so loose that the test never fails — thresholds should reflect actual SLA requirements.
- Warn if the OpenAPI spec contains endpoints that mutate shared data (user creation, payment processing) — these require careful data isolation to avoid corrupting test/staging environments.
- Do NOT generate JMeter XML without noting that it requires JMeter to be installed and cannot be easily reviewed as code.
