---
name: Cloudflare Durable Objects
description: >
  Manages Cloudflare Durable Objects for strongly consistent stateful coordination, real-time applications, distributed counters, locks, and transactional storage with WebSocket support. 
  Invoke when asked to create stateful Workers, build real-time apps, implement distributed coordination, manage WebSocket connections, create counters or locks, handle transactional storage, or build collaborative applications with Cloudflare.
license: MIT
---

# Cloudflare Durable Objects

Cloudflare Durable Objects provide low-latency coordination and consistent storage for Cloudflare Workers. Each Durable Object is a single-threaded, strongly consistent instance that can maintain state and handle WebSocket connections, making them ideal for real-time applications, distributed coordination, and stateful workflows.

## When to Use

Use Cloudflare Durable Objects when you need:

- **Stateful Coordination**: Distributed locks, leader election, or coordination primitives
- **Real-Time Applications**: Chat apps, collaborative editing, live cursors, multiplayer games
- **Consistent Counters**: Rate limiting, analytics, inventory management
- **WebSocket Management**: Long-lived connections with state persistence
- **Transactional Storage**: ACID-like guarantees for small datasets
- **Session Management**: User sessions with strong consistency
- **Queue Coordination**: Job queues, task distribution, workflow orchestration
- **Cache with Coordination**: Distributed caching with invalidation logic

**Don't use** for large-scale data storage (use R2 or KV), simple stateless functions (use Workers), or traditional databases (use D1 or external databases).

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/durable-objects/
- **API Reference**: https://developers.cloudflare.com/durable-objects/api/
- **Best Practices**: https://developers.cloudflare.com/durable-objects/best-practices/
- **Examples**: https://developers.cloudflare.com/durable-objects/examples/
- **Pricing**: https://developers.cloudflare.com/durable-objects/platform/pricing/
- **Limits**: https://developers.cloudflare.com/durable-objects/platform/limits/
- **WebSockets**: https://developers.cloudflare.com/durable-objects/examples/websocket-server/
- **Transactional Storage API**: https://developers.cloudflare.com/durable-objects/api/transactional-storage-api/
- **Alarms**: https://developers.cloudflare.com/durable-objects/api/alarms/
- **Migrations**: https://developers.cloudflare.com/durable-objects/reference/data-migration/

## Quick Start

### Step 1: Enable Durable Objects

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create a new Workers project
wrangler init my-durable-app
cd my-durable-app
```

### Step 2: Define a Durable Object Class

```javascript
// src/index.js
export class Counter {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    // Get current value
    let value = (await this.state.storage.get('value')) || 0;
    
    const url = new URL(request.url);
    
    switch (url.pathname) {
      case '/increment':
        value++;
        await this.state.storage.put('value', value);
        return new Response(value.toString());
      
      case '/decrement':
        value--;
        await this.state.storage.put('value', value);
        return new Response(value.toString());
      
      case '/get':
        return new Response(value.toString());
      
      default:
        return new Response('Not found', { status: 404 });
    }
  }
}

// Worker script to access Durable Object
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const id = env.COUNTER.idFromName('global-counter');
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  }
};
```

### Step 3: Configure wrangler.toml

```toml
name = "my-durable-app"
main = "src/index.js"
compatibility_date = "2024-01-01"

