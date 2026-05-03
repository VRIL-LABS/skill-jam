---
name: Cloudflare R2
description: |
  Use Cloudflare R2 object storage with S3-compatible API and zero egress fees.
  Trigger phrases: "cloudflare r2", "r2 storage", "s3 compatible cloudflare",
  "object storage r2", "zero egress", "r2 bucket", "cloudflare object storage"
license: MIT
---

# Cloudflare R2

Cloudflare R2 is an S3-compatible object storage service with zero egress fees. Store files, images, videos, backups, and any unstructured data globally with automatic replication and Workers integration.

## When to Use

**Best for:**
- **Media storage**: Images, videos, audio files
- **File uploads**: User-generated content, avatars, documents
- **Static assets**: CSS, JavaScript, fonts for CDN delivery
- **Backups**: Database backups, application snapshots
- **Data lakes**: Large-scale data storage for analytics
- **Public downloads**: Software releases, datasets
- **Archives**: Long-term data retention
- **CDN origin**: Serve assets globally with zero egress costs

**Not ideal for:**
- Transactional databases (use D1 instead)
- Real-time data streams (use Queues/Pub/Sub)
- Frequently modified small files (use KV instead)
- Data requiring ACID transactions

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/r2/
- **Get Started**: https://developers.cloudflare.com/r2/get-started/
- **API Reference**: https://developers.cloudflare.com/r2/api/
- **Workers Integration**: https://developers.cloudflare.com/r2/api/workers/
- **S3 Compatibility**: https://developers.cloudflare.com/r2/api/s3/
- **Public Buckets**: https://developers.cloudflare.com/r2/buckets/public-buckets/
- **Pricing**: https://developers.cloudflare.com/r2/pricing/
- **Limits**: https://developers.cloudflare.com/r2/platform/limits/

## Quick Start

### 1. Create R2 Bucket via Dashboard

```bash
# 1. Go to Cloudflare Dashboard
# 2. Navigate to R2
# 3. Click "Create bucket"
# 4. Enter bucket name (e.g., "my-files")
# 5. Click "Create bucket"

# Or via Wrangler CLI
wrangler r2 bucket create my-files
```

### 2. List Buckets

```bash
# List all R2 buckets
wrangler r2 bucket list

# Get bucket info
wrangler r2 bucket info my-files
```

### 3. Upload Files via CLI

```bash
# Upload a file
wrangler r2 object put my-files/example.txt --file=./local-file.txt

# Upload with content type
wrangler r2 object put my-files/image.png --file=./image.png --content-type=image/png

# List objects
wrangler r2 object list my-files

# Download object
wrangler r2 object get my-files/example.txt --file=./downloaded.txt

# Delete object
wrangler r2 object delete my-files/example.txt
```

### 4. Workers Integration

```typescript
// src/index.ts
interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);
    
    switch (request.method) {
      case 'GET':
        return handleGet(env.MY_BUCKET, key);
      case 'PUT':
        return handlePut(env.MY_BUCKET, key, request);
      case 'DELETE':
        return handleDelete(env.MY_BUCKET, key);
      default:
        return new Response('Method Not Allowed', { status: 405 });
    }
  }
};

async function handleGet(bucket: R2Bucket, key: string): Promise<Response> {
  const object = await bucket.get(key);
  
  if (!object) {
    return new Response('Not Found', { status: 404 });
  }
  
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('ETag', object.httpEtag);
  headers.set('Cache-Control', 'public, max-age=86400');
  
  return new Response(object.body, { headers });
}

async function handlePut(bucket: R2Bucket, key: string, request: Request): Promise<Response> {
  await bucket.put(key, request.body, {
    httpMetadata: {
      contentType: request.headers.get('Content-Type') || 'application/octet-stream'
    }
  });
  
  return Response.json({ success: true, key });
}

async function handleDelete(bucket: R2Bucket, key: string): Promise<Response> {
  await bucket.delete(key);
  return Response.json({ success: true });
}
```

```toml
# wrangler.toml
name = "r2-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-files"
```

## Core Features

### Upload Objects

