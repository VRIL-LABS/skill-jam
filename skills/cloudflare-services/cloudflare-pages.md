---
name: Cloudflare Pages
description: |
  Deploy JAMstack sites and full-stack applications with Cloudflare Pages.
  Trigger phrases: "cloudflare pages", "jamstack hosting", "static site cloudflare",
  "pages functions", "git deployment", "edge ssr", "cloudflare deploy", "pages deployment"
license: MIT
---

# Cloudflare Pages

Cloudflare Pages is a JAMstack platform for deploying static sites and full-stack applications. With Git integration, automatic builds, global CDN acceleration, and serverless Functions, Pages makes it easy to deploy modern web applications.

## When to Use

**Best for:**
- **Static sites**: Marketing sites, blogs, documentation
- **Single Page Applications**: React, Vue, Angular, Svelte apps
- **JAMstack architectures**: Static HTML with API-driven content
- **Full-stack apps**: Combining static frontend with Pages Functions
- **Preview deployments**: Automatic previews for pull requests
- **Monorepo projects**: Deploy multiple projects from one repository
- **Frameworks**: Next.js, Nuxt, SvelteKit, Astro, Remix
- **Blogs**: Hugo, Jekyll, Gatsby, Eleventy sites

**Not ideal for:**
- Applications requiring WebSockets (use Workers directly)
- Server-rendered apps with complex state (consider hybrid approach)
- File uploads >25MB (use Workers with R2)

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/pages/
- **Get Started**: https://developers.cloudflare.com/pages/get-started/
- **Framework Guides**: https://developers.cloudflare.com/pages/framework-guides/
- **Functions**: https://developers.cloudflare.com/pages/functions/
- **Platform**: https://developers.cloudflare.com/pages/platform/
- **Deployments**: https://developers.cloudflare.com/pages/configuration/
- **Builds**: https://developers.cloudflare.com/pages/configuration/build-configuration/
- **Redirects**: https://developers.cloudflare.com/pages/configuration/redirects/
- **Headers**: https://developers.cloudflare.com/pages/configuration/headers/

## Quick Start

### 1. Via Dashboard (Git Integration)

```bash
# 1. Push your site to GitHub/GitLab
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/my-site.git
git push -u origin main

# 2. Go to Cloudflare Dashboard
# - Navigate to Pages
# - Click "Create a project"
# - Connect your GitHub/GitLab account
# - Select repository
# - Configure build settings
# - Click "Save and Deploy"
```

### 2. Via Wrangler CLI (Direct Upload)

```bash
# Install Wrangler
npm install -g wrangler

# Build your site
npm run build

# Deploy to Pages
wrangler pages deploy dist --project-name=my-site

# Deploy with custom branch
wrangler pages deploy dist --project-name=my-site --branch=production
```

### 3. Static Site Example

```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Cloudflare Pages Site</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <h1>Welcome to Cloudflare Pages</h1>
  </header>
  
  <main>
    <section id="content">
      <p>Lightning-fast static site hosting on the edge.</p>
      <button id="fetchBtn">Fetch Data</button>
      <div id="result"></div>
    </section>
  </main>
  
  <script src="/script.js"></script>
</body>
</html>
```

```javascript
// public/script.js
document.getElementById('fetchBtn').addEventListener('click', async () => {
  try {
    const response = await fetch('/api/hello');
    const data = await response.json();
    document.getElementById('result').innerHTML = `
      <pre>${JSON.stringify(data, null, 2)}</pre>
    `;
  } catch (error) {
    console.error('Error:', error);
  }
});
```

```css
/* public/styles.css */
:root {
  --primary: #f38020;
  --background: #1a1a1a;
  --text: #ffffff;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--background);
  color: var(--text);
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

button {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  opacity: 0.9;
}
```

## Core Features

### Pages Functions (Serverless)

Pages Functions are serverless functions deployed alongside your static assets. They use the same runtime as Cloudflare Workers.

```typescript
// functions/api/hello.ts
interface Env {
  DB: D1Database;
  CACHE: KVNamespace;
}

export async function onRequest(context: EventContext<Env, any, any>): Promise<Response> {
  const { request, env } = context;
  
  return Response.json({
    message: 'Hello from Pages Functions!',
    time: new Date().toISOString(),
    location: request.cf?.city || 'Unknown'
  });
}
```

### Advanced Routing

