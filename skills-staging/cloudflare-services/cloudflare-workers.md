---
name: Cloudflare Workers
description: |
  Deploy serverless JavaScript/TypeScript functions at the edge using Cloudflare Workers.
  Trigger phrases: "cloudflare workers", "edge functions", "serverless edge", "wrangler cli",
  "v8 isolates", "edge compute", "workers runtime", "cloudflare serverless"
license: MIT
---

# Cloudflare Workers

Cloudflare Workers is a serverless platform that executes JavaScript and TypeScript code at the edge across 330+ data centers worldwide. Built on V8 isolates instead of containers, Workers start in milliseconds and scale instantly without cold starts.

## When to Use

**Best for:**
- **Edge APIs**: REST/GraphQL APIs with global low-latency
- **Request transformation**: Modify requests/responses in flight
- **Authentication**: JWT validation, OAuth flows at the edge
- **Server-Side Rendering**: Render React/Vue apps close to users
- **A/B testing**: Dynamic routing based on headers/cookies
- **AI inference**: Run ML models with Workers AI
- **Caching logic**: Custom cache rules and purging
- **Webhook handlers**: Process webhooks with minimal latency

**Not ideal for:**
- Long-running computations (>30s CPU time limit)
- Large file processing (128MB memory limit)
- Applications requiring persistent TCP connections

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/workers/
- **Get Started**: https://developers.cloudflare.com/workers/get-started/guide/
- **Runtime APIs**: https://developers.cloudflare.com/workers/runtime-apis/
- **Wrangler CLI**: https://developers.cloudflare.com/workers/wrangler/
- **Bindings**: https://developers.cloudflare.com/workers/runtime-apis/bindings/
- **Examples**: https://developers.cloudflare.com/workers/examples/
- **Pricing**: https://developers.cloudflare.com/workers/platform/pricing/
- **Limits**: https://developers.cloudflare.com/workers/platform/limits/

## Quick Start

### 1. Install Wrangler CLI

```bash
# Install globally
npm install -g wrangler

# Or use with npx
npx wrangler --version

# Login to Cloudflare
wrangler login
```

### 2. Create a New Worker

```bash
# Create worker from template
npm create cloudflare@latest my-worker

# Follow prompts:
# - Select "Hello World Worker"
# - Choose TypeScript
# - Select yes for Git

cd my-worker
```

### 3. Basic Worker Example

```typescript
// src/index.ts
export interface Env {
  // Define bindings here
  MY_KV: KVNamespace;
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // Route handling
    if (url.pathname === '/api/hello') {
      return new Response(JSON.stringify({
        message: 'Hello from Cloudflare Workers!',
        location: request.cf?.city || 'Unknown',
        timestamp: new Date().toISOString()
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### 4. Deploy

```bash
# Deploy to Cloudflare
wrangler deploy

# Test locally
wrangler dev

# Tail logs
wrangler tail
```

## Core Features

### Request/Response Handling

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    // Parse request
    const url = new URL(request.url);
    const method = request.method;
    const headers = request.headers;
    
    // Handle POST with JSON body
    if (method === 'POST') {
      const body = await request.json<{ name: string }>();
      return Response.json({
        received: body,
        method: method
      });
    }
    
    // Handle GET with query params
    const name = url.searchParams.get('name') || 'World';
    
    // Custom headers
    return new Response(`Hello, ${name}!`, {
      status: 200,
      headers: {
        'Content-Type': 'text/plain',
        'X-Custom-Header': 'Workers',
        'Cache-Control': 'public, max-age=3600'
      }
    });
  }
};
```

### KV Storage Binding

```typescript
interface Env {
  CACHE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const cacheKey = url.pathname;
    
    // Try cache first
    const cached = await env.CACHE.get(cacheKey);
    if (cached) {
      return new Response(cached, {
        headers: { 'X-Cache': 'HIT' }
      });
    }
    
    // Fetch fresh data
    const data = await fetchFreshData();
    
    // Store in KV with 1 hour TTL
    await env.CACHE.put(cacheKey, data, {
      expirationTtl: 3600
    });
    
    return new Response(data, {
      headers: { 'X-Cache': 'MISS' }
    });
  }
};

async function fetchFreshData(): Promise<string> {
  return 'Fresh data from origin';
}
```

### R2 Object Storage

```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Upload file
    if (request.method === 'PUT') {
      const key = url.pathname.slice(1);
      await env.MY_BUCKET.put(key, request.body, {
        httpMetadata: {
          contentType: request.headers.get('Content-Type') || 'application/octet-stream'
        },
        customMetadata: {
          uploadedBy: 'worker',
          uploadedAt: new Date().toISOString()
        }
      });
      return Response.json({ success: true, key });
    }
    
    // Download file
    if (request.method === 'GET') {
      const key = url.pathname.slice(1);
      const object = await env.MY_BUCKET.get(key);
      
      if (!object) {
        return new Response('Not Found', { status: 404 });
      }
      
      return new Response(object.body, {
        headers: {
          'Content-Type': object.httpMetadata.contentType || 'application/octet-stream',
          'ETag': object.httpEtag,
          'Cache-Control': 'public, max-age=86400'
        }
      });
    }
    
    return new Response('Method Not Allowed', { status: 405 });
  }
};
```