```typescript
interface Env {
  UPLOADS: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }
    
    const formData = await request.formData();
    const file = formData.get('file') as File;
    
    if (!file) {
      return Response.json({ error: 'No file provided' }, { status: 400 });
    }
    
    // Generate unique key
    const timestamp = Date.now();
    const key = `uploads/${timestamp}-${file.name}`;
    
    // Upload to R2
    await env.UPLOADS.put(key, file.stream(), {
      httpMetadata: {
        contentType: file.type,
        contentDisposition: `inline; filename="${file.name}"`
      },
      customMetadata: {
        originalName: file.name,
        uploadedAt: new Date().toISOString(),
        uploadedBy: request.headers.get('CF-Connecting-IP') || 'unknown'
      }
    });
    
    return Response.json({
      success: true,
      key: key,
      url: `https://yourworker.com/${key}`
    });
  }
};
```

### Download with Range Requests

```typescript
async function handleRangeRequest(
  bucket: R2Bucket,
  key: string,
  request: Request
): Promise<Response> {
  const rangeHeader = request.headers.get('Range');
  
  if (!rangeHeader) {
    // Normal download
    const object = await bucket.get(key);
    if (!object) {
      return new Response('Not Found', { status: 404 });
    }
    return new Response(object.body);
  }
  
  // Parse range header (e.g., "bytes=0-1023")
  const match = rangeHeader.match(/bytes=(\d+)-(\d*)/);
  if (!match) {
    return new Response('Invalid Range', { status: 416 });
  }
  
  const start = parseInt(match[1]);
  const end = match[2] ? parseInt(match[2]) : undefined;
  
  // Get object with range
  const object = await bucket.get(key, {
    range: { offset: start, length: end ? end - start + 1 : undefined }
  });
  
  if (!object) {
    return new Response('Not Found', { status: 404 });
  }
  
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('Content-Range', `bytes ${start}-${end || object.size - 1}/${object.size}`);
  headers.set('Accept-Ranges', 'bytes');
  
  return new Response(object.body, {
    status: 206,
    headers
  });
}
```

### List Objects with Pagination

```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const prefix = url.searchParams.get('prefix') || '';
    const cursor = url.searchParams.get('cursor') || undefined;
    const limit = parseInt(url.searchParams.get('limit') || '100');
    
    // List objects
    const listed = await env.MY_BUCKET.list({
      prefix: prefix,
      cursor: cursor,
      limit: limit
    });
    
    const objects = listed.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded,
      httpEtag: obj.httpEtag,
      customMetadata: obj.customMetadata
    }));
    
    return Response.json({
      objects: objects,
      truncated: listed.truncated,
      cursor: listed.truncated ? listed.cursor : null,
      delimitedPrefixes: listed.delimitedPrefixes
    });
  }
};
```

### Multipart Uploads

```typescript
interface Env {
  LARGE_FILES: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Start multipart upload
    if (url.pathname === '/start-upload' && request.method === 'POST') {
      const { key } = await request.json<{ key: string }>();
      
      const multipartUpload = await env.LARGE_FILES.createMultipartUpload(key, {
        httpMetadata: {
          contentType: 'video/mp4'
        }
      });
      
      return Response.json({
        uploadId: multipartUpload.uploadId,
        key: multipartUpload.key
      });
    }
    
    // Upload part
    if (url.pathname === '/upload-part' && request.method === 'PUT') {
      const { key, uploadId, partNumber } = await request.json<{
        key: string;
        uploadId: string;
        partNumber: number;
      }>();
      
      const multipartUpload = env.LARGE_FILES.resumeMultipartUpload(key, uploadId);
      
      const part = await multipartUpload.uploadPart(partNumber, request.body!);
      
      return Response.json({
        partNumber: part.partNumber,
        etag: part.etag
      });
    }
    
    // Complete upload
    if (url.pathname === '/complete-upload' && request.method === 'POST') {
      const { key, uploadId, parts } = await request.json<{
        key: string;
        uploadId: string;
        parts: R2UploadedPart[];
      }>();
      
      const multipartUpload = env.LARGE_FILES.resumeMultipartUpload(key, uploadId);
      
      const object = await multipartUpload.complete(parts);
      
      return Response.json({
        key: object.key,
        etag: object.etag,
        size: object.size
      });
    }
    
