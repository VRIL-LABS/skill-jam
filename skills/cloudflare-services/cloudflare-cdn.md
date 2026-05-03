---
name: Cloudflare CDN
description: >
  Manages Cloudflare's global Content Delivery Network for cache control, content optimization, edge caching, purging, and performance improvements.
  Invoke when asked to configure CDN, optimize content delivery, implement cache rules, purge cache, improve page load times, set cache headers, configure edge caching, or optimize static assets with Cloudflare.
license: MIT
---

# Cloudflare CDN

Cloudflare's global Content Delivery Network (CDN) serves content from 300+ data centers worldwide, reducing latency and improving performance. The CDN automatically caches static content and provides advanced cache control, purging, and optimization features to accelerate websites and applications.

## When to Use

Use Cloudflare CDN when you need:

- **Global Content Delivery**: Serve content from edge locations near users
- **Static Asset Caching**: Cache images, CSS, JavaScript, fonts, and other static files
- **Dynamic Content Acceleration**: Optimize delivery of API responses and HTML
- **Cache Control**: Fine-grained control over what gets cached and for how long
- **Origin Shield**: Reduce load on origin servers with additional caching layer
- **Bandwidth Savings**: Reduce origin bandwidth usage by serving from cache
- **Performance Optimization**: Minimize latency with edge caching
- **Cache Purging**: Instant cache invalidation when content updates

**Don't use** for content requiring user authentication without proper cache rules, highly personalized content that shouldn't be cached, or real-time data that changes constantly.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/cache/
- **Cache Rules**: https://developers.cloudflare.com/cache/how-to/cache-rules/
- **Cache Keys**: https://developers.cloudflare.com/cache/how-to/cache-keys/
- **Purge Cache**: https://developers.cloudflare.com/cache/how-to/purge-cache/
- **Cache by Device Type**: https://developers.cloudflare.com/cache/how-to/cache-by-device-type/
- **Cache Analytics**: https://developers.cloudflare.com/cache/cache-analytics/
- **Best Practices**: https://developers.cloudflare.com/cache/best-practices/
- **API Reference**: https://developers.cloudflare.com/api/operations/zone-purge
- **Tiered Cache**: https://developers.cloudflare.com/cache/how-to/tiered-cache/
- **Polish**: https://developers.cloudflare.com/images/polish/

## Quick Start

### Step 1: Enable Cloudflare CDN

```bash
# CDN is enabled by default when you proxy traffic through Cloudflare
# Ensure DNS records are proxied (orange cloud icon in dashboard)

# Verify DNS is proxied
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"
```

### Step 2: Configure Cache Rules (Dashboard)

1. Log in to Cloudflare Dashboard
2. Select your domain
3. Go to **Caching** > **Cache Rules**
4. Click **Create Rule**
5. Set conditions and cache behavior
6. Save and deploy

### Step 3: Set Cache Headers in Your Application

```javascript
// Example: Express.js
app.use('/static', express.static('public', {
  maxAge: '1y',
  etag: true,
  lastModified: true,
  setHeaders: (res, path) => {
    if (path.endsWith('.html')) {
      res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=7200');
    } else if (path.match(/\.(jpg|png|gif|css|js)$/)) {
      res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    }
  }
}));

// Example: Node.js HTTP server
const http = require('http');
http.createServer((req, res) => {
  if (req.url.endsWith('.css') || req.url.endsWith('.js')) {
    res.setHeader('Cache-Control', 'public, max-age=31536000');
  }
  // ... serve content
}).listen(3000);
```

### Step 4: Test Cache Status

```bash
# Check if content is cached
curl -I https://example.com/style.css | grep -i cf-cache-status

# Possible values:
# HIT - Served from Cloudflare cache
# MISS - Not in cache, fetched from origin
# EXPIRED - Cached but expired, revalidating
# BYPASS - Cache intentionally bypassed
# DYNAMIC - Not cacheable (dynamic content)
```

## Core Features

### 1. Cache Rules

Create custom caching behavior with Cache Rules:

