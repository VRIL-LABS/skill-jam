---
name: Cloudflare Queues
description: |
  Cloudflare Queues is a global message queuing service for reliable background job processing.
  Trigger phrases: "message queue", "background jobs", "async processing", "job queues", "task queues", "cloudflare queues"
license: MIT
---

# Cloudflare Queues

Cloudflare Queues is a global message queuing service that enables asynchronous communication between your Cloudflare Workers. It provides guaranteed message delivery, automatic retries, and seamless integration with the Workers platform for building scalable, event-driven applications.

## When to Use

Use Cloudflare Queues when you need to:
- **Offload heavy processing**: Move time-consuming tasks out of request/response cycles
- **Decouple services**: Enable independent scaling and reliability between producers and consumers
- **Batch operations**: Collect and process multiple messages together for efficiency
- **Guarantee delivery**: Ensure critical tasks are completed even if initial attempts fail
- **Handle traffic spikes**: Buffer incoming work to smooth out processing load
- **Build event-driven systems**: Create reactive architectures with asynchronous workflows
- **Schedule background jobs**: Process tasks that don't need immediate completion
- **Implement retry logic**: Automatically retry failed operations with backoff

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/queues/
- **Get Started Guide**: https://developers.cloudflare.com/queues/get-started/
- **Configuration Reference**: https://developers.cloudflare.com/queues/configuration/
- **JavaScript APIs**: https://developers.cloudflare.com/queues/javascript-apis/
- **Limits**: https://developers.cloudflare.com/queues/platform/limits/
- **Pricing**: https://developers.cloudflare.com/queues/platform/pricing/

## Quick Start

### 1. Create a Queue

Using Wrangler CLI:

```bash
# Create a new queue
npx wrangler queues create my-queue

# List existing queues
npx wrangler queues list

# Delete a queue
npx wrangler queues delete my-queue
```

### 2. Configure Producer Worker

Update `wrangler.toml`:

```toml
name = "queue-producer"
main = "src/producer.js"
compatibility_date = "2024-01-01"

[[queues.producers]]
queue = "my-queue"
binding = "MY_QUEUE"
```

### 3. Write Producer Code

```javascript
// src/producer.js
export default {
  async fetch(request, env) {
    // Send a message to the queue
    await env.MY_QUEUE.send({
      url: request.url,
      timestamp: Date.now(),
      headers: Object.fromEntries(request.headers),
    });

    return new Response('Message queued successfully', { status: 202 });
  },
};
```

### 4. Configure Consumer Worker

Update `wrangler.toml`:

```toml
name = "queue-consumer"
main = "src/consumer.js"
compatibility_date = "2024-01-01"

[[queues.consumers]]
queue = "my-queue"
max_batch_size = 10
max_batch_timeout = 5
max_retries = 3
dead_letter_queue = "my-dlq"
```

### 5. Write Consumer Code

```javascript
// src/consumer.js
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      console.log('Processing message:', message.id);
      console.log('Message body:', message.body);
      
      try {
        // Process the message
        await processMessage(message.body);
        
        // Acknowledge successful processing
        message.ack();
      } catch (error) {
        console.error('Error processing message:', error);
        
        // Retry the message
        message.retry();
      }
    }
  },
};

async function processMessage(data) {
  // Your processing logic here
  console.log('Processing:', data);
}
```

### 6. Deploy

```bash
# Deploy producer
npx wrangler deploy --config wrangler-producer.toml

# Deploy consumer
npx wrangler deploy --config wrangler-consumer.toml
```

## Core Features

### Message Operations

#### Sending Single Messages

```javascript
export default {
  async fetch(request, env) {
    const message = {
      orderId: '12345',
      action: 'send-email',
      email: 'customer@example.com',
    };

    await env.MY_QUEUE.send(message);
    
    return new Response('Message sent');
  },
};
```

#### Sending Batch Messages

```javascript
export default {
  async fetch(request, env) {
    const messages = [
      { userId: 1, action: 'update-profile' },
      { userId: 2, action: 'send-notification' },
      { userId: 3, action: 'process-payment' },
    ];

    await env.MY_QUEUE.sendBatch(messages);
    
    return new Response(`${messages.length} messages sent`);
  },
};
```

#### Message with Options

```javascript
await env.MY_QUEUE.send(
  { data: 'important-task' },
  {
    contentType: 'json',
    delaySeconds: 60, // Delay delivery by 60 seconds
  }
);
```

### Consumer Patterns

#### Basic Consumer

```javascript
export default {
  async queue(batch, env) {
    console.log(`Processing ${batch.messages.length} messages`);
    
    for (const message of batch.messages) {
      await handleMessage(message.body, env);
      message.ack();
    }
  },
};
```

