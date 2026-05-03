---
name: Cloudflare D1
description: |
  Deploy serverless SQLite databases at the edge with Cloudflare D1.
  Trigger phrases: "cloudflare d1", "serverless sqlite", "edge database",
  "d1 database", "sqlite cloudflare", "serverless sql", "d1 workers"
license: MIT
---

# Cloudflare D1

Cloudflare D1 is a serverless SQL database built on SQLite, designed for Cloudflare Workers. Run SQL queries at the edge with automatic replication, zero-maintenance scaling, and Workers integration.

## When to Use

**Best for:**
- **Relational data**: Structured data with relationships
- **Transactional operations**: ACID-compliant database operations
- **SQL queries**: Complex joins, aggregations, and analytics
- **User data**: Profiles, preferences, settings
- **Content management**: Blog posts, products, inventory
- **Session storage**: User sessions with complex queries
- **Analytics**: Time-series data and aggregations
- **Multi-tenant apps**: Isolated data per customer

**Not ideal for:**
- Extremely large datasets (>10GB per database)
- High-frequency writes (>1000 writes/second)
- Binary large objects (use R2 instead)
- Simple key-value data (use KV instead)
- Real-time collaborative editing

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/d1/
- **Get Started**: https://developers.cloudflare.com/d1/get-started/
- **Database Guide**: https://developers.cloudflare.com/d1/build-with-d1/
- **Workers API**: https://developers.cloudflare.com/d1/build-with-d1/d1-client-api/
- **Migrations**: https://developers.cloudflare.com/d1/reference/migrations/
- **Limits**: https://developers.cloudflare.com/d1/platform/limits/
- **Pricing**: https://developers.cloudflare.com/d1/platform/pricing/
- **Best Practices**: https://developers.cloudflare.com/d1/best-practices/

## Quick Start

### 1. Create Database

```bash
# Create D1 database
wrangler d1 create my-database

# Output includes database ID - copy it!
# ✅ Successfully created DB 'my-database'
# Database ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 2. Configure wrangler.toml

```toml
name = "d1-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 3. Create Schema Migration

```bash
# Create migration file
wrangler d1 migrations create my-database initial-schema
```

```sql
-- migrations/0001_initial-schema.sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published);
```

### 4. Apply Migrations

```bash
# Apply migrations locally
wrangler d1 migrations apply my-database --local

# Apply migrations to production
wrangler d1 migrations apply my-database --remote
```

### 5. Basic Worker Example

```typescript
// src/index.ts
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Create user
    if (url.pathname === '/users' && request.method === 'POST') {
      const { email, name } = await request.json<{ email: string; name: string }>();
      
      const result = await env.DB.prepare(
        'INSERT INTO users (email, name) VALUES (?, ?)'
      )
      .bind(email, name)
      .run();
      
      return Response.json({
        success: result.success,
        userId: result.meta.last_row_id
      });
    }
    
    // Get all users
    if (url.pathname === '/users' && request.method === 'GET') {
      const { results } = await env.DB.prepare(
        'SELECT id, email, name, created_at FROM users ORDER BY created_at DESC'
      ).all();
      
      return Response.json(results);
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

## Core Features

### CRUD Operations

```typescript
interface Env {
  DB: D1Database;
}

interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // CREATE
    if (path === '/users' && request.method === 'POST') {
      const { email, name } = await request.json<{ email: string; name: string }>();
      
      try {
        const result = await env.DB.prepare(
          'INSERT INTO users (email, name) VALUES (?, ?)'
        )
        .bind(email, name)
        .run();
        
        return Response.json({
          success: true,
          id: result.meta.last_row_id
        });
      } catch (error: any) {
        return Response.json(
          { error: error.message },
          { status: 400 }
        );
      }
    }
    
    // READ ONE
    if (path.startsWith('/users/') && request.method === 'GET') {
      const userId = path.split('/')[2];
      
      const user = await env.DB.prepare(
        'SELECT * FROM users WHERE id = ?'
      )
      .bind(userId)
      .first<User>();
      
      if (!user) {
        return new Response('User not found', { status: 404 });
      }
      
      return Response.json(user);
    }
    
    // READ ALL
    if (path === '/users' && request.method === 'GET') {
      const page = parseInt(url.searchParams.get('page') || '1');
      const limit = parseInt(url.searchParams.get('limit') || '10');
      const offset = (page - 1) * limit;
      
      const { results } = await env.DB.prepare(
        'SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?'
      )
      .bind(limit, offset)
      .all<User>();
      
      return Response.json({
        users: results,
        page,
        limit
      });
    }
    
    // UPDATE
    if (path.startsWith('/users/') && request.method === 'PUT') {
      const userId = path.split('/')[2];
      const { name } = await request.json<{ name: string }>();
      
      const result = await env.DB.prepare(
        'UPDATE users SET name = ? WHERE id = ?'
      )
      .bind(name, userId)
      .run();
      
      if (result.meta.changes === 0) {
        return new Response('User not found', { status: 404 });
      }
      
      return Response.json({ success: true });
    }
    
    // DELETE
    if (path.startsWith('/users/') && request.method === 'DELETE') {
      const userId = path.split('/')[2];
      
      const result = await env.DB.prepare(
        'DELETE FROM users WHERE id = ?'
      )
      .bind(userId)
      .run();
      
      if (result.meta.changes === 0) {
        return new Response('User not found', { status: 404 });
      }
      
      return Response.json({ success: true });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Transactions

```typescript
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { fromUserId, toUserId, amount } = await request.json<{
      fromUserId: number;
      toUserId: number;
      amount: number;
    }>();
    
    try {
      // Execute multiple statements in a transaction
      const results = await env.DB.batch([
        env.DB.prepare('UPDATE accounts SET balance = balance - ? WHERE user_id = ?')
          .bind(amount, fromUserId),
        env.DB.prepare('UPDATE accounts SET balance = balance + ? WHERE user_id = ?')
          .bind(amount, toUserId),
        env.DB.prepare('INSERT INTO transactions (from_user, to_user, amount) VALUES (?, ?, ?)')
          .bind(fromUserId, toUserId, amount)
      ]);
      
      // Check if all operations succeeded
      const allSucceeded = results.every(r => r.success);
      
      if (!allSucceeded) {
        return Response.json(
          { error: 'Transaction failed' },
          { status: 500 }
        );
      }
      
      return Response.json({
        success: true,
        transactionId: results[2].meta.last_row_id
      });
    } catch (error: any) {
      return Response.json(
        { error: error.message },
        { status: 500 }
      );
    }
  }
};
```

### Complex Queries

```typescript
interface Env {
  DB: D1Database;
}

interface PostWithAuthor {
  id: number;
  title: string;
  content: string;
  author_name: string;
  author_email: string;
  created_at: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // JOIN query
    if (url.pathname === '/posts') {
      const { results } = await env.DB.prepare(`
        SELECT 
          p.id,
          p.title,
          p.content,
          p.created_at,
          u.name as author_name,
          u.email as author_email
        FROM posts p
        INNER JOIN users u ON p.user_id = u.id
        WHERE p.published = 1
        ORDER BY p.created_at DESC
        LIMIT 20
      `).all<PostWithAuthor>();
      
      return Response.json(results);
    }
    
    // Aggregation query
    if (url.pathname === '/stats') {
      const stats = await env.DB.prepare(`
        SELECT 
          COUNT(*) as total_posts,
          COUNT(DISTINCT user_id) as total_authors,
          AVG(LENGTH(content)) as avg_content_length
        FROM posts
        WHERE published = 1
      `).first<{
        total_posts: number;
        total_authors: number;
        avg_content_length: number;
      }>();
      
      return Response.json(stats);
    }
    
    // Search with LIKE
    if (url.pathname === '/search') {
      const query = url.searchParams.get('q') || '';
      
      const { results } = await env.DB.prepare(`
        SELECT 
          p.*,
          u.name as author_name
        FROM posts p
        INNER JOIN users u ON p.user_id = u.id
        WHERE 
          p.title LIKE ? OR
          p.content LIKE ?
        ORDER BY p.created_at DESC
        LIMIT 50
      `)
      .bind(`%${query}%`, `%${query}%`)
      .all();
      
      return Response.json(results);
    }
    
    // Grouped data
    if (url.pathname === '/posts-by-author') {
      const { results } = await env.DB.prepare(`
        SELECT 
          u.id,
          u.name,
          u.email,
          COUNT(p.id) as post_count,
          MAX(p.created_at) as last_post_date
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        GROUP BY u.id, u.name, u.email
        HAVING post_count > 0
        ORDER BY post_count DESC
      `).all();
      
      return Response.json(results);
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Prepared Statements

```typescript
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Using bind() for parameterized queries (prevents SQL injection)
    const email = 'user@example.com';
    
    // ✅ GOOD: Parameterized query
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE email = ?'
    )
    .bind(email)
    .first();
    
    // ❌ BAD: String concatenation (SQL injection risk!)
    // const user = await env.DB.prepare(
    //   `SELECT * FROM users WHERE email = '${email}'`
    // ).first();
    
    // Multiple parameters
    const posts = await env.DB.prepare(
      'SELECT * FROM posts WHERE user_id = ? AND published = ? ORDER BY created_at DESC LIMIT ?'
    )
    .bind(user.id, 1, 10)
    .all();
    
    return Response.json({
      user,
      posts: posts.results
    });
  }
};
```

### Pagination

```typescript
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1'));
    const perPage = Math.min(100, parseInt(url.searchParams.get('per_page') || '20'));
    const offset = (page - 1) * perPage;
    
    // Get total count
    const countResult = await env.DB.prepare(
      'SELECT COUNT(*) as total FROM posts WHERE published = 1'
    ).first<{ total: number }>();
    
    const total = countResult?.total || 0;
    const totalPages = Math.ceil(total / perPage);
    
    // Get page data
    const { results } = await env.DB.prepare(`
      SELECT 
        p.*,
        u.name as author_name
      FROM posts p
      INNER JOIN users u ON p.user_id = u.id
      WHERE p.published = 1
      ORDER BY p.created_at DESC
      LIMIT ? OFFSET ?
    `)
    .bind(perPage, offset)
    .all();
    
    return Response.json({
      data: results,
      pagination: {
        page,
        perPage,
        total,
        totalPages,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });
  }
};
```

## Common Use Cases

### User Authentication System

```typescript
import { hash, compare } from 'bcrypt';