```javascript
// Using Workers for custom cache control
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Custom cache key
    const cacheKey = new Request(url.toString(), request);
    const cache = caches.default;

    // Check cache first
    let response = await cache.match(cacheKey);
    if (response) {
      console.log('Cache HIT');
      return response;
    }

    console.log('Cache MISS');
    
    // Fetch from origin
    response = await fetch(request);

    // Clone response for caching
    const cacheResponse = response.clone();

    // Cache based on content type
    const contentType = response.headers.get('Content-Type') || '';
    
    if (contentType.includes('image') || 
        contentType.includes('css') || 
        contentType.includes('javascript')) {
      
      // Set cache headers
      const headers = new Headers(cacheResponse.headers);
      headers.set('Cache-Control', 'public, max-age=86400');
      
      const cachedResponse = new Response(cacheResponse.body, {
        status: cacheResponse.status,
        statusText: cacheResponse.statusText,
        headers,
      });

      // Store in cache
      ctx.waitUntil(cache.put(cacheKey, cachedResponse));
    }

    return response;
  }
};
```

### 2. Cache Everything with Page Rules

```bash
# Via API: Create a Page Rule to cache everything
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [
      {
        "target": "url",
        "constraint": {
          "operator": "matches",
          "value": "*.example.com/api/*"
        }
      }
    ],
    "actions": [
      {
        "id": "cache_level",
        "value": "cache_everything"
      },
      {
        "id": "edge_cache_ttl",
        "value": 7200
      }
    ],
    "priority": 1,
    "status": "active"
  }'
```

### 3. Custom Cache Keys

Normalize cache keys for better hit rates:

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // Remove query parameters for cache key
    const cacheUrl = new URL(url.pathname, url.origin);
    
    // Or include specific query parameters only
    const allowedParams = ['version', 'lang'];
    for (const [key, value] of url.searchParams) {
      if (allowedParams.includes(key)) {
        cacheUrl.searchParams.set(key, value);
      }
    }

    const cacheKey = new Request(cacheUrl.toString(), {
      method: 'GET',
      headers: request.headers,
    });

    // Use custom cache key
    const cache = caches.default;
    let response = await cache.match(cacheKey);
    
    if (!response) {
      response = await fetch(request);
      const cacheResponse = response.clone();
      await cache.put(cacheKey, cacheResponse);
    }

    return response;
  }
};
```

### 4. Cache Purging

Clear cached content when it updates:

```bash
# Purge everything (use sparingly)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'

# Purge specific files
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "files": [
      "https://example.com/style.css",
      "https://example.com/script.js"
    ]
  }'

# Purge by prefix
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "prefixes": [
      "https://example.com/images/",
      "https://example.com/api/v2/"
    ]
  }'

# Purge by tag (enterprise only)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "tags": ["product-123", "category-tech"]
  }'

# Purge by hostname
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "hosts": ["www.example.com", "api.example.com"]
  }'
```

### 5. Browser Cache TTL

Control how long browsers cache content:

```javascript
export default {
  async fetch(request) {
    const response = await fetch(request);
    
    // Modify cache headers
    const newHeaders = new Headers(response.headers);
    
    // Set edge cache TTL (Cloudflare)
    newHeaders.set('CDN-Cache-Control', 'public, max-age=86400');
    
    // Set browser cache TTL
    newHeaders.set('Cache-Control', 'public, max-age=3600');
    
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders,
    });
  }
};
```

## Common Use Cases

### Static Website Optimization

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const cache = caches.default;

    // Define cache settings by file type
    const cacheSettings = {
      images: { ttl: 31536000, extensions: ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'] },
      fonts: { ttl: 31536000, extensions: ['.woff', '.woff2', '.ttf', '.eot'] },
      styles: { ttl: 86400, extensions: ['.css'] },
      scripts: { ttl: 86400, extensions: ['.js'] },
      html: { ttl: 3600, extensions: ['.html'] },
    };

    // Determine file type
    let cacheTTL = 0;
    for (const [type, config] of Object.entries(cacheSettings)) {
      if (config.extensions.some(ext => url.pathname.endsWith(ext))) {
        cacheTTL = config.ttl;
        break;
      }
    }

    if (cacheTTL > 0) {
      // Check cache
      let response = await cache.match(request);
      
      if (!response) {
        // Fetch from origin
        response = await fetch(request);
        
        // Cache if successful
        if (response.ok) {
          const headers = new Headers(response.headers);
          headers.set('Cache-Control', `public, max-age=${cacheTTL}`);
          
          const cachedResponse = new Response(response.body, {
            status: response.status,
            headers,
          });
          
          ctx.waitUntil(cache.put(request, cachedResponse.clone()));
          return cachedResponse;
        }
      }
      
      return response;
    }

    // No cache for other files
    return fetch(request);
  }
};
```

