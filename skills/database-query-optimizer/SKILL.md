---
name: database-query-optimizer
description: Analyzes SQL or NoSQL queries, explains query plans, and rewrites them for better performance. Invoke when asked to optimize a query, speed up a slow database call, analyze a query plan, add indexes, or fix N+1 query problems.
---

# Database Query Optimizer

Analyzes SQL and NoSQL queries for performance bottlenecks, interprets query execution plans, and rewrites queries or proposes schema/index changes to reduce latency and resource usage.

## When to Use

- User shares a slow query or reports high database latency
- `EXPLAIN` / `EXPLAIN ANALYZE` output shows sequential scans, hash joins on large tables, or high cost estimates
- Application performance profiling identifies database calls as the bottleneck
- An ORM is generating N+1 queries
- User asks to add indexes to improve query performance
- A query times out in production under load

## Process

1. **Understand the query context**:
   - What database engine? (PostgreSQL, MySQL, SQLite, MongoDB, DynamoDB, etc.)
   - What is the approximate table size and cardinality of key columns?
   - Are there existing indexes? (request `\d tablename` or `SHOW INDEX FROM tablename` if not provided)
   - What is the acceptable latency target?

2. **Parse and analyze the query**:
   - Identify which tables are scanned and which are indexed lookups
   - Look for `SELECT *` — replace with explicit column list
   - Find unindexed filter columns in `WHERE`, `JOIN ON`, and `ORDER BY` clauses
   - Spot functions applied to indexed columns (`WHERE LOWER(email) = ...`) that defeat indexes
   - Identify correlated subqueries that execute once per row
   - Check for `DISTINCT` or `GROUP BY` on large result sets without filtering first
   - Look for `OFFSET`-based pagination on large tables (use keyset pagination instead)

3. **Read and interpret the query plan** (if provided):
   - `Seq Scan` on a large table → missing index
   - `Hash Join` with high rows → consider indexed nested loop join
   - High `actual time` vs `estimated rows` → stale statistics, run `ANALYZE`
   - `Sort` node with high cost → add index that provides sort order
   - `Nested Loop` with large outer table → may need to rewrite as CTE or temp table

4. **Propose optimizations in priority order**:
   - **Index additions**: most impactful, lowest risk
   - **Query rewrite**: equivalent logic, better plan
   - **Schema changes**: denormalization, partitioning (higher effort, note trade-offs)
   - **Application-level**: batching, caching, connection pooling

5. **Write the optimized query** and explain the improvement.

6. **Suggest the index DDL** with justification.

7. **Estimate the improvement** based on query plan changes (e.g., "reduces rows scanned from 500k to ~200").

## Output Format

```
## Query Analysis

### Original Query
```sql
SELECT DISTINCT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE LOWER(u.email) LIKE '%@example.com'
GROUP BY u.name
ORDER BY order_count DESC;
```

### Issues Found

1. **Function on indexed column** (`LOWER(u.email)`) — prevents index use on `email`.
2. **Leading wildcard** in LIKE (`'%@example.com'`) — forces full table scan.
3. **SELECT DISTINCT + GROUP BY** is redundant — DISTINCT can be removed.
4. **No index** on `orders.user_id` — the JOIN causes a sequential scan of `orders`.

### Optimized Query
```sql
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.email ILIKE '%@example.com'  -- or store domain separately
GROUP BY u.id, u.name
ORDER BY order_count DESC;
```

### Recommended Indexes
```sql
-- Enables fast join on orders table
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);

-- For domain-based filtering, consider a generated column:
ALTER TABLE users ADD COLUMN email_domain TEXT GENERATED ALWAYS AS
  (split_part(email, '@', 2)) STORED;
CREATE INDEX idx_users_email_domain ON users(email_domain);
```

### Expected Improvement
- `idx_orders_user_id` reduces JOIN cost from Seq Scan (O(n)) to Index Scan (O(log n))
- Estimated query time: 2400ms → ~80ms for typical dataset of 100k users / 2M orders
```

## Examples

### Example Input (N+1 Problem)
```python
# ORM generating N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # triggers 1 query per user
```

### Example Output
```python
# Fix: use select_related to JOIN in a single query
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)  # no additional queries

# SQL generated (1 query instead of N+1):
# SELECT users.*, profiles.* FROM users
# INNER JOIN profiles ON profiles.user_id = users.id
```

## Boundaries

- Do NOT suggest schema changes (adding columns, partitioning) without explicitly noting the migration effort and potential downtime.
- Do NOT recommend `CREATE INDEX` without `CONCURRENTLY` on production PostgreSQL tables — blocking locks can cause outages.
- Do NOT assume cardinality or data distribution — ask if needed for accurate advice.
- Do NOT rewrite stored procedures or triggers unless explicitly asked.
- If the query plan is not provided, flag that recommendations are based on static analysis only and may not reflect actual execution behavior.
- Do NOT recommend disabling query planner features (e.g., `enable_seqscan = off`) as a production fix.
- NoSQL (MongoDB, DynamoDB) optimization follows different principles — confirm the query type before applying SQL-specific advice.
