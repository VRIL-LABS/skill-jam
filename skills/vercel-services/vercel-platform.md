---
name: Vercel Platform
description: |
  Cloud platform for Next.js hosting with Git integration, instant preview deployments, edge functions, and serverless.
  Use for deploying web apps, edge computing, preview environments, analytics, and global CDN distribution.
  Trigger phrases: "deploy to Vercel", "preview deployment", "edge functions", "serverless hosting", "Vercel analytics"
license: MIT
---

# Vercel Platform

Vercel is a cloud platform optimized for frontend frameworks and static sites, with native Next.js support. It provides Git integration, instant preview deployments, edge functions, serverless computing, and built-in analytics for modern web applications.

## When to Use

Use Vercel Platform when you need to:

- **Deploy Next.js applications** with zero configuration and optimal performance
- **Create preview deployments** automatically for every Git push
- **Run edge functions** at 300+ global locations for low latency
- **Implement serverless APIs** without managing infrastructure
- **Monitor web vitals** with built-in analytics and observability
- **Serve static sites** with automatic CDN distribution
- **Enable team collaboration** with deployment previews and comments
- **Scale automatically** based on traffic without manual intervention

## Official Documentation

- **Vercel Platform**: https://vercel.com/docs
- **Next.js on Vercel**: https://vercel.com/docs/frameworks/nextjs
- **Deployments**: https://vercel.com/docs/deployments
- **Functions**: https://vercel.com/docs/functions
- **Edge Functions**: https://vercel.com/docs/functions/edge-functions
- **Analytics**: https://vercel.com/docs/analytics
- **Speed Insights**: https://vercel.com/docs/speed-insights
- **Environment Variables**: https://vercel.com/docs/projects/environment-variables
- **Custom Domains**: https://vercel.com/docs/projects/domains
- **CLI Reference**: https://vercel.com/docs/cli

## Quick Start

### Install Vercel CLI

```bash
npm i -g vercel
```

### Deploy Your Project

```bash
cd my-next-app
vercel
```

### Deploy to Production

```bash
vercel --prod
```

### Create New Next.js App

```bash
npx create-next-app@latest my-app
cd my-app
git init
git add .
git commit -m "Initial commit"
vercel
```

## Core Features

### 1. Git Integration

```bash
# Connect repository
vercel link

# Auto-deploy on push
git push origin main

# Branch preview URLs
git checkout -b feature/new-design
git push origin feature/new-design
# Preview: https://my-app-git-feature-new-design.vercel.app
```

Configure in `vercel.json`:

```json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "staging": true
    }
  }
}
```

### 2. Preview Deployments

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  const isPreview = process.env.VERCEL_ENV === 'preview';
  const url = process.env.VERCEL_URL;

  return (
    <html>
      <body>
        {isPreview && <div>Preview: {url}</div>}
        {children}
      </body>
    </html>
  );
}
```

### 3. Edge Functions

```typescript
// app/api/edge/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  const geo = request.headers.get('x-vercel-ip-city');
  const country = request.headers.get('x-vercel-ip-country');

  return Response.json({
    message: 'Hello from the edge!',
    location: { city: geo, country },
  });
}
```

Edge middleware:

```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const country = request.geo?.country;
  
  if (country === 'US') {
    return NextResponse.redirect(new URL('/us', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/localized/:path*',
};
```

### 4. Serverless Functions

```typescript
// app/api/users/route.ts
export async function GET() {
  const users = await fetchUsers();
  return Response.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await createUser(body);
  return Response.json(user, { status: 201 });
}

export const maxDuration = 10;
```

Configure in `vercel.json`:

```json
{
  "functions": {
    "app/api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 10
    }
  }
}
```

### 5. Environment Variables

```bash
# Add variable
vercel env add DATABASE_URL

# Pull for local dev
vercel env pull .env.local

# List variables
vercel env ls
```

Access in code:

```typescript
export async function GET() {
  const db = process.env.DATABASE_URL;
  const env = process.env.VERCEL_ENV;
  
  return Response.json({ environment: env });
}
```

### 6. Custom Domains

```bash
# Add domain
vercel domains add example.com

# Add to project
vercel domains add example.com --project my-app
```

Configure redirects:

```json
{
  "redirects": [
    {
      "source": "/:path*",
      "destination": "https://www.example.com/:path*",
      "permanent": true,
      "has": [{ "type": "host", "value": "example.com" }]
    }
  ]
}
```

### 7. Analytics

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

Track custom events:

```typescript
'use client';
import { track } from '@vercel/analytics';

export function Button() {
  return (
    <button onClick={() => track('button_click', { page: 'home' })}>
      Click Me
    </button>
  );
}
```

### 8. Image Optimization

```typescript
import Image from 'next/image';

export default function ProductImage() {
  return (
    <Image
      src="/product.jpg"
      alt="Product"
      width={800}
      height={600}
      quality={85}
      priority
    />
  );
}
```

Configure:

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['cdn.example.com'],
    formats: ['image/avif', 'image/webp'],
  },
};
```

## Common Use Cases

### Full-Stack App

```typescript
// app/page.tsx
export default async function HomePage() {
  const posts = await getPosts();
  return <div>{posts.map(p => <article key={p.id}>{p.title}</article>)}</div>;
}

// app/api/posts/route.ts
export async function GET() {
  return Response.json(await getPosts());
}
```

### Incremental Static Regeneration

```typescript
// app/blog/[slug]/page.tsx
export const revalidate = 3600;

export async function generateStaticParams() {
  return (await getAllPosts()).map(p => ({ slug: p.slug }));
}

export default async function Post({ params }) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}
```

### API with Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export async function GET(request: Request) {
  const { success } = await ratelimit.limit(request.headers.get('x-forwarded-for') ?? 'anon');
  if (!success) return Response.json({ error: 'Rate limit exceeded' }, { status: 429 });
  return Response.json({ message: 'Success' });
}
```

### Authentication Middleware

```typescript
// middleware.ts
import { getToken } from 'next-auth/jwt';

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });
  if (!token) return NextResponse.redirect(new URL('/login', request.url));
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*'] };
```

### Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const body = await request.text();
  const sig = request.headers.get('stripe-signature')!;
  const event = stripe.webhooks.constructEvent(body, sig, process.env.SECRET!);
  await handleEvent(event);
  return Response.json({ received: true });
}
```

