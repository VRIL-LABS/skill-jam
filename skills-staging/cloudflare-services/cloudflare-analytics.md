---
name: Cloudflare Analytics
description: |
  Cloudflare Analytics provides comprehensive traffic, performance, and security insights for your applications.
  Trigger phrases: "analytics", "metrics", "insights", "traffic analysis", "performance monitoring", "cloudflare analytics"
license: MIT
---

# Cloudflare Analytics

Cloudflare Analytics provides real-time and historical insights into your application's traffic, performance, security, and usage patterns. With powerful GraphQL APIs, customizable dashboards, and detailed metrics, you can monitor, analyze, and optimize your Cloudflare services.

## When to Use

Use Cloudflare Analytics when you need to:
- **Monitor traffic patterns**: Track requests, bandwidth, and visitor behavior
- **Analyze performance**: Measure response times, cache hit rates, and optimization metrics
- **Track security threats**: Identify attacks, bot traffic, and security events
- **Measure Workers usage**: Monitor compute time, subrequest counts, and errors
- **Build custom dashboards**: Create tailored visualizations with GraphQL API
- **Generate reports**: Export data for analysis and business intelligence
- **Optimize costs**: Understand resource usage and billing metrics
- **Debug issues**: Investigate errors, slow requests, and anomalies

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/analytics/
- **GraphQL Analytics API**: https://developers.cloudflare.com/analytics/graphql-api/
- **Analytics Engine**: https://developers.cloudflare.com/analytics/analytics-engine/
- **Web Analytics**: https://developers.cloudflare.com/analytics/web-analytics/
- **Logs**: https://developers.cloudflare.com/logs/
- **Account Analytics**: https://developers.cloudflare.com/analytics/account-and-zone-analytics/

## Quick Start

### 1. Access Dashboard Analytics

Visit the Cloudflare Dashboard:
1. Navigate to your zone (domain)
2. Click **Analytics & Logs** → **Traffic**
3. Explore metrics: requests, bandwidth, threats, performance

### 2. Set Up API Access

Create an API token:

```bash
# Using Cloudflare Dashboard
# Go to: Profile → API Tokens → Create Token
# Template: Read Analytics

# Or use curl to test
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/analytics/dashboard" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### 3. Query with GraphQL

```bash
# GraphQL endpoint
https://api.cloudflare.com/client/v4/graphql
```

Example query:

```graphql
query {
  viewer {
    zones(filter: { zoneTag: "YOUR_ZONE_ID" }) {
      httpRequests1dGroups(
        limit: 10
        filter: { date_gt: "2024-01-01" }
      ) {
        dimensions {
          date
        }
        sum {
          requests
          bytes
          threats
        }
        uniq {
          uniques
        }
      }
    }
  }
}
```

### 4. Use Analytics Engine in Workers

```javascript
// wrangler.toml
[[analytics_engine_datasets]]
binding = "ANALYTICS"