    // Abort upload
    if (url.pathname === '/abort-upload' && request.method === 'DELETE') {
      const { key, uploadId } = await request.json<{
        key: string;
        uploadId: string;
      }>();
      
      const multipartUpload = env.LARGE_FILES.resumeMultipartUpload(key, uploadId);
      await multipartUpload.abort();
      
      return Response.json({ success: true });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Conditional Requests

```typescript
async function handleConditionalGet(
  bucket: R2Bucket,
  key: string,
  request: Request
): Promise<Response> {
  const ifNoneMatch = request.headers.get('If-None-Match');
  const ifModifiedSince = request.headers.get('If-Modified-Since');
  
  const object = await bucket.get(key, {
    onlyIf: {
      etagDoesNotMatch: ifNoneMatch || undefined,
      uploadedAfter: ifModifiedSince ? new Date(ifModifiedSince) : undefined
    }
  });
  
  if (object === null) {
    // Object exists but conditions not met (304 Not Modified)
    const head = await bucket.head(key);
    if (head) {
      return new Response(null, {
        status: 304,
        headers: {
          'ETag': head.httpEtag,
          'Last-Modified': head.uploaded.toUTCString()
        }
      });
    }
    return new Response('Not Found', { status: 404 });
  }
  
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('ETag', object.httpEtag);
  headers.set('Last-Modified', object.uploaded.toUTCString());
  headers.set('Cache-Control', 'public, max-age=31536000');
  
  return new Response(object.body, { headers });
}
```

### Image Transformations

```typescript
interface Env {
  IMAGES: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);
    
    // Get transformation params
    const width = url.searchParams.get('width');
    const quality = url.searchParams.get('quality') || '85';
    const format = url.searchParams.get('format') || 'auto';
    
    // Fetch from R2
    const object = await env.IMAGES.get(key);
    
    if (!object) {
      return new Response('Not Found', { status: 404 });
    }
    
    // Transform image using Cloudflare Images or external service
    if (width) {
      const transformedUrl = new URL('https://images.example.com/transform');
      transformedUrl.searchParams.set('width', width);
      transformedUrl.searchParams.set('quality', quality);
      transformedUrl.searchParams.set('format', format);
      
      // Stream original to transformation service
      const response = await fetch(transformedUrl, {
        method: 'POST',
        body: object.body
      });
      
      return response;
    }
    
    // Return original
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    
    return new Response(object.body, { headers });
  }
};
```

## Common Use Cases

### Public CDN for Static Assets

```typescript
interface Env {
  PUBLIC_ASSETS: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const cacheKey = new Request(url.toString(), request);
    const cache = caches.default;
    
    // Check cache first
    let response = await cache.match(cacheKey);
    if (response) {
      return response;
    }
    
    // Fetch from R2
    const key = url.pathname.slice(1);
    const object = await env.PUBLIC_ASSETS.get(key);
    
    if (!object) {
      return new Response('Not Found', { status: 404 });
    }
    
    // Create response with cache headers
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    headers.set('ETag', object.httpEtag);
    
    response = new Response(object.body, { headers });
    
    // Store in cache
    await cache.put(cacheKey, response.clone());
    
    return response;
  }
};
```

### Signed URLs for Private Content

```typescript
import { SignJWT } from 'jose';

interface Env {
  PRIVATE_FILES: R2Bucket;
  JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Generate signed URL
    if (url.pathname === '/generate-url' && request.method === 'POST') {
      const { key, expiresIn } = await request.json<{
        key: string;
        expiresIn: number;
      }>();
      
      const secret = new TextEncoder().encode(env.JWT_SECRET);
      const token = await new SignJWT({ key })
        .setProtectedHeader({ alg: 'HS256' })
        .setExpirationTime(`${expiresIn}s`)
        .sign(secret);
      
      return Response.json({
        url: `https://yourworker.com/download?token=${token}`
      });
    }
    
    // Download with signed URL
    if (url.pathname === '/download') {
      const token = url.searchParams.get('token');
      
      if (!token) {
        return new Response('Missing token', { status: 401 });
      }
      
      try {
        const secret = new TextEncoder().encode(env.JWT_SECRET);
        const { payload } = await jwtVerify(token, secret);
        const key = payload.key as string;
        
        const object = await env.PRIVATE_FILES.get(key);
        
        if (!object) {
          return new Response('Not Found', { status: 404 });
        }
        
        const headers = new Headers();
        object.writeHttpMetadata(headers);
        
        return new Response(object.body, { headers });
      } catch (err) {
        return new Response('Invalid or expired token', { status: 401 });
      }
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### S3 API Compatibility

```typescript
// Using AWS SDK with R2
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';

interface Env {
  R2_ACCESS_KEY_ID: string;
  R2_SECRET_ACCESS_KEY: string;
  R2_ACCOUNT_ID: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const s3Client = new S3Client({
      region: 'auto',
      endpoint: `https://${env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
      credentials: {
        accessKeyId: env.R2_ACCESS_KEY_ID,
        secretAccessKey: env.R2_SECRET_ACCESS_KEY
      }
    });
    
    // Upload using S3 API
    await s3Client.send(new PutObjectCommand({
      Bucket: 'my-bucket',
      Key: 'example.txt',
      Body: 'Hello R2!',
      ContentType: 'text/plain'
    }));
    
    // Download using S3 API
    const response = await s3Client.send(new GetObjectCommand({
      Bucket: 'my-bucket',
      Key: 'example.txt'
    }));
    
    const body = await response.Body?.transformToString();
    
    return new Response(body);
  }
};
```

## Integration

### Binding in wrangler.toml

```toml
name = "r2-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# R2 Buckets
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "production-files"
preview_bucket_name = "dev-files"