### API Response Caching

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Only cache GET requests
    if (request.method !== 'GET') {
      return fetch(request);
    }

    // Cache API responses
    if (url.pathname.startsWith('/api/')) {
      const cache = caches.default;
      
      // Create cache key (exclude certain query params)
      const cacheUrl = new URL(url);
      cacheUrl.searchParams.delete('_'); // Remove cache busters
      cacheUrl.searchParams.delete('timestamp');
      
      const cacheKey = new Request(cacheUrl.toString(), {
        method: 'GET',
      });

      // Check cache
      let response = await cache.match(cacheKey);
      
      if (response) {
        // Add custom header to indicate cache hit
        const headers = new Headers(response.headers);
        headers.set('X-Cache-Status', 'HIT');
        return new Response(response.body, {
          status: response.status,
          headers,
        });
      }

      // Fetch from origin
      response = await fetch(request);

      // Only cache successful responses
      if (response.ok) {
        const headers = new Headers(response.headers);
        headers.set('Cache-Control', 'public, max-age=300, s-maxage=600');
        headers.set('X-Cache-Status', 'MISS');
        
        const cachedResponse = new Response(response.body, {
          status: response.status,
          headers,
        });

        ctx.waitUntil(cache.put(cacheKey, cachedResponse.clone()));
        return cachedResponse;
      }

      return response;
    }

    return fetch(request);
  }
};
```

### Conditional Caching with Cookies

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const cookie = request.headers.get('Cookie') || '';
    
    // Don't cache if user is logged in
    if (cookie.includes('session=')) {
      const response = await fetch(request);
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'private, no-cache');
      return new Response(response.body, {
        status: response.status,
        headers,
      });
    }

    // Cache for anonymous users
    const cache = caches.default;
    let response = await cache.match(request);
    
    if (!response) {
      response = await fetch(request);
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=3600');
      
      const cachedResponse = new Response(response.body, {
        status: response.status,
        headers,
      });
      
      await cache.put(request, cachedResponse.clone());
      return cachedResponse;
    }

    return response;
  }
};
```

### Cache Warming

```javascript
// Proactively populate cache with important content
async function warmCache(urls, env) {
  const cache = caches.default;
  
  for (const url of urls) {
    try {
      const request = new Request(url);
      const response = await fetch(request);
      
      if (response.ok) {
        await cache.put(request, response.clone());
        console.log(`Cached: ${url}`);
      }
    } catch (err) {
      console.error(`Failed to cache ${url}:`, err);
    }
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Trigger cache warming
    if (url.pathname === '/admin/warm-cache') {
      const criticalUrls = [
        'https://example.com/',
        'https://example.com/popular-page',
        'https://example.com/api/config',
      ];
      
      ctx.waitUntil(warmCache(criticalUrls, env));
      return new Response('Cache warming started');
    }

    return fetch(request);
  }
};
```

### Device-Type Specific Caching

```javascript
export default {
  async fetch(request) {
    const userAgent = request.headers.get('User-Agent') || '';
    
    // Detect device type
    const isMobile = /mobile|android|iphone/i.test(userAgent);
    const isTablet = /tablet|ipad/i.test(userAgent);
    
    const deviceType = isMobile ? 'mobile' : (isTablet ? 'tablet' : 'desktop');
    
    // Create device-specific cache key
    const url = new URL(request.url);
    url.searchParams.set('device', deviceType);
    
    const cacheKey = new Request(url.toString(), request);
    const cache = caches.default;

    let response = await cache.match(cacheKey);
    
    if (!response) {
      // Fetch with device hint
      const originRequest = new Request(request.url, {
        method: request.method,
        headers: new Headers(request.headers),
      });
      originRequest.headers.set('X-Device-Type', deviceType);
      
      response = await fetch(originRequest);
      
      // Cache the response
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=3600');
      headers.set('Vary', 'User-Agent');
      
      const cachedResponse = new Response(response.body, {
        status: response.status,
        headers,
      });
      
      await cache.put(cacheKey, cachedResponse.clone());
      return cachedResponse;
    }

    return response;
  }
};
```