// worker.js
export default {
  async fetch(request, env) {
    const startTime = Date.now();
    
    // Your application logic
    const response = await handleRequest(request);
    
    // Write analytics data point
    env.ANALYTICS.writeDataPoint({
      indexes: [request.url, request.method],
      blobs: [
        request.headers.get('user-agent'),
        request.cf.country,
      ],
      doubles: [
        Date.now() - startTime, // response time
        response.status,
      ],
    });
    
    return response;
  },
};
```

## Core Features

### Zone Analytics API

#### HTTP Requests Analytics

```javascript
async function getHTTPAnalytics(zoneId, apiToken) {
  const query = `
    query {
      viewer {
        zones(filter: { zoneTag: "${zoneId}" }) {
          httpRequests1hGroups(
            limit: 24
            filter: { datetime_gt: "2024-01-01T00:00:00Z" }
          ) {
            dimensions {
              datetime
            }
            sum {
              requests
              cachedRequests
              bytes
              cachedBytes
              threats
              pageViews
            }
            avg {
              sampleInterval
            }
          }
        }
      }
    }
  `;
  
  const response = await fetch('https://api.cloudflare.com/client/v4/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  
  return response.json();
}
```

#### Performance Metrics

```javascript
const query = `
  query {
    viewer {
      zones(filter: { zoneTag: "${zoneId}" }) {
        httpRequests1dGroups(
          limit: 7
          filter: { date_geq: "2024-01-01", date_lt: "2024-01-08" }
        ) {
          dimensions {
            date
          }
          quantiles {
            originResponseDurationP50: originResponseDurationMsP50
            originResponseDurationP95: originResponseDurationMsP95
            originResponseDurationP99: originResponseDurationMsP99
          }
          avg {
            sampleInterval
          }
        }
      }
    }
  }
`;
```

#### Cache Analytics

```javascript
const query = `
  query {
    viewer {
      zones(filter: { zoneTag: "${zoneId}" }) {
        httpRequests1dGroups(
          limit: 30
          filter: { date_geq: "2024-01-01" }
        ) {
          dimensions {
            date
          }
          sum {
            requests
            cachedRequests
            bytes
            cachedBytes
          }
          ratio {
            cacheHitRate: cachedRequests
            bandwidthSaved: cachedBytes
          }
        }
      }
    }
  }
`;
```

### Analytics Engine

#### Writing Data Points

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const startTime = Date.now();
    
    try {
      const response = await handleRequest(request);
      const duration = Date.now() - startTime;
      
      // Write analytics
      env.ANALYTICS.writeDataPoint({
        // Indexed fields (filterable)
        indexes: [
          url.pathname,
          request.method,
          response.status.toString(),
          request.cf.colo, // Cloudflare data center
        ],
        // Non-indexed fields
        blobs: [
          request.headers.get('user-agent') || 'unknown',
          request.cf.country || 'XX',
          request.cf.city || 'unknown',
        ],
        // Numeric fields
        doubles: [
          duration,
          parseInt(response.headers.get('content-length') || '0'),
        ],
      });
      
      return response;
    } catch (error) {
      // Track errors
      env.ANALYTICS.writeDataPoint({
        indexes: ['error', url.pathname, error.name],
        blobs: [error.message],
        doubles: [Date.now() - startTime],
      });
      
      throw error;
    }
  },
};
```

#### Querying Analytics Engine

```sql
-- SQL API for Analytics Engine
SELECT
  index1 as path,
  index2 as method,
  index3 as status,
  COUNT() as requests,
  AVG(double1) as avg_duration_ms,
  QUANTILE(double1, 0.95) as p95_duration_ms,
  SUM(double2) as total_bytes
FROM ANALYTICS_DATASET
WHERE
  timestamp >= NOW() - INTERVAL '24' HOUR
  AND index1 = '/api/users'
GROUP BY index1, index2, index3
ORDER BY requests DESC
```

GraphQL query for Analytics Engine:

```javascript
const query = `
  query {
    viewer {
      accounts(filter: { accountTag: "${accountId}" }) {
        analyticsEngineDatasets(filter: { name: "default" }) {
          name
          query(
            query: """
              SELECT
                index1 as endpoint,
                COUNT() as requests,
                AVG(double1) as avg_response_time
              FROM default
              WHERE timestamp >= NOW() - INTERVAL '1' HOUR
              GROUP BY endpoint
              ORDER BY requests DESC
              LIMIT 10
            """
          ) {
            rows
          }
        }
      }
    }
  }
`;
```

### Workers Analytics

```javascript
const query = `
  query {
    viewer {
      accounts(filter: { accountTag: "${accountId}" }) {
        workersInvocationsAdaptive(
          limit: 100
          filter: {
            datetime_geq: "2024-01-01T00:00:00Z"
            datetime_lt: "2024-01-02T00:00:00Z"
            scriptName: "my-worker"
          }
        ) {
          dimensions {
            datetime
            scriptName
            status
          }
          sum {
            requests
            subrequests
            errors
          }
          quantiles {
            cpuTimeP50
            cpuTimeP95
            cpuTimeP99
          }
        }
      }
    }
  }
`;
```

### Firewall Analytics

```javascript
const query = `
  query {
    viewer {
      zones(filter: { zoneTag: "${zoneId}" }) {
        firewallEventsAdaptive(
          limit: 100
          filter: {
            datetime_geq: "2024-01-01T00:00:00Z"
            datetime_lt: "2024-01-02T00:00:00Z"
          }
        ) {
          dimensions {
            datetime
            action
            ruleId
            source
            clientCountryName
          }
          sum {
            count
          }
        }
      }
    }
  }
`;
```

## Common Use Cases

### Custom Dashboard

```javascript
// Worker that serves analytics dashboard
export default {
  async fetch(request, env) {
    const analytics = await fetchAnalytics(env);
    
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Analytics Dashboard</title>
          <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
          <h1>Traffic Analytics</h1>
          <canvas id="requestsChart"></canvas>
          <script>
            const data = ${JSON.stringify(analytics)};
            
            new Chart(document.getElementById('requestsChart'), {
              type: 'line',
              data: {
                labels: data.map(d => d.date),
                datasets: [{
                  label: 'Requests',
                  data: data.map(d => d.requests),
                  borderColor: 'rgb(75, 192, 192)',
                }]
              }
            });
          </script>
        </body>
      </html>
    `;
    
    return new Response(html, {
      headers: { 'Content-Type': 'text/html' },
    });
  },
};