[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "my-durable-app"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

### Step 4: Deploy

```bash
# Deploy to Cloudflare
wrangler deploy

# Test the deployment
curl https://my-durable-app.workers.dev/increment
curl https://my-durable-app.workers.dev/get
```

## Core Features

### 1. Transactional Storage API

Durable Objects provide a key-value storage API with atomic operations:

```javascript
export class DataStore {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    const { method, url: urlStr } = request;
    const url = new URL(urlStr);

    // Single operations
    if (method === 'GET') {
      const value = await this.state.storage.get(url.pathname.slice(1));
      return new Response(JSON.stringify({ value }));
    }

    if (method === 'PUT') {
      const data = await request.json();
      await this.state.storage.put(data.key, data.value);
      return new Response('OK');
    }

    if (method === 'DELETE') {
      await this.state.storage.delete(url.pathname.slice(1));
      return new Response('Deleted');
    }

    // Batch operations
    if (url.pathname === '/batch') {
      const items = await request.json();
      const entries = Object.entries(items);
      await this.state.storage.put(Object.fromEntries(entries));
      return new Response('Batch saved');
    }

    // List all keys
    if (url.pathname === '/list') {
      const map = await this.state.storage.list();
      const result = Object.fromEntries(map);
      return new Response(JSON.stringify(result));
    }

    // Transactions
    if (url.pathname === '/transaction') {
      await this.state.storage.transaction(async (txn) => {
        const count = (await txn.get('count')) || 0;
        await txn.put('count', count + 1);
        await txn.put('lastUpdate', Date.now());
      });
      return new Response('Transaction complete');
    }

    return new Response('Method not allowed', { status: 405 });
  }
}
```

### 2. WebSocket Server

Build real-time applications with WebSocket support:

```javascript
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.sessions = [];
  }

  async fetch(request) {
    // Handle WebSocket upgrade
    if (request.headers.get('Upgrade') === 'websocket') {
      const pair = new WebSocketPair();
      await this.handleSession(pair[1]);
      return new Response(null, {
        status: 101,
        webSocket: pair[0],
      });
    }

    // HTTP endpoints
    const url = new URL(request.url);
    if (url.pathname === '/count') {
      return new Response(this.sessions.length.toString());
    }

    return new Response('Expected WebSocket', { status: 400 });
  }

  async handleSession(webSocket) {
    webSocket.accept();
    
    const session = { webSocket, quit: false };
    this.sessions.push(session);

    webSocket.addEventListener('message', async (msg) => {
      try {
        const data = JSON.parse(msg.data);
        
        // Broadcast to all sessions
        this.broadcast(JSON.stringify({
          type: 'message',
          text: data.text,
          timestamp: Date.now(),
        }));

        // Save message history
        const messages = (await this.state.storage.get('messages')) || [];
        messages.push({ text: data.text, timestamp: Date.now() });
        await this.state.storage.put('messages', messages.slice(-100));
      } catch (err) {
        webSocket.send(JSON.stringify({ error: err.message }));
      }
    });

    webSocket.addEventListener('close', () => {
      session.quit = true;
      this.sessions = this.sessions.filter((s) => s !== session);
    });

    webSocket.addEventListener('error', () => {
      session.quit = true;
      this.sessions = this.sessions.filter((s) => s !== session);
    });

    // Send message history
    const messages = (await this.state.storage.get('messages')) || [];
    webSocket.send(JSON.stringify({
      type: 'history',
      messages,
    }));
  }

  broadcast(message) {
    this.sessions = this.sessions.filter((session) => {
      if (session.quit) return false;
      try {
        session.webSocket.send(message);
        return true;
      } catch (err) {
        session.quit = true;
        return false;
      }
    });
  }
}
```

### 3. Alarms for Scheduled Execution

Set alarms to execute code at specific times:

```javascript
export class ScheduledTask {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === '/schedule') {
      // Schedule an alarm 60 seconds from now
      const currentAlarm = await this.state.storage.getAlarm();
      if (currentAlarm == null) {
        await this.state.storage.setAlarm(Date.now() + 60000);
      }
      return new Response('Alarm scheduled');
    }

    if (url.pathname === '/cancel') {
      await this.state.storage.deleteAlarm();
      return new Response('Alarm cancelled');
    }

    return new Response('OK');
  }

  async alarm() {
    // This method is called when the alarm triggers
    console.log('Alarm triggered!');
    
    // Perform scheduled task
    const count = (await this.state.storage.get('executions')) || 0;
    await this.state.storage.put('executions', count + 1);
    
    // Optionally reschedule
    await this.state.storage.setAlarm(Date.now() + 60000);
  }
}
```

### 4. Distributed Locking

Implement distributed locks for coordination:

```javascript
export class DistributedLock {
  constructor(state, env) {
    this.state = state;
    this.locks = new Map();
  }

  async fetch(request) {
    const { method } = request;
    const url = new URL(request.url);
    const lockName = url.searchParams.get('name');
    const timeout = parseInt(url.searchParams.get('timeout') || '30000');

    if (method === 'POST' && url.pathname === '/acquire') {
      return await this.acquireLock(lockName, timeout);
    }

    if (method === 'POST' && url.pathname === '/release') {
      return await this.releaseLock(lockName);
    }

    if (method === 'GET' && url.pathname === '/status') {
      const locked = this.locks.has(lockName);
      return new Response(JSON.stringify({ locked }));
    }

    return new Response('Not found', { status: 404 });
  }

  async acquireLock(name, timeout) {
    if (this.locks.has(name)) {
      return new Response(JSON.stringify({ acquired: false }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const lockId = crypto.randomUUID();
    this.locks.set(name, {
      id: lockId,
      acquiredAt: Date.now(),
    });

    // Set auto-release alarm
    const expiryTime = Date.now() + timeout;
    await this.state.storage.put(`lock:${name}:expiry`, expiryTime);

    return new Response(JSON.stringify({ acquired: true, lockId }), {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  async releaseLock(name) {
    if (this.locks.has(name)) {
      this.locks.delete(name);
      await this.state.storage.delete(`lock:${name}:expiry`);
      return new Response(JSON.stringify({ released: true }));
    }
    return new Response(JSON.stringify({ released: false }), {
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
```

## Common Use Cases

### Real-Time Collaboration

```javascript
export class CollaborativeDoc {
  constructor(state, env) {
    this.state = state;
    this.sessions = new Map();
  }

  async fetch(request) {
    if (request.headers.get('Upgrade') !== 'websocket') {
      return new Response('Expected WebSocket', { status: 400 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    await this.handleSession(server, request);

    return new Response(null, {
      status: 101,
      webSocket: client,
    });
  }

  async handleSession(webSocket, request) {
    webSocket.accept();

    const url = new URL(request.url);
    const userId = url.searchParams.get('userId') || 'anonymous';
    const sessionId = crypto.randomUUID();

    this.sessions.set(sessionId, { webSocket, userId });

    // Send current document state
    const doc = await this.state.storage.get('document') || { content: '' };
    webSocket.send(JSON.stringify({
      type: 'init',
      document: doc,
      users: Array.from(this.sessions.values()).map(s => s.userId),
    }));

    // Broadcast new user joined
    this.broadcast({
      type: 'user-joined',
      userId,
    }, sessionId);

    webSocket.addEventListener('message', async (msg) => {
      const data = JSON.parse(msg.data);

      if (data.type === 'edit') {
        // Apply operational transform or CRDT here
        const doc = await this.state.storage.get('document') || { content: '' };
        doc.content = data.content;
        doc.version = (doc.version || 0) + 1;
        await this.state.storage.put('document', doc);

        // Broadcast change to all clients
        this.broadcast({
          type: 'edit',
          userId,
          content: data.content,
          version: doc.version,
        }, sessionId);
      }

      if (data.type === 'cursor') {
        this.broadcast({
          type: 'cursor',
          userId,
          position: data.position,
        }, sessionId);
      }
    });

    webSocket.addEventListener('close', () => {
      this.sessions.delete(sessionId);
      this.broadcast({
        type: 'user-left',
        userId,
      });
    });
  }

  broadcast(message, excludeSessionId = null) {
    const payload = JSON.stringify(message);
    for (const [sessionId, session] of this.sessions.entries()) {
      if (sessionId !== excludeSessionId) {
        try {
          session.webSocket.send(payload);
        } catch (err) {
          this.sessions.delete(sessionId);
        }
      }
    }
  }
}
```

### Rate Limiting with Sliding Window

```javascript
export class RateLimiter {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    const url = new URL(request.url);
    const key = url.searchParams.get('key');
    const limit = parseInt(url.searchParams.get('limit') || '10');
    const windowMs = parseInt(url.searchParams.get('window') || '60000');

    const now = Date.now();
    const windowStart = now - windowMs;

    // Get request timestamps
    const timestamps = (await this.state.storage.get(key)) || [];
    
    // Remove old timestamps outside the window
    const validTimestamps = timestamps.filter(ts => ts > windowStart);
    
    // Check if limit exceeded
    if (validTimestamps.length >= limit) {
      const oldestTimestamp = validTimestamps[0];
      const retryAfter = Math.ceil((oldestTimestamp + windowMs - now) / 1000);
      
      return new Response(JSON.stringify({
        allowed: false,
        retryAfter,
        current: validTimestamps.length,
        limit,
      }), {
        status: 429,
        headers: {
          'Content-Type': 'application/json',
          'Retry-After': retryAfter.toString(),
        },
      });
    }

    // Add current timestamp
    validTimestamps.push(now);
    await this.state.storage.put(key, validTimestamps);

    return new Response(JSON.stringify({
      allowed: true,
      current: validTimestamps.length,
      limit,
      remaining: limit - validTimestamps.length,
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
```

### Leader Election

```javascript
export class LeaderElection {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    const url = new URL(request.url);
    const nodeId = url.searchParams.get('nodeId');

    if (url.pathname === '/elect') {
      return await this.electLeader(nodeId);
    }

    if (url.pathname === '/leader') {
      const leader = await this.state.storage.get('leader');
      return new Response(JSON.stringify({ leader }));
    }

    if (url.pathname === '/heartbeat') {
      return await this.heartbeat(nodeId);
    }

    return new Response('Not found', { status: 404 });
  }

  async electLeader(nodeId) {
    const leader = await this.state.storage.get('leader');
    const leaderHeartbeat = await this.state.storage.get('leaderHeartbeat');
    const now = Date.now();

    // If no leader or leader expired (no heartbeat in 30 seconds)
    if (!leader || !leaderHeartbeat || now - leaderHeartbeat > 30000) {
      await this.state.storage.put('leader', nodeId);
      await this.state.storage.put('leaderHeartbeat', now);
      return new Response(JSON.stringify({ 
        elected: true, 
        leader: nodeId 
      }));
    }

    return new Response(JSON.stringify({ 
      elected: false, 
      leader 
    }));
  }

  async heartbeat(nodeId) {
    const leader = await this.state.storage.get('leader');
    
    if (leader === nodeId) {
      await this.state.storage.put('leaderHeartbeat', Date.now());
      return new Response(JSON.stringify({ success: true }));
    }

    return new Response(JSON.stringify({ success: false }), { 
      status: 403 
    });
  }
}
```

## Integration

### Using with Workers

```javascript
// Main worker that uses Durable Objects
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Get or create a Durable Object
    const id = env.MY_DURABLE_OBJECT.idFromName('singleton');
    const stub = env.MY_DURABLE_OBJECT.get(id);
    
    // Forward request to Durable Object
    return stub.fetch(request);
  }
};
```

### ID Generation Strategies

```javascript
// Named ID - same name always returns same object
const id = env.MY_DO.idFromName('user-123');

// Random ID - creates new object
const id = env.MY_DO.newUniqueId();

// From string (deterministic)
const id = env.MY_DO.idFromString(hexId);

// Derived from user input
const userId = '12345';
const id = env.MY_DO.idFromName(`user:${userId}`);

// Sharding pattern
const shard = hashCode(key) % 10;
const id = env.MY_DO.idFromName(`shard:${shard}`);
```

### Using with D1 Database

```javascript
export class UserSession {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    const url = new URL(request.url);
    const userId = url.searchParams.get('userId');

    // Use Durable Object for session state
    const session = await this.state.storage.get('session') || {};

    // Use D1 for persistent data
    const user = await this.env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(userId).first();

    return new Response(JSON.stringify({ session, user }));
  }
}
```

## Best Practices

### 1. Minimize Object Creation

```javascript
// Good: Use named IDs for logical partitions
const roomId = 'chat-room-123';
const id = env.CHAT_ROOM.idFromName(roomId);

// Avoid: Creating too many random IDs
// const id = env.CHAT_ROOM.newUniqueId(); // Creates billing for each
```

### 2. Handle Errors Gracefully

```javascript
export class ResilientDO {
  async fetch(request) {
    try {
      const data = await this.state.storage.get('key');
      return new Response(JSON.stringify(data));
    } catch (err) {
      console.error('Storage error:', err);
      return new Response('Service unavailable', { status: 503 });
    }
  }
}
```

### 3. Use Transactions for Consistency

```javascript
// Good: Atomic updates
await this.state.storage.transaction(async (txn) => {
  const balance = await txn.get('balance') || 0;
  await txn.put('balance', balance - amount);
  await txn.put('lastTransaction', Date.now());
});

// Avoid: Non-atomic operations
const balance = await this.state.storage.get('balance');
await this.state.storage.put('balance', balance - amount);
```

### 4. Clean Up WebSocket Sessions

```javascript
async handleSession(webSocket) {
  webSocket.accept();
  
  const session = { 
    webSocket, 
    lastActivity: Date.now() 
  };
  
  this.sessions.push(session);

  // Periodic cleanup of idle sessions
  setInterval(() => {
    const timeout = 5 * 60 * 1000; // 5 minutes
    this.sessions = this.sessions.filter(s => {
      if (Date.now() - s.lastActivity > timeout) {
        s.webSocket.close();
        return false;
      }
      return true;
    });
  }, 60000);
}
```

### 5. Optimize Storage Operations

```javascript
// Good: Batch operations
await this.state.storage.put({
  'key1': value1,
  'key2': value2,
  'key3': value3,
});

// Avoid: Multiple single operations
await this.state.storage.put('key1', value1);
await this.state.storage.put('key2', value2);
await this.state.storage.put('key3', value3);
```

## Troubleshooting

### Common Issues

**Issue**: Object not persisting data
```javascript
// Problem: Not awaiting storage operations
this.state.storage.put('key', value); // Missing await

// Solution: Always await
await this.state.storage.put('key', value);
```

**Issue**: WebSocket connection drops
```javascript
// Solution: Implement heartbeat
setInterval(() => {
  for (const session of this.sessions) {
    session.webSocket.send(JSON.stringify({ type: 'ping' }));
  }
}, 30000);
```

**Issue**: High costs from too many objects
```javascript
// Problem: Creating unique ID for each request
const id = env.MY_DO.newUniqueId();

// Solution: Use named IDs with logical partitioning
const userId = getUserId(request);
const id = env.MY_DO.idFromName(`user:${userId}`);
```

**Issue**: Hitting storage limits
```javascript
// Monitor storage size
const size = await this.state.storage.list();
console.log(`Storage keys: ${size.size}`);

// Implement cleanup
if (size.size > 1000) {
  const oldKeys = Array.from(size.keys()).slice(0, 100);
  await this.state.storage.delete(oldKeys);
}
```

### Debugging

```javascript
export class DebugDO {
  async fetch(request) {
    console.log('Request received:', request.url);
    
    try {
      const result = await this.processRequest(request);
      console.log('Success:', result);
      return new Response(JSON.stringify(result));
    } catch (err) {
      console.error('Error:', err.message, err.stack);
      return new Response(err.message, { status: 500 });
    }
  }
}
```

## See Also

- **Cloudflare Workers**: https://developers.cloudflare.com/workers/
- **Workers KV**: https://developers.cloudflare.com/kv/
- **R2 Storage**: https://developers.cloudflare.com/r2/
- **D1 Database**: https://developers.cloudflare.com/d1/
- **Queues**: https://developers.cloudflare.com/queues/
- **Wrangler CLI**: https://developers.cloudflare.com/workers/wrangler/
