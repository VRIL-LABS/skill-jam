---
name: cache-advisor
description: Recommends caching strategies (in-memory, Redis, CDN) based on access patterns and suggests TTL policies and invalidation logic. Invoke when asked to add caching, reduce database load, improve API response times, choose a caching strategy, or implement cache invalidation.
---

# Cache Advisor

Analyzes application access patterns, data volatility, and infrastructure to recommend the right caching layer (in-memory, Redis, CDN, HTTP), appropriate TTL policies, and cache invalidation strategies that improve performance without introducing stale data risks.

## When to Use

- User asks to "add caching", "reduce DB load", or "speed up this endpoint"
- Database queries are repeated for the same data within short time windows
- API response times are slow due to expensive computations or downstream calls
- User asks about Redis, Memcached, CDN caching, or HTTP cache headers
- Cache invalidation logic is missing or incorrect (stale data issues)
- User asks about cache-aside, write-through, or write-behind patterns

## Process

1. **Understand the data characteristics**:
   - **Read frequency**: how often is this data read? (per second, per minute)
   - **Write frequency**: how often does it change? (real-time vs. hourly vs. rarely)
   - **Consistency requirements**: is stale data acceptable? For how long?
   - **Data size**: bytes per cached object × expected cardinality = total cache memory
   - **Sharing**: is data per-user (private) or shared (public)?

2. **Choose the appropriate caching layer**:

   | Layer | Best For | Examples |
   |-------|----------|---------|
   | In-process (in-memory) | Same-instance, low-latency, single-node | `lru-cache`, Python `functools.lru_cache`, Go `sync.Map` |
   | Distributed cache | Multi-instance, session data, shared state | Redis, Memcached |
   | HTTP cache headers | Public API responses, browser + proxy caching | `Cache-Control`, `ETag`, `Last-Modified` |
   | CDN | Static assets, geographically distributed reads | Cloudflare, Fastly, CloudFront |
   | Database query cache | Repeated identical queries | Redis, query result caching |

3. **Select the caching pattern**:
   - **Cache-Aside (Lazy Loading)**: check cache → if miss, fetch from source → populate cache → return. Simple, but first request always misses.
   - **Write-Through**: write to cache and DB simultaneously. Cache always current, but write latency is higher.
   - **Write-Behind (Write-Back)**: write to cache, async flush to DB. Low write latency, risk of data loss on crash.
   - **Read-Through**: cache sits in front of DB; cache handles misses transparently. Requires cache-DB integration.
   - **Refresh-Ahead**: proactively refresh cache before expiry based on access patterns. Reduces miss rate.

4. **Design the TTL policy**:
   - Start conservative (shorter TTL) and increase based on observed cache hit rate
   - Consider the cost of stale data vs. the cost of a cache miss
   - Use sliding TTL (reset on access) for user session data
   - Use fixed TTL for time-sensitive data (stock prices, availability)
   - Add jitter to TTL (±10%) to prevent cache stampede (all keys expiring simultaneously)

5. **Design the invalidation strategy**:
   - **TTL-based**: simplest; accept eventual consistency for the TTL window
   - **Event-driven**: invalidate on write/delete events (database triggers, message queue events)
   - **Tag-based**: group related keys under tags, invalidate the tag to evict all related entries
   - **Versioned keys**: `user:123:v5` — bump version on invalidation; old entries expire naturally

6. **Identify cache stampede risks** and add protection:
   - Probabilistic Early Expiration (PER) / XFetch algorithm
   - Locking: only one process fetches on miss, others wait
   - Background refresh before TTL expires

7. **Generate code** for the recommended cache implementation.

## Output Format

```
## Caching Recommendation

**Endpoint:** `GET /api/products/:id`
**Current behavior:** Queries PostgreSQL on every request (~45ms avg)
**Read rate:** ~500 req/s · **Write rate:** ~5 updates/hour

### Recommendation: Redis Cache-Aside with 5-minute TTL

**Rationale:** Products change infrequently (5/hour) but are read very frequently
(500 req/s). A 5-minute TTL means at most 5 minutes of stale data — acceptable
for a product catalog. Redis is appropriate since the app runs multiple instances.

### Implementation
```ts
const PRODUCT_TTL = 5 * 60; // 5 minutes in seconds

async function getProduct(id: string): Promise<Product> {
  const cacheKey = `product:${id}`;

  // Check cache first
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Cache miss — fetch from DB
  const product = await db.products.findById(id);
  if (!product) return null;

  // Populate cache with jitter to prevent stampede
  const ttl = PRODUCT_TTL + Math.floor(Math.random() * 30);
  await redis.setex(cacheKey, ttl, JSON.stringify(product));

  return product;
}

// Invalidate on update
async function updateProduct(id: string, data: Partial<Product>) {
  const updated = await db.products.update(id, data);
  await redis.del(`product:${id}`); // event-driven invalidation
  return updated;
}
```

**Expected impact:** ~45ms → ~2ms for cached requests (~98% cache hit rate expected)
```

## Examples

### Example Input
```
We have a user profile endpoint hit 1000 times/second. Profiles change rarely
(user updates their profile maybe once a week). Currently hitting Postgres every time.
```

### Example Output
```
Recommendation: In-process LRU cache (primary) + Redis (secondary/shared)

- In-process LRU: 10,000 entries, TTL 60s — serves ~80% of requests with <1ms latency
- Redis fallback: TTL 10 minutes — handles cache misses from in-process eviction
- Invalidation: on profile update, delete from both Redis and broadcast to app instances
  via Redis pub/sub to clear in-process caches

At 1000 req/s with 60s TTL, expect >99% hit rate. DB load drops from 1000 QPS to ~10 QPS.
```

## Boundaries

- Do NOT recommend caching for highly volatile data (financial account balances, inventory counts in checkout flows) without explicitly noting the consistency risk.
- Do NOT recommend in-process caching for multi-instance deployments without noting that each instance has its own cache (no shared state).
- Do NOT cache responses containing user-specific data in a shared (public) cache layer.
- Do NOT recommend turning off cache TTLs (no expiry) without a clearly defined invalidation strategy.
- Always recommend TTL jitter when caching many keys with the same expiry time.
- Do NOT assume Redis is available — if not detected in the project, suggest it as a new dependency and note the operational overhead.