async function fetchAnalytics(env) {
  const query = `
    query {
      viewer {
        zones(filter: { zoneTag: "${env.ZONE_ID}" }) {
          httpRequests1dGroups(limit: 30) {
            dimensions { date }
            sum { requests }
          }
        }
      }
    }
  `;
  
  const response = await fetch('https://api.cloudflare.com/client/v4/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.API_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  
  const result = await response.json();
  return result.data.viewer.zones[0].httpRequests1dGroups;
}
```

### API Usage Tracking

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const apiKey = request.headers.get('X-API-Key');
    const startTime = Date.now();
    
    // Handle request
    const response = await handleAPIRequest(request);
    const duration = Date.now() - startTime;
    
    // Track API usage
    env.ANALYTICS.writeDataPoint({
      indexes: [
        apiKey,
        url.pathname,
        request.method,
        response.status.toString(),
      ],
      blobs: [
        request.cf.country,
        url.searchParams.get('version') || 'v1',
      ],
      doubles: [
        duration,
        1, // request count
      ],
    });
    
    return response;
  },
};

// Query API usage
async function getAPIUsageReport(env) {
  const query = `
    SELECT
      index1 as api_key,
      index2 as endpoint,
      COUNT() as requests,
      AVG(double1) as avg_response_time_ms,
      SUM(double2) as total_requests
    FROM api_analytics
    WHERE timestamp >= NOW() - INTERVAL '30' DAY
    GROUP BY api_key, endpoint
    ORDER BY total_requests DESC
  `;
  
  // Execute query and return results
}
```

### Performance Monitoring

```javascript
export default {
  async fetch(request, env) {
    const startTime = Date.now();
    const timings = {};
    
    // Track database query
    const dbStart = Date.now();
    const data = await env.DB.prepare('SELECT * FROM users').all();
    timings.database = Date.now() - dbStart;
    
    // Track external API call
    const apiStart = Date.now();
    const apiResponse = await fetch('https://api.example.com/data');
    timings.externalAPI = Date.now() - apiStart;
    
    // Track rendering
    const renderStart = Date.now();
    const html = renderTemplate(data.results);
    timings.rendering = Date.now() - renderStart;
    
    const totalTime = Date.now() - startTime;
    
    // Write performance metrics
    env.ANALYTICS.writeDataPoint({
      indexes: ['performance', request.url],
      blobs: [request.cf.colo],
      doubles: [
        totalTime,
        timings.database,
        timings.externalAPI,
        timings.rendering,
      ],
    });
    
    return new Response(html, {
      headers: {
        'Content-Type': 'text/html',
        'Server-Timing': `
          db;dur=${timings.database},
          api;dur=${timings.externalAPI},
          render;dur=${timings.rendering},
          total;dur=${totalTime}
        `.trim(),
      },
    });
  },
};
```

### Error Tracking

```javascript
export default {
  async fetch(request, env) {
    try {
      return await handleRequest(request);
    } catch (error) {
      // Log error with context
      env.ANALYTICS.writeDataPoint({
        indexes: [
          'error',
          error.name,
          request.url,
          request.method,
        ],
        blobs: [
          error.message,
          error.stack || '',
          request.headers.get('user-agent') || '',
          request.cf.country || '',
        ],
        doubles: [
          Date.now(),
          1, // error count
        ],
      });
      
      return new Response('Internal Server Error', { status: 500 });
    }
  },
};

// Query error rates
const errorQuery = `
  SELECT
    index2 as error_type,
    blob1 as error_message,
    COUNT() as occurrences,
    MIN(timestamp) as first_seen,
    MAX(timestamp) as last_seen
  FROM error_analytics
  WHERE
    timestamp >= NOW() - INTERVAL '24' HOUR
    AND index1 = 'error'
  GROUP BY error_type, error_message
  ORDER BY occurrences DESC
  LIMIT 20
`;
```

### Business Metrics

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/checkout/complete') {
      const orderData = await request.json();
      
      // Track business metrics
      env.ANALYTICS.writeDataPoint({
        indexes: [
          'conversion',
          orderData.productCategory,
          orderData.paymentMethod,
          request.cf.country,
        ],
        blobs: [
          orderData.customerId,
          orderData.campaignSource || 'direct',
        ],
        doubles: [
          orderData.orderValue,
          orderData.itemCount,
          1, // conversion count
        ],
      });
      
      return Response.json({ success: true });
    }
    
    return handleRequest(request);
  },
};

