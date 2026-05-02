---
name: Cloudflare KV
description: |
  Use Cloudflare Workers KV for globally distributed key-value storage.
  Trigger phrases: "cloudflare kv", "workers kv", "kv namespace", "edge kv",
  "key value cloudflare", "kv storage", "distributed kv", "workers key value"
license: MIT
---

# Cloudflare Workers KV

Cloudflare Workers KV is a globally distributed, eventually consistent, key-value data store accessible from Cloudflare Workers. Optimized for high-read, low-write workloads with sub-50ms global reads.

## When to Use

**Best for:**
- **Configuration data**: Feature flags, API keys, settings
- **Session storage**: User sessions and JWT tokens
- **Caching**: API responses, computed results
- **Content delivery**: HTML fragments, JSON data
- **Static data**: Country codes, translations, product catalogs
- **Rate limiting**: Request counters with TTL
- **A/B testing**: Experiment configurations
- **CDN edge caching**: Pre-computed pages, assets

**Not ideal for:**
- Frequently changing data (eventual consistency)
- Large binary files >25MB (use R2 instead)
- Relational data with complex queries (use D1)
- Real-time updates requiring strong consistency
- High-frequency writes (>1 write/second per key)

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/kv/
- **Get Started**: https://developers.cloudflare.com/kv/get-started/
- **API Reference**: https://developers.cloudflare.com/kv/api/
- **Workers API**: https://developers.cloudflare.com/kv/api/
- **Best Practices**: https://developers.cloudflare.com/kv/best-practices/
- **Limits**: https://developers.cloudflare.com/kv/platform/limits/
- **Pricing**: https://developers.cloudflare.com/kv/platform/pricing/

## Quick Start

### 1. Create KV Namespace

```bash
# Create KV namespace
wrangler kv:namespace create MY_KV

# Output includes namespace ID - copy it!
# ✅ Created namespace with id "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Add the following to your wrangler.toml:
# [[kv_namespaces]]
# binding = "MY_KV"
# id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Create preview namespace for development
wrangler kv:namespace create MY_KV --preview

# List all namespaces
wrangler kv:namespace list
```

### 2. Configure wrangler.toml

```toml
name = "kv-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "MY_KV"
id = "production-namespace-id"
preview_id = "preview-namespace-id"

[[kv_namespaces]]
binding = "CACHE"
id = "cache-namespace-id"
```

### 3. Basic Worker Example

```typescript
// src/index.ts
interface Env {
  MY_KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1) || 'default';
    
    // GET: Read from KV
    if (request.method === 'GET') {
      const value = await env.MY_KV.get(key);
      
      if (value === null) {
        return new Response('Key not found', { status: 404 });
      }
      
      return new Response(value);
    }
    
    // PUT: Write to KV
    if (request.method === 'PUT') {
      const value = await request.text();
      await env.MY_KV.put(key, value);
      
      return Response.json({ success: true, key });
    }
    
    // DELETE: Remove from KV
    if (request.method === 'DELETE') {
      await env.MY_KV.delete(key);
      return Response.json({ success: true });
    }
    
    return new Response('Method Not Allowed', { status: 405 });
  }
};
```

### 4. CLI Operations

```bash
# Put a key-value pair
wrangler kv:key put --namespace-id=xxx "my-key" "my-value"

# Put with metadata
wrangler kv:key put --namespace-id=xxx "my-key" "my-value" --metadata='{"created": "2024-01-01"}'

# Put with TTL (expires in 1 hour)
wrangler kv:key put --namespace-id=xxx "my-key" "my-value" --expiration-ttl=3600

# Get a value
wrangler kv:key get --namespace-id=xxx "my-key"

# Get with metadata
wrangler kv:key get --namespace-id=xxx "my-key" --preview

# Delete a key
wrangler kv:key delete --namespace-id=xxx "my-key"

# List keys
wrangler kv:key list --namespace-id=xxx

# Bulk upload from JSON file
wrangler kv:bulk put --namespace-id=xxx ./data.json
```

## Core Features

### Basic Operations

