---
name: message-queue-integrator
description: Sets up publish/subscribe or task queue patterns using RabbitMQ, Kafka, or SQS, including producer, consumer, and dead-letter configs. Invoke when asked to add a message queue, implement async processing, set up event-driven architecture, configure Kafka, RabbitMQ, or SQS, or decouple services with messaging.
---

# Message Queue Integrator

Designs and implements message queue and event streaming integrations for asynchronous processing, service decoupling, and event-driven architectures — covering RabbitMQ, Apache Kafka, Amazon SQS, and Google Pub/Sub with producer, consumer, dead-letter queue, and retry configurations.

## When to Use

- User asks to "add a message queue", "implement async processing", or "decouple these services"
- Long-running tasks need to be offloaded from synchronous request handlers
- Services need to communicate without direct dependencies (event-driven architecture)
- User asks about Kafka, RabbitMQ, SQS, or pub/sub patterns
- A task queue is needed for background jobs (email sending, report generation, data processing)
- User wants to implement fan-out (one message → multiple consumers)

## Process

1. **Identify the messaging system** from context or recommend one:
   - **RabbitMQ**: general-purpose, complex routing, task queues, moderate scale
   - **Apache Kafka**: high-throughput event streaming, audit logs, event sourcing, replay capability
   - **Amazon SQS**: managed, AWS-native, serverless-friendly, simple task queues
   - **Google Pub/Sub**: GCP-native, scalable pub/sub
   - **Redis Streams** / **BullMQ**: lightweight task queues for Node.js backed by Redis

2. **Choose the messaging pattern**:
   - **Task Queue (Work Queue)**: one message consumed by exactly one worker (load balancing). Use for: email sending, image processing, data exports.
   - **Pub/Sub (Fan-out)**: one message delivered to all subscribers. Use for: notifications, cache invalidation, event broadcasting.
   - **Event Streaming**: ordered, replayable log of events. Use for: audit trail, event sourcing, analytics pipelines (Kafka).
   - **Request/Reply**: send a message and wait for a correlated response. Use for: RPC-style async operations.

3. **Design the message schema**:
   - Use a consistent envelope: `{ id, type, timestamp, version, payload }`
   - Specify a content type (JSON is default)
   - Consider schema registry (Confluent Schema Registry for Kafka, Avro/Protobuf)
   - Include a `correlationId` for request tracking across services

4. **Design the reliability configuration**:
   - **Dead-Letter Queue (DLQ)**: messages that fail after N retries go here for investigation
   - **Retry policy**: exponential backoff, max retries (3–5 for most cases)
   - **Message TTL**: expire messages that are too old to be useful
   - **Acknowledgement**: explicitly ACK on success; NACK/reject on failure to trigger retry
   - **Idempotency**: consumers must handle duplicate delivery (at-least-once guarantees)

5. **Generate producer code**:
   - Connect with retry on startup (queues/topics may not be ready immediately)
   - Serialize message with schema envelope
   - Publish with appropriate routing key / topic / queue name
   - Handle publish confirmation (publisher confirms in RabbitMQ, delivery callbacks in Kafka)

6. **Generate consumer code**:
   - Subscribe to the appropriate queue/topic/subscription
   - Deserialize and validate message schema
   - Process idempotently (check if already processed using `id`)
   - Explicitly ACK on success
   - On error: retry with backoff; after max retries, send to DLQ and ACK original

7. **Generate infrastructure config** (docker-compose for local, or IaC snippet).

## Output Format

```
## Message Queue Integration Plan

**System:** RabbitMQ
**Pattern:** Task Queue (Work Queue)
**Use case:** Async email sending triggered by user registration

### Architecture
```
UserService ──publish──▶ [exchange: notifications] ──route──▶ [queue: email.send]
                                                                      │
                                                               EmailWorker (consumer)
                                                                      │
                                                              [DLQ: email.send.dlq]
                                                              (on 3 failed attempts)
```

### Files Generated
- `src/messaging/rabbitmq.client.ts`  — connection management, channel pool
- `src/messaging/producers/email.producer.ts` — publish email task messages
- `src/workers/email.worker.ts`       — consume and process email tasks
- `src/messaging/types.ts`            — message envelope and payload types
- `docker-compose.yml` (rabbitmq service) — management UI on port 15672
```

### `src/messaging/producers/email.producer.ts`
```ts
import { getChannel } from '../rabbitmq.client';
import { MessageEnvelope } from '../types';
import { randomUUID } from 'crypto';

const EXCHANGE = 'notifications';
const ROUTING_KEY = 'email.send';

export async function publishSendEmail(payload: SendEmailPayload): Promise<void> {
  const channel = await getChannel();
  const message: MessageEnvelope<SendEmailPayload> = {
    id: randomUUID(),
    type: 'email.send',
    timestamp: new Date().toISOString(),
    version: '1',
    payload,
  };
  channel.publish(
    EXCHANGE,
    ROUTING_KEY,
    Buffer.from(JSON.stringify(message)),
    { persistent: true, contentType: 'application/json' }
  );
}
```

## Examples

### Example Input
```
Add Kafka for order events in a Node.js e-commerce app.
Orders service publishes events. Inventory and notification services consume them.
Need DLQ for failed processing.
```

### Example Output (summary)
```
Topic: order-events (3 partitions, replication-factor: 3)
DLQ topic: order-events-dlq

Producer (orders service):
  - Publishes OrderCreated, OrderCancelled, OrderShipped events
  - Key: orderId (ensures order events processed in sequence per order)
  - Acks: all (wait for all replicas to confirm)

Consumers:
  - inventory-service consumer group: subscribes to order-events, updates stock
  - notification-service consumer group: subscribes to order-events, sends emails

Consumer error handling:
  - On error: retry up to 3 times with 1s/2s/4s backoff
  - After 3 failures: produce to order-events-dlq with error metadata
  - Commit offset only after successful processing (manual commit)

Message schema:
  { id: uuid, type: 'OrderCreated', timestamp: ISO8601, version: '1', payload: { orderId, ... } }
```

## Boundaries

- Do NOT generate broker-specific infrastructure configs (RabbitMQ policies, Kafka broker configs) without noting that these require broker-admin access.
- Do NOT use auto-acknowledge in consumers — always require explicit ACK after successful processing.
- Do NOT produce messages without persistence (`persistent: true` or `acks: all`) for business-critical events.
- Always design for at-least-once delivery — consumers must be idempotent.
- Do NOT recommend message queues for synchronous request/response patterns where direct HTTP is simpler and adequate.
- Note that schema evolution (adding fields) is generally safe; removing or renaming fields requires versioned schemas or a migration strategy.
- If the broker is not available in the local environment, provide docker-compose setup instructions.