### Cron Jobs

```typescript
// app/api/cron/cleanup/route.ts
export async function GET(request: Request) {
  if (request.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }
  await cleanup();
  return Response.json({ success: true });
}
```

## Integration

### Vercel Postgres

```bash
npm install @vercel/postgres
```

```typescript
import { sql } from '@vercel/postgres';

export async function GET() {
  const { rows } = await sql`SELECT * FROM users`;
  return Response.json(rows);
}
```

### Vercel KV (Redis)

```bash
npm install @vercel/kv
```

```typescript
import { kv } from '@vercel/kv';

export async function POST(request: Request) {
  const { key, value } = await request.json();
  await kv.set(key, value, { ex: 3600 });
  return Response.json({ success: true });
}
```

### Vercel Blob

```bash
npm install @vercel/blob
```

```typescript
import { put } from '@vercel/blob';

export async function POST(request: Request) {
  const file = (await request.formData()).get('file') as File;
  const blob = await put(file.name, file, { access: 'public' });
  return Response.json({ url: blob.url });
}
```

### Edge Config

```bash
npm install @vercel/edge-config
```

```typescript
import { get } from '@vercel/edge-config';

export async function middleware(request: NextRequest) {
  const maintenance = await get('maintenance_mode');
  if (maintenance) return NextResponse.redirect('/maintenance');
  return NextResponse.next();
}
```

## Best Practices

### Optimize Builds

```javascript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['lodash'],
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
};
```

### Cache Control

```typescript
export async function GET() {
  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}
```

### Security Headers

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
        ],
      },
    ];
  },
};
```

### Monitoring

```typescript
export async function GET(request: Request) {
  const start = Date.now();

  try {
    const data = await fetchData();
    console.log({ event: 'success', duration: Date.now() - start });
    return Response.json(data);
  } catch (error) {
    console.error({ event: 'error', duration: Date.now() - start });
    return Response.json({ error: 'Failed' }, { status: 500 });
  }
}
```

### Type-Safe Env

```typescript
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
```

## Troubleshooting

### Build Failures

**Problem**: Build memory errors

**Solutions**:
```json
{
  "functions": {
    "api/**/*.ts": {
      "memory": 3008
    }
  }
}
```

### Environment Variables

**Problem**: Variables not updating

**Solutions**:
```bash
vercel --force
# Or
vercel env pull
vercel
```

### Function Timeout

**Problem**: Function timeout

**Solutions**:
```typescript
export const maxDuration = 60; // Requires Pro plan
```

### CORS Issues

**Problem**: CORS errors

**Solutions**:
```typescript
export async function GET() {
  return Response.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST',
    },
  });
}
```

### Image Optimization

**Problem**: Images not loading

**Solutions**:
```javascript
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },
};
```

## See Also

- [Vercel AI Gateway](./vercel-ai-gateway.md) - AI model access
- [Next.js Documentation](https://nextjs.org/docs) - Next.js framework
- [Vercel CLI](https://vercel.com/docs/cli) - CLI reference
- [Vercel Storage](https://vercel.com/docs/storage) - Storage solutions
- [Vercel Templates](https://vercel.com/templates) - Starter templates