### D1 Database Integration

```typescript
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/users') {
      // Query with parameters
      const results = await env.DB.prepare(
        'SELECT * FROM users WHERE active = ? ORDER BY created_at DESC LIMIT ?'
      )
      .bind(1, 10)
      .all();
      
      return Response.json(results.results);
    }
    
    if (url.pathname === '/api/users' && request.method === 'POST') {
      const { name, email } = await request.json<{ name: string; email: string }>();
      
      // Insert with transaction
      const result = await env.DB.prepare(
        'INSERT INTO users (name, email, active) VALUES (?, ?, ?)'
      )
      .bind(name, email, 1)
      .run();
      
      return Response.json({
        success: result.success,
        id: result.meta.last_row_id
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Durable Objects

```typescript
// worker.ts
interface Env {
  COUNTER: DurableObjectNamespace;
}

export class Counter {
  state: DurableObjectState;
  value: number;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.value = 0;
  }

  async fetch(request: Request): Promise<Response> {
    // Initialize from storage
    const stored = await this.state.storage.get<number>('value');
    this.value = stored || 0;

    const url = new URL(request.url);
    
    if (url.pathname === '/increment') {
      this.value++;
      await this.state.storage.put('value', this.value);
    }

    return Response.json({ value: this.value });
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Get Durable Object instance
    const id = env.COUNTER.idFromName('global-counter');
    const stub = env.COUNTER.get(id);
    
    // Forward request to Durable Object
    return stub.fetch(request);
  }
};
```

### Scheduled Events (Cron Triggers)

```typescript
interface Env {
  DB: D1Database;
}

export default {
  // HTTP handler
  async fetch(request: Request): Promise<Response> {
    return new Response('Worker running');
  },
  
  // Cron handler
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    // Run cleanup job
    ctx.waitUntil(cleanupOldRecords(env.DB));
  }
};

async function cleanupOldRecords(db: D1Database): Promise<void> {
  const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
  
  await db.prepare(
    'DELETE FROM sessions WHERE created_at < ?'
  )
  .bind(thirtyDaysAgo)
  .run();
  
  console.log('Cleanup completed');
}
```

### Environment Variables & Secrets

```typescript
interface Env {
  // Environment variables
  ENVIRONMENT: string;
  API_URL: string;
  
  // Secrets (encrypted)
  API_KEY: string;
  DATABASE_URL: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Access environment variables
    const apiUrl = env.API_URL;
    
    // Use secrets securely
    const response = await fetch(apiUrl, {
      headers: {
        'Authorization': `Bearer ${env.API_KEY}`
      }
    });
    
    const data = await response.json();
    
    return Response.json({
      environment: env.ENVIRONMENT,
      data: data
    });
  }
};
```

## Common Use Cases

### JWT Authentication

```typescript
import { SignJWT, jwtVerify } from 'jose';

interface Env {
  JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Login endpoint
    if (url.pathname === '/login' && request.method === 'POST') {
      const { username, password } = await request.json<{ username: string; password: string }>();
      
      // Verify credentials (example)
      if (username === 'demo' && password === 'secret') {
        const secret = new TextEncoder().encode(env.JWT_SECRET);
        
        const token = await new SignJWT({ sub: username, role: 'user' })
          .setProtectedHeader({ alg: 'HS256' })
          .setIssuedAt()
          .setExpirationTime('24h')
          .sign(secret);
        
        return Response.json({ token });
      }
      
      return new Response('Unauthorized', { status: 401 });
    }
    
    // Protected endpoint
    if (url.pathname === '/protected') {
      const authHeader = request.headers.get('Authorization');
      
      if (!authHeader?.startsWith('Bearer ')) {
        return new Response('Missing token', { status: 401 });
      }
      
      const token = authHeader.substring(7);
      
      try {
        const secret = new TextEncoder().encode(env.JWT_SECRET);
        const { payload } = await jwtVerify(token, secret);
        
        return Response.json({
          message: 'Access granted',
          user: payload.sub
        });
      } catch (err) {
        return new Response('Invalid token', { status: 401 });
      }
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### API Proxy with Caching

```typescript
interface Env {
  CACHE: KVNamespace;
  ORIGIN_API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const cacheKey = `api:${url.pathname}${url.search}`;
    
    // Check cache
    const cached = await env.CACHE.get(cacheKey, 'json');
    if (cached) {
      return Response.json(cached, {
        headers: { 'X-Cache': 'HIT' }
      });
    }
    
    // Fetch from origin
    const originUrl = `https://api.example.com${url.pathname}${url.search}`;
    const response = await fetch(originUrl, {
      headers: {
        'Authorization': `Bearer ${env.ORIGIN_API_KEY}`,
        'User-Agent': 'CloudflareWorker/1.0'
      }
    });
    
    if (!response.ok) {
      return new Response(response.statusText, { status: response.status });
    }
    
    const data = await response.json();
    
    // Store in cache asynchronously
    ctx.waitUntil(
      env.CACHE.put(cacheKey, JSON.stringify(data), {
        expirationTtl: 300 // 5 minutes
      })
    );
    
    return Response.json(data, {
      headers: { 'X-Cache': 'MISS' }
    });
  }
};
```

### Rate Limiting

```typescript
interface Env {
  RATE_LIMITER: DurableObjectNamespace;
}