#### Batch Processing

```javascript
export default {
  async queue(batch, env) {
    // Process all messages at once
    const bodies = batch.messages.map(m => m.body);
    
    try {
      await processBatch(bodies, env);
      
      // Acknowledge all messages
      batch.ackAll();
    } catch (error) {
      console.error('Batch processing failed:', error);
      
      // Retry all messages
      batch.retryAll();
    }
  },
};

async function processBatch(items, env) {
  // Batch insert to database, bulk API call, etc.
  await env.DB.prepare('INSERT INTO items VALUES (?)').bind(items).run();
}
```

#### Selective Acknowledgment

```javascript
export default {
  async queue(batch, env) {
    const results = await Promise.allSettled(
      batch.messages.map(async (message) => {
        try {
          await processMessage(message.body);
          message.ack();
        } catch (error) {
          console.error(`Failed to process ${message.id}:`, error);
          message.retry({ delaySeconds: 30 });
        }
      })
    );
  },
};
```

#### Dead Letter Queue Handling

```javascript
// Consumer for DLQ
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      console.log('DLQ message:', message.id);
      console.log('Original body:', message.body);
      console.log('Retry count:', message.attempts);
      
      // Log to external monitoring
      await logFailedMessage(message, env);
      
      // Send alert
      await env.ALERTS.send({
        type: 'queue-failure',
        messageId: message.id,
        attempts: message.attempts,
      });
      
      message.ack();
    }
  },
};
```

### Advanced Patterns

#### Priority Queue Pattern

```javascript
// Use multiple queues for priority
export default {
  async fetch(request, env) {
    const task = await request.json();
    
    if (task.priority === 'high') {
      await env.HIGH_PRIORITY_QUEUE.send(task);
    } else if (task.priority === 'medium') {
      await env.MEDIUM_PRIORITY_QUEUE.send(task);
    } else {
      await env.LOW_PRIORITY_QUEUE.send(task);
    }
    
    return new Response('Task queued');
  },
};
```

#### Delayed Processing

```javascript
export default {
  async fetch(request, env) {
    const job = await request.json();
    
    // Schedule for 1 hour later
    await env.MY_QUEUE.send(job, {
      delaySeconds: 3600,
    });
    
    return new Response('Job scheduled');
  },
};
```

#### Fan-out Pattern

```javascript
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      const tasks = message.body.tasks;
      
      // Fan out to multiple queues
      await Promise.all([
        env.EMAIL_QUEUE.send({ type: 'email', data: tasks.email }),
        env.SMS_QUEUE.send({ type: 'sms', data: tasks.sms }),
        env.PUSH_QUEUE.send({ type: 'push', data: tasks.push }),
      ]);
      
      message.ack();
    }
  },
};
```

#### Aggregate Pattern

```javascript
export default {
  async queue(batch, env) {
    // Group messages by user
    const byUser = {};
    
    for (const message of batch.messages) {
      const userId = message.body.userId;
      if (!byUser[userId]) {
        byUser[userId] = [];
      }
      byUser[userId].push(message);
    }
    
    // Process aggregated data
    for (const [userId, messages] of Object.entries(byUser)) {
      await processUserMessages(userId, messages.map(m => m.body));
      messages.forEach(m => m.ack());
    }
  },
};
```

## Common Use Cases

### Email Processing

```javascript
// Producer: Queue email requests
export default {
  async fetch(request, env) {
    const { to, subject, body } = await request.json();
    
    await env.EMAIL_QUEUE.send({
      to,
      subject,
      body,
      timestamp: Date.now(),
    });
    
    return Response.json({ status: 'queued' });
  },
};

// Consumer: Send emails
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      const { to, subject, body } = message.body;
      
      try {
        await sendEmail(to, subject, body, env);
        message.ack();
      } catch (error) {
        console.error('Email failed:', error);
        message.retry();
      }
    }
  },
};

async function sendEmail(to, subject, body, env) {
  await fetch('https://api.mailgun.net/v3/domain/messages', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.MAILGUN_API_KEY}`,
    },
    body: JSON.stringify({ to, subject, text: body }),
  });
}
```

### Image Processing

```javascript
// Producer: Queue image processing tasks
export default {
  async fetch(request, env) {
    const { imageUrl, operations } = await request.json();
    
    await env.IMAGE_QUEUE.send({
      imageUrl,
      operations, // resize, crop, optimize
      callbackUrl: request.headers.get('X-Callback-URL'),
    });
    
    return Response.json({ status: 'processing' });
  },
};