## Integration

### With Origin Servers

```nginx
# Nginx configuration for optimal caching
server {
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(html|json|xml)$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }

    location /api/ {
        add_header Cache-Control "public, max-age=300, s-maxage=600";
    }
}
```

### With WordPress

```php
// wp-config.php or functions.php
// Set cache headers for WordPress

function set_cloudflare_cache_headers() {
    if (!is_user_logged_in()) {
        if (is_front_page() || is_home()) {
            header('Cache-Control: public, max-age=3600, s-maxage=7200');
        } elseif (is_single() || is_page()) {
            header('Cache-Control: public, max-age=7200, s-maxage=14400');
        }
    } else {
        header('Cache-Control: private, no-cache');
    }
}
add_action('send_headers', 'set_cloudflare_cache_headers');

// Purge Cloudflare cache on post update
function purge_cloudflare_on_update($post_id) {
    $zone_id = 'YOUR_ZONE_ID';
    $api_token = 'YOUR_API_TOKEN';
    $post_url = get_permalink($post_id);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://api.cloudflare.com/client/v4/zones/$zone_id/purge_cache");
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['files' => [$post_url]]));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer $api_token",
        "Content-Type: application/json"
    ]);
    curl_exec($ch);
    curl_close($ch);
}
add_action('save_post', 'purge_cloudflare_on_update');
```

### With Next.js

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=60, s-maxage=300, stale-while-revalidate',
          },
        ],
      },
    ];
  },
};
```

## Best Practices

### 1. Set Appropriate TTLs

```javascript
// Static assets: Long TTL with versioning
// /static/app.v123.js -> Cache-Control: max-age=31536000, immutable

// HTML: Short TTL for freshness
// /index.html -> Cache-Control: max-age=3600, must-revalidate

// API: Medium TTL with stale-while-revalidate
// /api/data -> Cache-Control: max-age=300, stale-while-revalidate=600

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const response = await fetch(request);
    const headers = new Headers(response.headers);

    if (url.pathname.includes('/static/') && /\.[a-f0-9]{8,}\./.test(url.pathname)) {
      headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    } else if (url.pathname.endsWith('.html')) {
      headers.set('Cache-Control', 'public, max-age=3600, must-revalidate');
    } else if (url.pathname.startsWith('/api/')) {
      headers.set('Cache-Control', 'public, max-age=300, stale-while-revalidate=600');
    }

    return new Response(response.body, {
      status: response.status,
      headers,
    });
  }
};
```

### 2. Use Cache Tags for Organized Purging

```javascript
// Add cache tags to responses (Enterprise only)
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const response = await fetch(request);
    const headers = new Headers(response.headers);

    // Tag by content type
    if (url.pathname.startsWith('/products/')) {
      const productId = url.pathname.split('/')[2];
      headers.set('Cache-Tag', `product-${productId},products,catalog`);
    }

    return new Response(response.body, {
      status: response.status,
      headers,
    });
  }
};
```

### 3. Implement Stale-While-Revalidate

```javascript
export default {
  async fetch(request, env, ctx) {
    const cache = caches.default;
    
    let response = await cache.match(request);
    const now = Date.now();

    if (response) {
      const cachedTime = response.headers.get('X-Cached-Time');
      const age = now - parseInt(cachedTime || '0');
      
      // Serve stale content while revalidating
      if (age > 300000) { // 5 minutes
        ctx.waitUntil(
          fetch(request).then(freshResponse => {
            const headers = new Headers(freshResponse.headers);
            headers.set('X-Cached-Time', now.toString());
            return cache.put(request, new Response(freshResponse.body, {
              status: freshResponse.status,
              headers,
            }));
          })
        );
      }
      
      return response;
    }

    response = await fetch(request);
    const headers = new Headers(response.headers);
    headers.set('X-Cached-Time', now.toString());
    
    const cachedResponse = new Response(response.body, {
      status: response.status,
      headers,
    });
    
    ctx.waitUntil(cache.put(request, cachedResponse.clone()));
    return cachedResponse;
  }
};
```

### 4. Respect Origin Cache Headers

```javascript
export default {
  async fetch(request) {
    const response = await fetch(request);
    const cacheControl = response.headers.get('Cache-Control') || '';

    // Respect origin's no-cache directive
    if (cacheControl.includes('no-cache') || cacheControl.includes('private')) {
      return response;
    }

    // Use origin's max-age if available
    const maxAgeMatch = cacheControl.match(/max-age=(\d+)/);
    if (maxAgeMatch) {
      return response; // Use origin's settings
    }

    // Set default cache if origin doesn't specify
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'public, max-age=3600');
    
    return new Response(response.body, {
      status: response.status,
      headers,
    });
  }
};
```

### 5. Monitor Cache Performance

```javascript
export default {
  async fetch(request, env, ctx) {
    const cache = caches.default;
    const startTime = Date.now();
    
    let response = await cache.match(request);
    const cacheHit = !!response;
    
    if (!response) {
      response = await fetch(request);
      ctx.waitUntil(cache.put(request, response.clone()));
    }
    
    const duration = Date.now() - startTime;
    
    // Log metrics
    console.log(JSON.stringify({
      url: request.url,
      cacheHit,
      duration,
      timestamp: new Date().toISOString(),
    }));

    // Add debug headers
    const headers = new Headers(response.headers);
    headers.set('X-Cache-Status', cacheHit ? 'HIT' : 'MISS');
    headers.set('X-Response-Time', `${duration}ms`);
    
    return new Response(response.body, {
      status: response.status,
      headers,
    });
  }
};
```

## Troubleshooting

### Cache Not Working

```bash
# Check CF-Cache-Status header
curl -I https://example.com/image.jpg | grep -i cf-cache-status