[[r2_buckets]]
binding = "IMAGES"
bucket_name = "images"

# Environment variables for S3 API
[vars]
R2_ACCOUNT_ID = "your-account-id"

# Secrets (use wrangler secret put)
# R2_ACCESS_KEY_ID
# R2_SECRET_ACCESS_KEY
```

### Public Buckets

```bash
# Enable public access via dashboard or CLI
# Dashboard: R2 > Bucket > Settings > Public Access

# Add custom domain
# Dashboard: R2 > Bucket > Settings > Public Access > Add Custom Domain
# Example: assets.example.com

# Access publicly
curl https://pub-xxxxx.r2.dev/image.png
curl https://assets.example.com/image.png
```

### CORS Configuration

```typescript
// Configure CORS for browser uploads
interface Env {
  UPLOADS: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400'
        }
      });
    }
    
    // Handle request
    const response = await handleRequest(request, env);
    
    // Add CORS headers to response
    const headers = new Headers(response.headers);
    headers.set('Access-Control-Allow-Origin', '*');
    
    return new Response(response.body, {
      status: response.status,
      headers
    });
  }
};
```

## Best Practices

1. **Use descriptive keys**: Organize with prefixes (e.g., `users/123/avatar.jpg`)
2. **Set content types**: Always specify correct HTTP metadata
3. **Implement caching**: Use ETags and Cache-Control headers
4. **Handle errors**: Check for null responses from R2 operations
5. **Use custom domains**: Better branding and SEO than r2.dev URLs
6. **Multipart for large files**: Files >100MB should use multipart uploads
7. **Add metadata**: Store useful info in customMetadata
8. **Monitor usage**: Track storage and request counts in dashboard
9. **Implement lifecycle**: Delete old/unused objects to reduce costs
10. **Security**: Use signed URLs for private content, validate uploads

## Troubleshooting

### Binding errors

```typescript
// Ensure binding name matches wrangler.toml
interface Env {
  MY_BUCKET: R2Bucket;  // Must match binding = "MY_BUCKET"
}

// Check bucket exists
wrangler r2 bucket list
```

### Upload failures

```typescript
// Handle errors properly
try {
  await env.MY_BUCKET.put(key, data);
} catch (error) {
  console.error('Upload failed:', error);
  return Response.json(
    { error: 'Upload failed' },
    { status: 500 }
  );
}

// Check file size limits (5TB max per object)
// Use multipart for files >100MB
```

### Download issues

```typescript
// Always check for null
const object = await bucket.get(key);

if (!object) {
  return new Response('Object not found', { status: 404 });
}

// Handle range requests properly
const rangeHeader = request.headers.get('Range');
// Implement range logic
```

### CORS errors

```typescript
// Ensure preflight requests are handled
if (request.method === 'OPTIONS') {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, PUT, DELETE',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}
```

## See Also

- [Cloudflare Workers](cloudflare-workers.md) - Runtime for R2 access
- [Cloudflare KV](cloudflare-kv.md) - Alternative for small, frequently accessed data
- [Cloudflare D1](cloudflare-d1.md) - SQL database for metadata
- [Cloudflare Pages](cloudflare-pages.md) - Static site hosting
- **Cloudflare Images**: https://developers.cloudflare.com/images/
- **Stream**: https://developers.cloudflare.com/stream/