interface Env {
  DB: D1Database;
  JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Register
    if (url.pathname === '/auth/register' && request.method === 'POST') {
      const { email, password, name } = await request.json<{
        email: string;
        password: string;
        name: string;
      }>();
      
      // Hash password
      const passwordHash = await hash(password, 10);
      
      try {
        const result = await env.DB.prepare(`
          INSERT INTO users (email, password_hash, name)
          VALUES (?, ?, ?)
        `)
        .bind(email, passwordHash, name)
        .run();
        
        return Response.json({
          success: true,
          userId: result.meta.last_row_id
        });
      } catch (error: any) {
        if (error.message.includes('UNIQUE constraint')) {
          return Response.json(
            { error: 'Email already exists' },
            { status: 409 }
          );
        }
        throw error;
      }
    }
    
    // Login
    if (url.pathname === '/auth/login' && request.method === 'POST') {
      const { email, password } = await request.json<{
        email: string;
        password: string;
      }>();
      
      const user = await env.DB.prepare(
        'SELECT id, email, password_hash, name FROM users WHERE email = ?'
      )
      .bind(email)
      .first<{
        id: number;
        email: string;
        password_hash: string;
        name: string;
      }>();
      
      if (!user) {
        return Response.json(
          { error: 'Invalid credentials' },
          { status: 401 }
        );
      }
      
      const valid = await compare(password, user.password_hash);
      
      if (!valid) {
        return Response.json(
          { error: 'Invalid credentials' },
          { status: 401 }
        );
      }
      
      // Update last login
      await env.DB.prepare(
        'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?'
      )
      .bind(user.id)
      .run();
      
      return Response.json({
        user: {
          id: user.id,
          email: user.email,
          name: user.name
        }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Blog with Comments

```typescript
interface Env {
  DB: D1Database;
}

interface Comment {
  id: number;
  post_id: number;
  author_name: string;
  content: string;
  created_at: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Get post with comments
    if (url.pathname.startsWith('/posts/')) {
      const postId = url.pathname.split('/')[2];
      
      // Get post
      const post = await env.DB.prepare(
        'SELECT p.*, u.name as author_name FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = ?'
      )
      .bind(postId)
      .first();
      
      if (!post) {
        return new Response('Post not found', { status: 404 });
      }
      
      // Get comments
      const { results: comments } = await env.DB.prepare(
        'SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC'
      )
      .bind(postId)
      .all<Comment>();
      
      return Response.json({
        ...post,
        comments
      });
    }
    
    // Add comment
    if (url.pathname === '/comments' && request.method === 'POST') {
      const { postId, authorName, content } = await request.json<{
        postId: number;
        authorName: string;
        content: string;
      }>();
      
      const result = await env.DB.prepare(
        'INSERT INTO comments (post_id, author_name, content) VALUES (?, ?, ?)'
      )
      .bind(postId, authorName, content)
      .run();
      
      return Response.json({
        success: true,
        commentId: result.meta.last_row_id
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Analytics Dashboard

```typescript
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/analytics') {
      // Daily active users (last 30 days)
      const { results: dailyActiveUsers } = await env.DB.prepare(`
        SELECT 
          DATE(created_at) as date,
          COUNT(DISTINCT user_id) as active_users
        FROM page_views
        WHERE created_at >= DATE('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
      `).all();
      
      // Top pages
      const { results: topPages } = await env.DB.prepare(`
        SELECT 
          page_url,
          COUNT(*) as views,
          COUNT(DISTINCT user_id) as unique_visitors
        FROM page_views
        WHERE created_at >= DATE('now', '-7 days')
        GROUP BY page_url
        ORDER BY views DESC
        LIMIT 10
      `).all();
      
      // User retention
      const retention = await env.DB.prepare(`
        SELECT 
          COUNT(DISTINCT CASE WHEN days_since_signup <= 1 THEN user_id END) as day_1,
          COUNT(DISTINCT CASE WHEN days_since_signup <= 7 THEN user_id END) as day_7,
          COUNT(DISTINCT CASE WHEN days_since_signup <= 30 THEN user_id END) as day_30
        FROM (
          SELECT 
            user_id,
            JULIANDAY('now') - JULIANDAY(created_at) as days_since_signup
          FROM users
        )
      `).first();
      
      return Response.json({
        dailyActiveUsers,
        topPages,
        retention
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

## Integration

### Schema Migrations

```sql
-- migrations/0001_create_users.sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_login DATETIME
);

CREATE INDEX idx_users_email ON users(email);
```

```sql
-- migrations/0002_create_posts.sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_slug ON posts(slug);
CREATE INDEX idx_posts_published ON posts(published);
```

```sql
-- migrations/0003_create_comments.sql
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  author_name TEXT NOT NULL,
  content TEXT NOT NULL,
  approved BOOLEAN DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE INDEX idx_comments_post_id ON comments(post_id);
```

```bash
# Apply migrations
wrangler d1 migrations apply my-database --local
wrangler d1 migrations apply my-database --remote
```

### Local Development

```bash
# Start local D1 instance
wrangler dev --local

# Execute SQL directly
wrangler d1 execute my-database --local --command="SELECT * FROM users"

# Execute SQL file
wrangler d1 execute my-database --local --file=./seed.sql
```

### Testing with Mock Data

```typescript
// test/setup.ts
import { D1Database } from '@cloudflare/workers-types';

async function seedDatabase(db: D1Database): Promise<void> {
  // Seed users
  await db.batch([
    db.prepare('INSERT INTO users (email, name) VALUES (?, ?)').bind('alice@example.com', 'Alice'),
    db.prepare('INSERT INTO users (email, name) VALUES (?, ?)').bind('bob@example.com', 'Bob')
  ]);
  
  // Seed posts
  await db.prepare(
    'INSERT INTO posts (user_id, title, content, published) VALUES (?, ?, ?, ?)'
  )
  .bind(1, 'First Post', 'Hello World!', 1)
  .run();
}
```

## Best Practices

1. **Use migrations**: Version control your schema changes
2. **Add indexes**: Index columns used in WHERE, JOIN, and ORDER BY
3. **Parameterize queries**: Always use .bind() to prevent SQL injection
4. **Batch operations**: Use .batch() for multiple statements
5. **Handle errors**: Check .success and wrap in try/catch
6. **Limit result sets**: Always use LIMIT to prevent excessive data transfer
7. **Normalize data**: Follow database normalization principles
8. **Use foreign keys**: Maintain referential integrity
9. **Add timestamps**: Track created_at and updated_at
10. **Test locally**: Use --local flag during development

## Troubleshooting

### Migration errors

```bash
# List applied migrations
wrangler d1 migrations list my-database --local
wrangler d1 migrations list my-database --remote

# If migration fails, fix SQL and reapply
# Edit migration file, then:
wrangler d1 migrations apply my-database --local
```

### Query performance

```sql
-- Use EXPLAIN QUERY PLAN to debug slow queries
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE user_id = 1;

-- Add indexes for commonly queried columns
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Avoid SELECT * - specify columns
SELECT id, title FROM posts WHERE published = 1;
```

### Binding issues

```typescript
// Ensure env interface matches wrangler.toml
interface Env {
  DB: D1Database;  // Matches binding = "DB"
}

// Check wrangler.toml has correct binding
// [[d1_databases]]
// binding = "DB"
// database_name = "my-database"
// database_id = "your-database-id"
```

### Data type handling

```typescript
// SQLite has dynamic typing - be explicit
const user = await env.DB.prepare(
  'SELECT id, email, created_at FROM users WHERE id = ?'
)
.bind(userId)
.first<{
  id: number;
  email: string;
  created_at: string;  // Dates are returned as strings
}>();

// Convert date strings if needed
if (user) {
  const createdDate = new Date(user.created_at);
}
```

## See Also

- [Cloudflare Workers](cloudflare-workers.md) - Runtime for D1 queries
- [Cloudflare KV](cloudflare-kv.md) - Alternative for simple key-value data
- [Cloudflare R2](cloudflare-r2.md) - Object storage for file data
- [Cloudflare Pages](cloudflare-pages.md) - Frontend with D1 backend
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **SQL Tutorial**: https://www.sqltutorial.org/