// Consumer: Process images
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      const { imageUrl, operations, callbackUrl } = message.body;
      
      try {
        // Download image
        const image = await fetch(imageUrl).then(r => r.arrayBuffer());
        
        // Apply operations
        const processed = await applyOperations(image, operations);
        
        // Upload to R2
        const key = `processed/${Date.now()}.jpg`;
        await env.BUCKET.put(key, processed);
        
        // Callback
        if (callbackUrl) {
          await fetch(callbackUrl, {
            method: 'POST',
            body: JSON.stringify({ url: `https://cdn.example.com/${key}` }),
          });
        }
        
        message.ack();
      } catch (error) {
        console.error('Image processing failed:', error);
        message.retry();
      }
    }
  },
};
```

### Analytics Processing

```javascript
// Producer: Queue analytics events
export default {
  async fetch(request, env) {
    const event = await request.json();
    
    await env.ANALYTICS_QUEUE.send({
      ...event,
      timestamp: Date.now(),
      ip: request.headers.get('CF-Connecting-IP'),
    });
    
    return new Response(null, { status: 204 });
  },
};

// Consumer: Write to analytics database
export default {
  async queue(batch, env) {
    // Batch insert for efficiency
    const events = batch.messages.map(m => m.body);
    
    try {
      await env.DB.batch(
        events.map(event =>
          env.DB.prepare(
            'INSERT INTO events (type, user_id, data, timestamp) VALUES (?, ?, ?, ?)'
          ).bind(event.type, event.userId, JSON.stringify(event.data), event.timestamp)
        )
      );
      
      batch.ackAll();
    } catch (error) {
      console.error('Failed to insert events:', error);
      batch.retryAll();
    }
  },
};
```

### Order Processing

```javascript
// Producer: Queue orders
export default {
  async fetch(request, env) {
    const order = await request.json();
    
    // Validate order
    if (!order.items || order.items.length === 0) {
      return Response.json({ error: 'Invalid order' }, { status: 400 });
    }
    
    // Queue for processing
    await env.ORDER_QUEUE.send({
      orderId: crypto.randomUUID(),
      ...order,
      status: 'pending',
      createdAt: Date.now(),
    });
    
    return Response.json({ status: 'accepted' }, { status: 202 });
  },
};

// Consumer: Process orders
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      const order = message.body;
      
      try {
        // Update inventory
        await updateInventory(order.items, env);
        
        // Process payment
        await processPayment(order.payment, env);
        
        // Create shipment
        await createShipment(order, env);
        
        // Send confirmation
        await env.EMAIL_QUEUE.send({
          to: order.email,
          subject: `Order ${order.orderId} Confirmed`,
          template: 'order-confirmation',
          data: order,
        });
        
        message.ack();
      } catch (error) {
        console.error(`Order ${order.orderId} failed:`, error);
        message.retry({ delaySeconds: 60 });
      }
    }
  },
};
```

## Integration

### With Cloudflare Workers

```javascript
export default {
  async fetch(request, env, ctx) {
    // Process request
    const response = handleRequest(request);
    
    // Queue background task without blocking response
    ctx.waitUntil(
      env.MY_QUEUE.send({
        url: request.url,
        timestamp: Date.now(),
      })
    );
    
    return response;
  },
};
```

### With Durable Objects

```javascript
export class Counter {
  async fetch(request) {
    // Update state
    const count = await this.updateCount();
    
    // Queue notification when threshold reached
    if (count % 100 === 0) {
      await this.env.NOTIFICATIONS.send({
        type: 'milestone',
        count,
      });
    }
    
    return Response.json({ count });
  }
}
```

### With R2 Storage

```javascript
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      const { fileName, data } = message.body;
      
      try {
        // Store in R2
        await env.BUCKET.put(fileName, data, {
          httpMetadata: {
            contentType: 'application/json',
          },
        });
        
        message.ack();
      } catch (error) {
        message.retry();
      }
    }
  },
};
```

### With D1 Database

```javascript
export default {
  async queue(batch, env) {
    try {
      // Use transaction for batch insert
      const stmt = env.DB.prepare(
        'INSERT INTO jobs (id, data, status) VALUES (?, ?, ?)'
      );
      
      const batch_ops = batch.messages.map(m =>
        stmt.bind(m.id, JSON.stringify(m.body), 'completed')
      );
      
      await env.DB.batch(batch_ops);
      batch.ackAll();
    } catch (error) {
      batch.retryAll();
    }
  },
};
```

## Best Practices

### Message Design

```javascript
// Good: Structured message with all needed data
await env.MY_QUEUE.send({
  type: 'user-registered',
  userId: user.id,
  email: user.email,
  timestamp: Date.now(),
  metadata: {
    source: 'web',
    campaign: 'summer-2024',
  },
});