# If BYPASS, check:
# 1. DNS is proxied (orange cloud)
# 2. Cache headers are set correctly
# 3. No conflicting page rules
# 4. File extension is cacheable
```

### Cache Hit Rate Too Low

```javascript
// Analyze and normalize cache keys
export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // Remove tracking parameters
    const trackingParams = ['utm_source', 'utm_medium', 'fbclid', 'gclid'];
    trackingParams.forEach(param => url.searchParams.delete(param));
    
    // Sort query parameters for consistency
    url.searchParams.sort();
    
    const normalizedRequest = new Request(url.toString(), request);
    return fetch(normalizedRequest);
  }
};
```

### Purge Not Taking Effect

```bash
# Verify purge was successful
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://example.com/file.css"]}' | jq .

# Check for errors in response
# Wait 30 seconds for purge to propagate globally
```

### Origin Overload from Cache Misses

```javascript
// Implement request coalescing
const pendingRequests = new Map();

export default {
  async fetch(request, env, ctx) {
    const cache = caches.default;
    const cacheKey = request.url;

    let response = await cache.match(request);
    if (response) return response;

    // Coalesce concurrent requests
    if (pendingRequests.has(cacheKey)) {
      return await pendingRequests.get(cacheKey);
    }

    const fetchPromise = fetch(request).then(async (res) => {
      const cachedRes = res.clone();
      ctx.waitUntil(cache.put(request, cachedRes));
      pendingRequests.delete(cacheKey);
      return res;
    });

    pendingRequests.set(cacheKey, fetchPromise);
    return await fetchPromise;
  }
};
```

## See Also

- **Cloudflare Workers**: https://developers.cloudflare.com/workers/
- **Page Rules**: https://developers.cloudflare.com/rules/page-rules/
- **Transform Rules**: https://developers.cloudflare.com/rules/transform/
- **Cache Reserve**: https://developers.cloudflare.com/cache/advanced-configuration/cache-reserve/
- **Tiered Cache**: https://developers.cloudflare.com/cache/how-to/tiered-cache/
- **Argo Smart Routing**: https://developers.cloudflare.com/argo-smart-routing/
- **Polish (Image Optimization)**: https://developers.cloudflare.com/images/polish/
- **Cloudflare Images**: https://developers.cloudflare.com/images/