```typescript
// functions/api/users/[id].ts
interface Env {
  DB: D1Database;
}

// GET /api/users/:id
export async function onRequestGet(context: EventContext<Env, any, any>): Promise<Response> {
  const { params, env } = context;
  const userId = params.id as string;
  
  const user = await env.DB.prepare(
    'SELECT * FROM users WHERE id = ?'
  )
  .bind(userId)
  .first();
  
  if (!user) {
    return new Response('User not found', { status: 404 });
  }
  
  return Response.json(user);
}

// PUT /api/users/:id
export async function onRequestPut(context: EventContext<Env, any, any>): Promise<Response> {
  const { request, params, env } = context;
  const userId = params.id as string;
  const { name, email } = await request.json<{ name: string; email: string }>();
  
  await env.DB.prepare(
    'UPDATE users SET name = ?, email = ? WHERE id = ?'
  )
  .bind(name, email, userId)
  .run();
  
  return Response.json({ success: true });
}

// DELETE /api/users/:id
export async function onRequestDelete(context: EventContext<Env, any, any>): Promise<Response> {
  const { params, env } = context;
  const userId = params.id as string;
  
  await env.DB.prepare('DELETE FROM users WHERE id = ?')
    .bind(userId)
    .run();
  
  return Response.json({ success: true });
}
```

### Middleware

```typescript
// functions/_middleware.ts
interface Env {
  JWT_SECRET: string;
}

export async function onRequest(context: EventContext<Env, any, any>): Promise<Response> {
  const { request, next, env } = context;
  
  // CORS headers
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });
  }
  
  // Authentication check for /api/* routes
  const url = new URL(request.url);
  if (url.pathname.startsWith('/api/')) {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader?.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }
    
    // Verify JWT (simplified)
    const token = authHeader.substring(7);
    // Add JWT verification logic here
  }
  
  // Continue to next handler
  const response = await next();
  
  // Add security headers
  const newHeaders = new Headers(response.headers);
  newHeaders.set('X-Content-Type-Options', 'nosniff');
  newHeaders.set('X-Frame-Options', 'DENY');
  newHeaders.set('X-XSS-Protection', '1; mode=block');
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}
```

### Environment Variables

```typescript
// functions/api/config.ts
interface Env {
  // Public variables (visible in browser)
  PUBLIC_API_URL: string;
  
  // Private variables (server-side only)
  API_KEY: string;
  DATABASE_URL: string;
}

export async function onRequest(context: EventContext<Env, any, any>): Promise<Response> {
  const { env } = context;
  
  // Use environment variables
  const apiResponse = await fetch(env.PUBLIC_API_URL, {
    headers: {
      'Authorization': `Bearer ${env.API_KEY}`
    }
  });
  
  const data = await apiResponse.json();
  
  return Response.json(data);
}
```

### Form Handling

```typescript
// functions/api/contact.ts
interface Env {
  RESEND_API_KEY: string;
}

export async function onRequestPost(context: EventContext<Env, any, any>): Promise<Response> {
  const { request, env } = context;
  
  // Parse form data
  const formData = await request.formData();
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  const message = formData.get('message') as string;
  
  // Validate
  if (!name || !email || !message) {
    return Response.json(
      { error: 'All fields are required' },
      { status: 400 }
    );
  }
  
  // Send email via Resend
  const emailResponse = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: 'noreply@example.com',
      to: 'contact@example.com',
      subject: 'New Contact Form Submission',
      html: `
        <h2>New message from ${name}</h2>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Message:</strong></p>
        <p>${message}</p>
      `
    })
  });
  
  if (!emailResponse.ok) {
    return Response.json(
      { error: 'Failed to send email' },
      { status: 500 }
    );
  }
  
  return Response.json({ success: true });
}
```

## Common Use Cases

### React SPA with API

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist'
  }
});
```

```typescript
// functions/api/data.ts
export async function onRequest(): Promise<Response> {
  const data = {
    users: [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' }
    ]
  };
  
  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, max-age=300'
    }
  });
}
```

```typescript
// src/App.tsx
import { useEffect, useState } from 'react';

interface User {
  id: number;
  name: string;
}

export default function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch('/api/data')
      .then(r => r.json())
      .then(data => {
        setUsers(data.users);
        setLoading(false);
      });
  }, []);
  
  if (loading) return <div>Loading...</div>;
  
  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Next.js Application

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true
  }
};

module.exports = nextConfig;
```

```typescript
// pages/api/hello.ts (using Pages Functions)
// Move to functions/api/hello.ts for Pages deployment
export async function onRequest(): Promise<Response> {
  return Response.json({
    message: 'Hello from Next.js on Cloudflare Pages!'
  });
}
```

### Astro Site

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'hybrid',
  adapter: cloudflare()
});
```

```astro
---
// src/pages/api/posts.ts
export async function GET({ request }) {
  const posts = await fetchPosts();
  
  return new Response(JSON.stringify(posts), {
    headers: {
      'Content-Type': 'application/json'
    }
  });
}
---
```

### Hugo Static Site

```toml
# config.toml
baseURL = "https://mysite.pages.dev"
languageCode = "en-us"
title = "My Hugo Site"
theme = "your-theme"

[build]
  writeStats = true

[outputs]
  home = ["HTML", "RSS", "JSON"]
```

```bash
# Build configuration in Pages dashboard
# Build command: hugo
# Build output directory: public
```

## Integration

### Build Configuration

Create `wrangler.toml` for Pages project:

```toml
name = "my-pages-project"
compatibility_date = "2024-01-01"
pages_build_output_dir = "dist"

# KV Namespaces
[[kv_namespaces]]
binding = "CACHE"
id = "your-kv-id"

# D1 Databases
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "your-db-id"

# R2 Buckets
[[r2_buckets]]
binding = "ASSETS"
bucket_name = "my-assets"

# Environment Variables
[vars]
PUBLIC_API_URL = "https://api.example.com"
ENVIRONMENT = "production"
```

### Redirects Configuration

```toml
# public/_redirects
# Redirect rules (processed top to bottom)

# Redirect old blog to new location
/old-blog/* /blog/:splat 301

# SPA fallback (must be last)
/* /index.html 200

# Redirect with specific status
/temp-redirect /new-page 302

# Query parameters
/search  /search-page?q=:q

# Country-based redirects
/  /uk  302  Country=GB
/  /us  302  Country=US

# Custom headers in redirect
/api/*  https://api.backend.com/:splat  200  X-Custom-Header=value
```

### Headers Configuration

```toml
# public/_headers
# Custom headers for specific paths

/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/api/*
  Cache-Control: no-cache, no-store, must-revalidate
  Access-Control-Allow-Origin: https://example.com
  Access-Control-Allow-Methods: GET, POST, OPTIONS

/sw.js
  Cache-Control: no-cache
```

### Custom Domains

```bash
# Via Wrangler CLI
wrangler pages deployment tail --project-name=my-site

# Add custom domain via dashboard or CLI
# Dashboard: Pages > Your Project > Custom domains > Set up a domain
```

### Preview Deployments

Every push to a branch creates a preview deployment:

```bash
# Automatic preview URL format
https://<commit-hash>.<project-name>.pages.dev
https://<branch>.<project-name>.pages.dev

# Access preview deployments programmatically
curl https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/deployments \
  -H "Authorization: Bearer {api_token}"
```

## Best Practices

1. **Optimize Assets**: Compress images, minify CSS/JS before deployment
2. **Use _redirects**: Define redirects in `_redirects` file for better performance
3. **Set Cache Headers**: Use `_headers` file for static asset caching
4. **Environment Variables**: Use Pages dashboard for secrets, not in code
5. **Preview Deployments**: Test changes in preview before merging to production
6. **Build Optimization**: Cache dependencies to speed up build times
7. **Functions Placement**: Keep Functions code in `/functions` directory
8. **Error Handling**: Create custom 404.html for better UX
9. **Security Headers**: Always set security headers in `_headers` or middleware
10. **Monitor Builds**: Use build logs to debug deployment issues

## Troubleshooting

### Build Failures

```bash
# Check build logs in Dashboard or via CLI
wrangler pages deployment tail --project-name=my-site

# Common fixes:
# 1. Verify build command
# 2. Check Node.js version compatibility
# 3. Ensure all dependencies in package.json
# 4. Clear build cache in dashboard

# Set build environment variables
# Dashboard: Pages > Settings > Environment variables
```

### Functions Not Working

```typescript
// Ensure Functions are in correct directory structure
// ✅ Correct
functions/
  api/
    hello.ts        # Accessible at /api/hello
  _middleware.ts    # Applies to all routes

// ❌ Wrong
src/functions/      # Won't work
api/functions/      # Won't work
```

### Redirects Not Applied

```toml
# _redirects file must be in build output directory
# For Vite: copy to public/ folder
# For Next.js: add to public/ folder
# For Hugo: add to static/ folder

# Ensure proper syntax (no comments inline)
/old-path /new-path 301

# Debug with curl
curl -I https://yoursite.pages.dev/old-path
```

### Custom Domain Issues

```bash
# Verify DNS records
# For apex domain: Add A/AAAA records from Pages dashboard
# For subdomain: Add CNAME record pointing to project.pages.dev

# Check SSL certificate status in dashboard
# SSL provisioning can take up to 24 hours

# Verify domain ownership
dig yourdomain.com
```

### Build Output Directory

```javascript
// Ensure correct output directory in build config

// Vite
export default defineConfig({
  build: { outDir: 'dist' }  // Set in Pages: dist
});

// Next.js (static export)
module.exports = {
  output: 'export',  // Creates 'out' directory
  distDir: 'out'     // Set in Pages: out
};

// Astro
export default defineConfig({
  outDir: './dist'  // Set in Pages: dist
});
```

## See Also

- [Cloudflare Workers](cloudflare-workers.md) - Serverless functions powering Pages Functions
- [Cloudflare D1](cloudflare-d1.md) - SQLite database for Pages Functions
- [Cloudflare KV](cloudflare-kv.md) - Key-value storage for Pages
- [Cloudflare R2](cloudflare-r2.md) - Object storage for assets
- **Pages Plugins**: https://developers.cloudflare.com/pages/functions/plugins/
- **Deploy Hooks**: https://developers.cloudflare.com/pages/configuration/deploy-hooks/
- **Rollbacks**: https://developers.cloudflare.com/pages/configuration/rollbacks/