export class RateLimiter {
  state: DurableObjectState;

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    const { limit, window } = await request.json<{ limit: number; window: number }>();
    
    const now = Date.now();
    const windowStart = now - (window * 1000);
    
    // Get requests in current window
    const requests = await this.state.storage.list<number>({
      start: windowStart.toString()
    });
    
    const count = requests.size;
    
    if (count >= limit) {
      return Response.json({ allowed: false, remaining: 0 });
    }
    
    // Record this request
    await this.state.storage.put(now.toString(), now);
    
    // Cleanup old entries
    await this.state.storage.deleteAll({
      end: windowStart.toString()
    });
    
    return Response.json({
      allowed: true,
      remaining: limit - count - 1
    });
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    const id = env.RATE_LIMITER.idFromName(clientIP);
    const limiter = env.RATE_LIMITER.get(id);
    
    // Check rate limit: 100 requests per 60 seconds
    const result = await limiter.fetch('https://fake-host', {
      method: 'POST',
      body: JSON.stringify({ limit: 100, window: 60 })
    }).then(r => r.json<{ allowed: boolean; remaining: number }>());
    
    if (!result.allowed) {
      return new Response('Rate limit exceeded', {
        status: 429,
        headers: {
          'X-RateLimit-Remaining': '0',
          'Retry-After': '60'
        }
      });
    }
    
    // Process request
    return Response.json({
      message: 'Success',
      rateLimitRemaining: result.remaining
    });
  }
};
```

## Integration

### wrangler.toml Configuration

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Account ID
account_id = "your-account-id"

# Workers AI
[ai]
binding = "AI"

# KV Namespaces
[[kv_namespaces]]
binding = "CACHE"
id = "your-kv-namespace-id"

# R2 Buckets
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

# D1 Databases
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"

# Durable Objects
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "my-worker"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]

# Environment Variables
[vars]
ENVIRONMENT = "production"
API_URL = "https://api.example.com"

# Cron Triggers
[triggers]
crons = ["0 0 * * *"]  # Daily at midnight

# Custom Domains
routes = [
  { pattern = "api.example.com/*", custom_domain = true }
]
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "lib": ["ES2020"],
    "types": ["@cloudflare/workers-types"],
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

## Best Practices

1. **Use TypeScript**: Type safety prevents runtime errors
2. **Minimize bundle size**: Workers have a 1MB limit after compression
3. **Use bindings**: Don't hardcode credentials; use environment variables
4. **Cache strategically**: Use Cache API and KV for frequently accessed data
5. **Handle errors gracefully**: Always return valid Response objects
6. **Use waitUntil()**: For async operations that shouldn't block response
7. **Monitor performance**: Use Wrangler tail and analytics dashboard
8. **Version your workers**: Use Wrangler deployments for rollback capability
9. **Test locally**: Use `wrangler dev` with --local flag
10. **Optimize cold starts**: Keep dependencies minimal

## Troubleshooting

### Worker not deploying

```bash
# Check authentication
wrangler whoami

# Verify wrangler.toml syntax
wrangler deploy --dry-run

# Check account ID
wrangler deploy --account-id=your-account-id
```

### Binding errors

```typescript
// Always type your Env interface
interface Env {
  MY_KV: KVNamespace;  // Not 'any'
}

// Check binding exists in wrangler.toml
[[kv_namespaces]]
binding = "MY_KV"
id = "namespace-id"
```

### Memory limit exceeded

```typescript
// Stream large responses instead of buffering
async function streamLargeFile(bucket: R2Bucket, key: string): Promise<Response> {
  const object = await bucket.get(key);
  
  if (!object) {
    return new Response('Not Found', { status: 404 });
  }
  
  // Stream the body directly
  return new Response(object.body);
}
```

### CPU time limit

```typescript
// Use waitUntil for background tasks
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Return response immediately
    const response = Response.json({ status: 'processing' });
    
    // Continue processing in background
    ctx.waitUntil(performHeavyTask(env));
    
    return response;
  }
};
```

## See Also

- [Cloudflare Pages](cloudflare-pages.md) - JAMstack hosting platform
- [Cloudflare KV](cloudflare-kv.md) - Key-value storage for Workers
- [Cloudflare R2](cloudflare-r2.md) - Object storage for Workers
- [Cloudflare D1](cloudflare-d1.md) - Serverless SQL database
- **Workers AI**: https://developers.cloudflare.com/workers-ai/
- **Queues**: https://developers.cloudflare.com/queues/
- **Streams**: https://developers.cloudflare.com/stream/