// Avoid: Minimal data requiring additional lookups
await env.MY_QUEUE.send({ userId: user.id }); // Consumer needs to fetch user data
```

### Error Handling

```javascript
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      try {
        await processMessage(message.body);
        message.ack();
      } catch (error) {
        // Log error with context
        console.error('Processing failed:', {
          messageId: message.id,
          attempt: message.attempts,
          error: error.message,
        });
        
        // Retry with exponential backoff
        const delay = Math.min(300, Math.pow(2, message.attempts) * 10);
        message.retry({ delaySeconds: delay });
      }
    }
  },
};
```

### Batch Size Optimization

```toml
# For high-throughput, low-latency processing
[[queues.consumers]]
queue = "fast-queue"
max_batch_size = 10
max_batch_timeout = 1

# For efficiency with batch operations
[[queues.consumers]]
queue = "batch-queue"
max_batch_size = 100
max_batch_timeout = 30
```

### Idempotency

```javascript
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      // Use message ID for idempotency
      const processed = await env.KV.get(`processed:${message.id}`);
      
      if (processed) {
        console.log(`Message ${message.id} already processed`);
        message.ack();
        continue;
      }
      
      try {
        await processMessage(message.body);
        
        // Mark as processed
        await env.KV.put(`processed:${message.id}`, '1', {
          expirationTtl: 86400, // 24 hours
        });
        
        message.ack();
      } catch (error) {
        message.retry();
      }
    }
  },
};
```

### Monitoring

```javascript
export default {
  async queue(batch, env) {
    const startTime = Date.now();
    let successful = 0;
    let failed = 0;
    
    for (const message of batch.messages) {
      try {
        await processMessage(message.body);
        message.ack();
        successful++;
      } catch (error) {
        message.retry();
        failed++;
      }
    }
    
    // Send metrics
    await env.ANALYTICS.writeDataPoint({
      indexes: ['queue-consumer'],
      blobs: [env.QUEUE_NAME],
      doubles: [
        Date.now() - startTime, // processing time
        successful,
        failed,
      ],
    });
  },
};
```

## Troubleshooting

### Messages Not Being Consumed

Check consumer configuration:

```bash
# Verify queue binding
npx wrangler queues list

# Check consumer logs
npx wrangler tail queue-consumer
```

Verify consumer is deployed:

```javascript
// Ensure queue handler is exported
export default {
  async queue(batch, env) {
    // Handler code
  },
};
```

### High Retry Rates

Implement proper error handling:

```javascript
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      try {
        // Validate message before processing
        if (!isValidMessage(message.body)) {
          console.error('Invalid message format:', message.body);
          message.ack(); // Don't retry invalid messages
          continue;
        }
        
        await processMessage(message.body);
        message.ack();
      } catch (error) {
        if (isRetriableError(error)) {
          message.retry();
        } else {
          console.error('Non-retriable error:', error);
          message.ack(); // Send to DLQ if configured
        }
      }
    }
  },
};

function isRetriableError(error) {
  return error.code === 'ETIMEDOUT' || 
         error.code === 'ECONNRESET' ||
         error.status >= 500;
}
```

### Dead Letter Queue Full

Monitor and process DLQ:

```javascript
// DLQ Consumer with alerting
export default {
  async queue(batch, env) {
    if (batch.messages.length > 100) {
      // Alert on high DLQ volume
      await sendAlert(env, `DLQ has ${batch.messages.length} messages`);
    }
    
    for (const message of batch.messages) {
      // Log for investigation
      await env.ERROR_LOG.put(
        `dlq/${message.id}`,
        JSON.stringify({
          body: message.body,
          attempts: message.attempts,
          timestamp: Date.now(),
        })
      );
      
      message.ack();
    }
  },
};
```

### Memory Issues

Process messages efficiently:

```javascript
export default {
  async queue(batch, env) {
    // Process in chunks to avoid memory issues
    const CHUNK_SIZE = 10;
    
    for (let i = 0; i < batch.messages.length; i += CHUNK_SIZE) {
      const chunk = batch.messages.slice(i, i + CHUNK_SIZE);
      await Promise.all(chunk.map(async (message) => {
        await processMessage(message.body);
        message.ack();
      }));
    }
  },
};
```

## See Also

- [Cloudflare Workers](./cloudflare-workers.md) - Serverless compute platform
- [Cloudflare D1](./cloudflare-d1.md) - Serverless SQL database
- [Cloudflare R2](./cloudflare-r2.md) - Object storage
- [Cloudflare KV](./cloudflare-kv.md) - Key-value storage
- [Cloudflare Durable Objects](./cloudflare-durable-objects.md) - Stateful coordination