// Revenue analytics query
const revenueQuery = `
  SELECT
    index4 as country,
    index2 as category,
    COUNT() as orders,
    SUM(double1) as total_revenue,
    AVG(double1) as average_order_value,
    SUM(double2) as total_items
  FROM business_analytics
  WHERE
    timestamp >= NOW() - INTERVAL '30' DAY
    AND index1 = 'conversion'
  GROUP BY country, category
  ORDER BY total_revenue DESC
`;
```

## Integration

### With Workers

```javascript
export default {
  async fetch(request, env, ctx) {
    // Write analytics without blocking response
    ctx.waitUntil(
      env.ANALYTICS.writeDataPoint({
        indexes: [request.url],
        doubles: [Date.now()],
      })
    );
    
    return handleRequest(request);
  },
};
```

### With Pages

```javascript
// pages/functions/_middleware.js
export async function onRequest(context) {
  const startTime = Date.now();
  const response = await context.next();
  
  // Track page performance
  context.env.ANALYTICS.writeDataPoint({
    indexes: [
      context.request.url,
      response.status.toString(),
    ],
    doubles: [
      Date.now() - startTime,
    ],
  });
  
  return response;
}
```

### With D1

```javascript
// Combine D1 queries with analytics
export default {
  async fetch(request, env) {
    const startTime = Date.now();
    
    const result = await env.DB.prepare(
      'SELECT * FROM products WHERE category = ?'
    ).bind('electronics').all();
    
    const queryTime = Date.now() - startTime;
    
    // Track query performance
    env.ANALYTICS.writeDataPoint({
      indexes: ['d1-query', 'products', 'category-lookup'],
      doubles: [queryTime, result.results.length],
    });
    
    return Response.json(result.results);
  },
};
```

### With R2

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);
    
    const object = await env.BUCKET.get(key);
    
    if (object) {
      // Track file downloads
      env.ANALYTICS.writeDataPoint({
        indexes: ['r2-download', key],
        blobs: [request.cf.country],
        doubles: [object.size],
      });
      
      return new Response(object.body);
    }
    
    return new Response('Not found', { status: 404 });
  },
};
```

## Best Practices

### Efficient Data Collection

```javascript
// Good: Batch related metrics
env.ANALYTICS.writeDataPoint({
  indexes: [endpoint, method, status, region],
  doubles: [duration, bytes, dbTime, apiTime],
});

// Avoid: Multiple separate writes for same event
env.ANALYTICS.writeDataPoint({ indexes: [endpoint], doubles: [duration] });
env.ANALYTICS.writeDataPoint({ indexes: [endpoint], doubles: [bytes] });
```

### Index Strategy

```javascript
// Use indexes for fields you'll filter/group by
env.ANALYTICS.writeDataPoint({
  indexes: [
    'api',               // index1: filter by event type
    endpoint,            // index2: group by endpoint
    statusCode,          // index3: filter by status
    region,              // index4: analyze by region
  ],
  blobs: [
    userAgent,           // metadata, not filtered
    requestId,           // reference data
  ],
  doubles: [
    responseTime,        // aggregate metrics
    bytesSent,
  ],
});
```

### Query Optimization

```sql
-- Good: Specific time range and filters
SELECT * FROM analytics
WHERE timestamp >= NOW() - INTERVAL '1' HOUR
  AND index1 = 'api'
LIMIT 1000

-- Avoid: Open-ended queries
SELECT * FROM analytics
WHERE index1 = 'api'
```

### Cost Management

```javascript
// Sample high-volume events
export default {
  async fetch(request, env) {
    const shouldSample = Math.random() < 0.1; // 10% sample rate
    
    if (shouldSample || request.url.includes('/api/')) {
      env.ANALYTICS.writeDataPoint({
        // ... analytics data
      });
    }
    
    return handleRequest(request);
  },
};
```

## Troubleshooting

### Missing Data Points

Verify writeDataPoint calls:

```javascript
try {
  env.ANALYTICS.writeDataPoint({ /* ... */ });
} catch (error) {
  console.error('Analytics write failed:', error);
}
```

### Query Performance

Optimize queries:

```sql
-- Add time filters
WHERE timestamp >= NOW() - INTERVAL '24' HOUR

-- Limit results
LIMIT 1000

-- Use appropriate aggregations
GROUP BY index1, index2
```

### High Costs

Implement sampling:

```javascript
const SAMPLE_RATE = parseFloat(env.ANALYTICS_SAMPLE_RATE || '1.0');

if (Math.random() < SAMPLE_RATE) {
  env.ANALYTICS.writeDataPoint({ /* ... */ });
}
```

## See Also

- [Cloudflare Workers](./cloudflare-workers.md) - Serverless compute platform
- [Cloudflare Logs](https://developers.cloudflare.com/logs/) - Detailed request logs
- [Web Analytics](https://developers.cloudflare.com/analytics/web-analytics/) - Privacy-first web analytics