```typescript
interface Env {
  KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // PUT: Store text
    await env.KV.put('greeting', 'Hello, World!');
    
    // PUT: Store JSON
    await env.KV.put('user:1', JSON.stringify({
      id: 1,
      name: 'Alice',
      email: 'alice@example.com'
    }));
    
    // PUT: With expiration (1 hour TTL)
    await env.KV.put('session:abc123', 'session-data', {
      expirationTtl: 3600
    });
    
    // PUT: With absolute expiration time
    const tomorrow = Math.floor(Date.now() / 1000) + 86400;
    await env.KV.put('temp-token', 'token-value', {
      expiration: tomorrow
    });
    
    // PUT: With metadata
    await env.KV.put('image:logo', 'base64-data', {
      metadata: {
        width: 200,
        height: 100,
        format: 'png'
      }
    });
    
    // GET: Retrieve text
    const greeting = await env.KV.get('greeting');
    // 'Hello, World!'
    
    // GET: Retrieve JSON
    const userData = await env.KV.get('user:1', 'json');
    // { id: 1, name: 'Alice', email: 'alice@example.com' }
    
    // GET: With metadata
    const { value, metadata } = await env.KV.getWithMetadata('image:logo', 'text');
    // value: 'base64-data'
    // metadata: { width: 200, height: 100, format: 'png' }
    
    // DELETE: Remove key
    await env.KV.delete('temp-token');
    
    return Response.json({ success: true });
  }
};
```

### Value Types

```typescript
interface Env {
  KV: KVNamespace;
}

interface UserMetadata {
  uploadedAt: string;
  contentType: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Text (default)
    const text = await env.KV.get('key', 'text');
    // Returns: string | null
    
    // JSON (automatically parsed)
    const json = await env.KV.get('user:1', 'json');
    // Returns: any | null
    
    // ArrayBuffer (binary data)
    const buffer = await env.KV.get('file', 'arrayBuffer');
    // Returns: ArrayBuffer | null
    
    // Stream (for large values)
    const stream = await env.KV.get('large-file', 'stream');
    // Returns: ReadableStream | null
    
    if (stream) {
      return new Response(stream, {
        headers: { 'Content-Type': 'application/octet-stream' }
      });
    }
    
    // Type-safe metadata
    const { value, metadata } = await env.KV.getWithMetadata<UserMetadata>('file:image.png');
    if (metadata) {
      console.log(metadata.contentType); // Type-safe access
    }
    
    return new Response('OK');
  }
};
```

### Listing Keys

```typescript
interface Env {
  KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // List all keys (up to 1000)
    const list1 = await env.KV.list();
    // {
    //   keys: [{ name: 'key1' }, { name: 'key2' }],
    //   list_complete: true,
    //   cursor: ''
    // }
    
    // List with prefix
    const list2 = await env.KV.list({ prefix: 'user:' });
    // Lists: user:1, user:2, user:3, etc.
    
    // List with limit
    const list3 = await env.KV.list({ limit: 10 });
    
    // Paginated listing
    const cursor = url.searchParams.get('cursor') || undefined;
    const list = await env.KV.list({
      prefix: 'user:',
      limit: 100,
      cursor: cursor
    });
    
    return Response.json({
      keys: list.keys,
      hasMore: !list.list_complete,
      nextCursor: list.cursor
    });
  }
};
```

### Caching Pattern

```typescript
interface Env {
  CACHE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const cacheKey = `api:${url.pathname}`;
    
    // Try KV cache first
    const cached = await env.CACHE.get(cacheKey, 'json');
    
    if (cached) {
      return Response.json(cached, {
        headers: { 'X-Cache': 'HIT' }
      });
    }
    
    // Fetch from origin
    const data = await fetchFromAPI(url.pathname);
    
    // Store in KV with 5 minute TTL
    ctx.waitUntil(
      env.CACHE.put(cacheKey, JSON.stringify(data), {
        expirationTtl: 300
      })
    );
    
    return Response.json(data, {
      headers: { 'X-Cache': 'MISS' }
    });
  }
};

async function fetchFromAPI(path: string): Promise<any> {
  const response = await fetch(`https://api.example.com${path}`);
  return response.json();
}
```

## Common Use Cases

### Session Management

```typescript
import { SignJWT, jwtVerify } from 'jose';

interface Env {
  SESSIONS: KVNamespace;
  JWT_SECRET: string;
}

interface Session {
  userId: string;
  email: string;
  createdAt: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Create session
    if (url.pathname === '/login' && request.method === 'POST') {
      const { email, password } = await request.json<{
        email: string;
        password: string;
      }>();
      
      // Verify credentials (simplified)
      if (email === 'user@example.com' && password === 'secret') {
        const sessionId = crypto.randomUUID();
        const session: Session = {
          userId: '123',
          email: email,
          createdAt: new Date().toISOString()
        };
        
        // Store session in KV (expires in 24 hours)
        await env.SESSIONS.put(
          `session:${sessionId}`,
          JSON.stringify(session),
          { expirationTtl: 86400 }
        );
        
        // Create JWT token
        const secret = new TextEncoder().encode(env.JWT_SECRET);
        const token = await new SignJWT({ sessionId })
          .setProtectedHeader({ alg: 'HS256' })
          .setExpirationTime('24h')
          .sign(secret);
        
        return Response.json({ token });
      }
      
      return new Response('Invalid credentials', { status: 401 });
    }
    
    // Validate session
    if (url.pathname === '/me') {
      const authHeader = request.headers.get('Authorization');
      
      if (!authHeader?.startsWith('Bearer ')) {
        return new Response('Unauthorized', { status: 401 });
      }
      
      const token = authHeader.substring(7);
      
      try {
        const secret = new TextEncoder().encode(env.JWT_SECRET);
        const { payload } = await jwtVerify(token, secret);
        const sessionId = payload.sessionId as string;
        
        // Get session from KV
        const session = await env.SESSIONS.get<Session>(
          `session:${sessionId}`,
          'json'
        );
        
        if (!session) {
          return new Response('Session expired', { status: 401 });
        }
        
        return Response.json({ user: session });
      } catch (err) {
        return new Response('Invalid token', { status: 401 });
      }
    }
    
    // Logout
    if (url.pathname === '/logout' && request.method === 'POST') {
      const authHeader = request.headers.get('Authorization');
      
      if (authHeader?.startsWith('Bearer ')) {
        const token = authHeader.substring(7);
        const secret = new TextEncoder().encode(env.JWT_SECRET);
        
        try {
          const { payload } = await jwtVerify(token, secret);
          const sessionId = payload.sessionId as string;
          
          // Delete session from KV
          await env.SESSIONS.delete(`session:${sessionId}`);
        } catch (err) {
          // Token invalid, ignore
        }
      }
      
      return Response.json({ success: true });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Feature Flags

```typescript
interface Env {
  FLAGS: KVNamespace;
}

interface FeatureFlag {
  enabled: boolean;
  rolloutPercentage: number;
  allowedUsers?: string[];
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Check if feature is enabled
    const userId = request.headers.get('X-User-ID') || 'anonymous';
    const featureName = 'new-dashboard';
    
    const isEnabled = await checkFeatureFlag(
      env.FLAGS,
      featureName,
      userId
    );
    
    if (isEnabled) {
      return Response.json({ feature: 'new-dashboard', enabled: true });
    } else {
      return Response.json({ feature: 'old-dashboard', enabled: false });
    }
  }
};

async function checkFeatureFlag(
  kv: KVNamespace,
  flagName: string,
  userId: string
): Promise<boolean> {
  const flag = await kv.get<FeatureFlag>(`flag:${flagName}`, 'json');
  
  if (!flag || !flag.enabled) {
    return false;
  }
  
  // Check if user is in allowed list
  if (flag.allowedUsers && flag.allowedUsers.includes(userId)) {
    return true;
  }
  
  // Check rollout percentage
  const hash = await hashString(userId + flagName);
  const percentage = (hash % 100) + 1;
  
  return percentage <= flag.rolloutPercentage;
}

async function hashString(str: string): Promise<number> {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.reduce((acc, byte) => acc + byte, 0);
}
```

### Rate Limiting

```typescript
interface Env {
  RATE_LIMIT: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    const rateLimitKey = `ratelimit:${clientIP}`;
    
    // Get current request count
    const currentCount = await env.RATE_LIMIT.get(rateLimitKey);
    const count = currentCount ? parseInt(currentCount) : 0;
    
    // Limit: 100 requests per minute
    const limit = 100;
    
    if (count >= limit) {
      return new Response('Rate limit exceeded', {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': '0',
          'Retry-After': '60'
        }
      });
    }
    
    // Increment counter with 60 second TTL
    await env.RATE_LIMIT.put(rateLimitKey, (count + 1).toString(), {
      expirationTtl: 60
    });
    
    return Response.json({
      success: true,
      rateLimit: {
        limit,
        remaining: limit - count - 1
      }
    });
  }
};
```

### Configuration Management

```typescript
interface Env {
  CONFIG: KVNamespace;
}

interface AppConfig {
  apiUrl: string;
  features: Record<string, boolean>;
  limits: {
    maxUploadSize: number;
    maxRequests: number;
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Load configuration
    const config = await env.CONFIG.get<AppConfig>('app-config', 'json');
    
    if (!config) {
      return Response.json(
        { error: 'Configuration not found' },
        { status: 500 }
      );
    }
    
    // Use configuration
    const apiUrl = config.apiUrl;
    const maxUploadSize = config.limits.maxUploadSize;
    
    return Response.json({
      message: 'Using configuration',
      apiUrl,
      maxUploadSize
    });
  }
};
```

### HTML Fragment Caching

```typescript
interface Env {
  HTML_CACHE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const cacheKey = `html:${url.pathname}`;
    
    // Try to get cached HTML
    const cached = await env.HTML_CACHE.get(cacheKey);
    
    if (cached) {
      return new Response(cached, {
        headers: {
          'Content-Type': 'text/html',
          'X-Cache': 'HIT'
        }
      });
    }
    
    // Generate HTML
    const html = await generateHTML(url.pathname);
    
    // Cache for 1 hour
    ctx.waitUntil(
      env.HTML_CACHE.put(cacheKey, html, {
        expirationTtl: 3600,
        metadata: {
          generatedAt: new Date().toISOString(),
          path: url.pathname
        }
      })
    );
    
    return new Response(html, {
      headers: {
        'Content-Type': 'text/html',
        'X-Cache': 'MISS'
      }
    });
  }
};

async function generateHTML(path: string): Promise<string> {
  return `
    <!DOCTYPE html>
    <html>
      <head><title>Page ${path}</title></head>
      <body>
        <h1>Generated at ${new Date().toISOString()}</h1>
        <p>Path: ${path}</p>
      </body>
    </html>
  `;
}
```

## Integration

### Bulk Upload

```json
[
  {
    "key": "config:apiUrl",
    "value": "https://api.example.com"
  },
  {
    "key": "config:maxUploadSize",
    "value": "10485760"
  },
  {
    "key": "flag:newFeature",
    "value": "{\"enabled\": true, \"rollout\": 50}",
    "metadata": {
      "type": "feature-flag"
    }
  }
]
```

```bash
# Upload from JSON file
wrangler kv:bulk put --namespace-id=xxx ./config.json

# Upload with preview namespace
wrangler kv:bulk put --namespace-id=xxx --preview ./config.json
```

### Multiple Namespaces

```toml
# wrangler.toml
[[kv_namespaces]]
binding = "SESSIONS"
id = "sessions-namespace-id"

[[kv_namespaces]]
binding = "CACHE"
id = "cache-namespace-id"

[[kv_namespaces]]
binding = "CONFIG"
id = "config-namespace-id"
```

```typescript
interface Env {
  SESSIONS: KVNamespace;
  CACHE: KVNamespace;
  CONFIG: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Use different namespaces for different purposes
    await env.SESSIONS.put('session:123', 'data');
    await env.CACHE.put('api:/users', 'cached-response');
    await env.CONFIG.put('feature:new-ui', 'true');
    
    return new Response('OK');
  }
};
```

## Best Practices

1. **Use prefixes**: Organize keys with prefixes (e.g., `user:123`, `cache:api:/users`)
2. **Set TTLs**: Always expire temporary data to avoid unnecessary storage costs
3. **Eventual consistency**: Design for eventual consistency; don't expect immediate reads after writes
4. **Small values**: Keep values under 25MB; use R2 for larger files
5. **Batch operations**: Use `ctx.waitUntil()` for non-critical writes
6. **Metadata**: Store useful metadata for debugging and management
7. **Namespaces**: Use separate namespaces for different data types
8. **Cache invalidation**: Implement cache invalidation strategies
9. **Monitor usage**: Track read/write operations and storage costs
10. **Error handling**: Always handle null returns from `.get()`

## Troubleshooting

### Values not updating immediately

```typescript
// KV is eventually consistent
// Writes may take up to 60 seconds to propagate globally

// ❌ Don't expect immediate consistency
await env.KV.put('counter', '1');
const value = await env.KV.get('counter'); // May still be old value

// ✅ Design for eventual consistency
// Store critical data in Durable Objects or D1 for strong consistency
```

### Binding errors

```typescript
// Ensure binding name matches wrangler.toml
interface Env {
  MY_KV: KVNamespace;  // Must match binding = "MY_KV"
}

// Verify namespace exists
// wrangler kv:namespace list
```

### Large value errors

```typescript
// KV has 25MB limit per value
// For larger data, split or use R2

// ❌ Don't store large files in KV
await env.KV.put('video', largeVideoBuffer); // May fail

// ✅ Use R2 for large files
await env.BUCKET.put('video.mp4', videoStream);
```

### TTL not working

```typescript
// Ensure expirationTtl is in seconds
await env.KV.put('key', 'value', {
  expirationTtl: 3600  // ✅ 1 hour in seconds
});

// Not milliseconds!
await env.KV.put('key', 'value', {
  expirationTtl: 3600000  // ❌ Wrong - this is ~42 days
});
```

## See Also

- [Cloudflare Workers](cloudflare-workers.md) - Runtime for KV access
- [Cloudflare D1](cloudflare-d1.md) - SQL database for complex queries
- [Cloudflare R2](cloudflare-r2.md) - Object storage for large files
- [Cloudflare Pages](cloudflare-pages.md) - Static sites with KV backend
- **Durable Objects**: https://developers.cloudflare.com/durable-objects/
