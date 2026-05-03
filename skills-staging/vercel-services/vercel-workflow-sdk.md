---
name: Vercel Workflow SDK
description: Build durable workflows and AI agents with the Vercel Workflow SDK. Features "use workflow" and "use step" directives, hooks, sleep/delay, multiple execution worlds (Vercel, local, custom), observability, and debugging tools. Trigger phrases include "durable workflows", "workflow SDK", "AI agents", "long-running tasks", "workflow orchestration".
license: MIT
---

# Vercel Workflow SDK

The Vercel Workflow SDK enables building durable, resumable workflows and AI agents that can survive failures, handle long-running tasks, and maintain state across execution boundaries. Perfect for complex multi-step processes and AI agent orchestration.

## When to Use

Use the Vercel Workflow SDK when you need to:

- **Build durable workflows** that survive restarts
- **Create AI agents** with multi-step reasoning
- **Handle long-running tasks** (hours, days, weeks)
- **Orchestrate multi-step processes** with state management
- **Implement retries and error handling** automatically
- **Sleep/delay execution** for scheduled tasks
- **Coordinate parallel tasks** with dependencies
- **Build reliable automations** with guaranteed execution
- **Track workflow progress** with observability
- **Debug complex workflows** with step-by-step inspection

Trigger phrases: "durable workflows", "workflow SDK", "long-running tasks", "AI agents", "workflow orchestration", "resumable workflows", "step functions"

## Official Documentation

- **Main Documentation**: https://workflow-sdk.dev/
- **Getting Started**: https://workflow-sdk.dev/docs/getting-started
- **Quickstart**: https://workflow-sdk.dev/docs/quickstart
- **Concepts**: https://workflow-sdk.dev/docs/concepts
- **API Reference**: https://workflow-sdk.dev/docs/api
- **Worlds**: https://workflow-sdk.dev/docs/worlds
- **Observability**: https://workflow-sdk.dev/docs/observability
- **GitHub Repository**: https://github.com/vercel/workflow

## Quick Start

### Installation

```bash
# Install Workflow SDK
npm install @vercel/workflow

# Install AI SDK for AI agents (optional)
npm install ai @ai-sdk/openai
```

### Basic Workflow

```typescript
'use workflow';

import { step, sleep } from '@vercel/workflow';

export async function myWorkflow(input: string) {
  // Step 1: Process input
  const processed = await step('process', async () => {
    return input.toUpperCase();
  });

  // Step 2: Wait 5 seconds
  await sleep('5s');

  // Step 3: Final transformation
  const result = await step('transform', async () => {
    return `Result: ${processed}`;
  });

  return result;
}
```

### AI Agent Workflow

```typescript
'use workflow';

import { step } from '@vercel/workflow';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function aiAgentWorkflow(task: string) {
  // Step 1: Analyze task
  const analysis = await step('analyze', async () => {
    const { text } = await generateText({
      model: openai('gpt-4-turbo'),
      prompt: `Analyze this task and break it into steps: ${task}`,
    });
    return JSON.parse(text);
  });

  // Step 2: Execute each step
  const results = [];
  for (const [index, substep] of analysis.steps.entries()) {
    const result = await step(`execute-${index}`, async () => {
      const { text } = await generateText({
        model: openai('gpt-4-turbo'),
        prompt: `Execute this step: ${substep}`,
      });
      return text;
    });
    results.push(result);
  }

  // Step 3: Synthesize results
  const final = await step('synthesize', async () => {
    const { text } = await generateText({
      model: openai('gpt-4-turbo'),
      prompt: `Synthesize these results: ${results.join('\n')}`,
    });
    return text;
  });

  return final;
}
```

### Invoking Workflows

```typescript
// Next.js API route
import { myWorkflow } from '@/workflows/my-workflow';

export async function POST(req: Request) {
  const { input } = await req.json();
  
  const result = await myWorkflow(input);
  
  return Response.json({ result });
}
```

## Core Features

### Workflow Directives

- **'use workflow'**: Marks file as workflow
- **'use step'**: Marks function as step
- **Automatic Durability**: State persisted between steps
- **Resume on Failure**: Continue from last checkpoint
- **Idempotent Steps**: Same step ID = cached result
- **Type Safety**: Full TypeScript support

### Step Management

- **step()**: Define durable execution steps
- **Step IDs**: Unique identifiers for caching
- **Step Retry**: Automatic retry on failure
- **Step Timeout**: Configure execution limits
- **Step Dependencies**: Order execution
- **Parallel Steps**: Concurrent execution

### Time Control

- **sleep()**: Delay execution (seconds, minutes, hours, days)
- **sleepUntil()**: Sleep until specific timestamp
- **Scheduled Workflows**: Cron-like scheduling
- **Timeout Handling**: Graceful timeout handling
- **Long Delays**: Support for days/weeks delays

### Execution Worlds

- **Vercel World**: Production Vercel deployment
- **Local World**: Development environment
- **Custom World**: Your own infrastructure
- **World Switching**: Easy environment changes
- **State Persistence**: Per-world state storage

### Error Handling

- **Automatic Retries**: Configurable retry logic
- **Exponential Backoff**: Smart retry delays
- **Error Recovery**: Resume from failures
- **Error Logging**: Detailed error tracking
- **Fallback Logic**: Alternative execution paths
- **Circuit Breakers**: Prevent cascading failures

### Observability

- **Workflow Dashboard**: Visual workflow tracking
- **Step Timeline**: See step execution history
- **Real-time Updates**: Monitor running workflows
- **Execution Logs**: Detailed logging
- **Performance Metrics**: Duration, retries, errors
- **Debug Mode**: Step-by-step debugging

## Common Use Cases

### Multi-Step AI Agent

```typescript
'use workflow';

import { step } from '@vercel/workflow';
import { generateText, generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

export async function researchAgent(topic: string) {
  // Step 1: Generate research questions
  const questions = await step('generate-questions', async () => {
    const { object } = await generateObject({
      model: openai('gpt-4-turbo'),
      schema: z.object({
        questions: z.array(z.string()),
      }),
      prompt: `Generate 5 research questions about: ${topic}`,
    });
    return object.questions;
  });

  // Step 2: Research each question
  const answers = [];
  for (const [i, question] of questions.entries()) {
    const answer = await step(`research-${i}`, async () => {
      // Simulate research (could call external APIs)
      const { text } = await generateText({
        model: openai('gpt-4-turbo'),
        prompt: `Research and answer: ${question}`,
      });
      return { question, answer: text };
    });
    answers.push(answer);
  }

  // Step 3: Synthesize report
  const report = await step('synthesize-report', async () => {
    const { text } = await generateText({
      model: openai('gpt-4-turbo'),
      prompt: `Create a research report from these Q&As: ${JSON.stringify(answers)}`,
    });
    return text;
  });

  return report;
}
```

### Scheduled Email Campaign

```typescript
'use workflow';

import { step, sleep } from '@vercel/workflow';

export async function emailCampaign(subscribers: string[], content: string) {
  const results = [];
  
  for (const [index, email] of subscribers.entries()) {
    // Send email
    const sent = await step(`send-${index}`, async () => {
      await sendEmail(email, content);
      return { email, sent: true };
    });
    results.push(sent);
    
    // Wait 1 minute between emails (rate limiting)
    if (index < subscribers.length - 1) {
      await sleep('1m');
    }
  }
  
  // Wait 24 hours
  await sleep('24h');
  
  // Follow-up email
  const followUps = await step('follow-up', async () => {
    const opened = await checkOpened(subscribers);
    const notOpened = subscribers.filter(e => !opened.includes(e));
    
    for (const email of notOpened) {
      await sendEmail(email, 'Follow-up: ' + content);
    }
    
    return notOpened.length;
  });
  
  return { sent: results.length, followUps };
}
```

### Data Processing Pipeline

```typescript
'use workflow';

import { step } from '@vercel/workflow';

export async function dataPipeline(dataUrl: string) {
  // Step 1: Fetch data
  const rawData = await step('fetch', async () => {
    const response = await fetch(dataUrl);
    return response.json();
  });

  // Step 2: Validate
  const validated = await step('validate', async () => {
    return rawData.filter(item => isValid(item));
  });

  // Step 3: Transform (parallel)
  const transformed = await Promise.all(
    validated.map((item, i) =>
      step(`transform-${i}`, async () => transform(item))
    )
  );

  // Step 4: Load to database
  const loaded = await step('load', async () => {
    await db.bulkInsert(transformed);
    return transformed.length;
  });

  return { processed: loaded };
}
```

### Retry with Exponential Backoff

```typescript
'use workflow';

import { step, sleep } from '@vercel/workflow';

export async function reliableApiCall(url: string) {
  const maxRetries = 3;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const result = await step(`api-call-attempt-${attempt}`, async () => {
        const response = await fetch(url);
        if (!response.ok) throw new Error('API error');
        return response.json();
      });
      return result;
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      
      // Exponential backoff: 2^attempt seconds
      await sleep(`${Math.pow(2, attempt)}s`);
    }
  }
}
```

### Approval Workflow

```typescript
'use workflow';

import { step, sleep } from '@vercel/workflow';

export async function approvalWorkflow(request: any) {
  // Step 1: Submit request
  const submission = await step('submit', async () => {
    return await db.requests.create(request);
  });

  // Step 2: Send notification
  await step('notify', async () => {
    await sendNotification(request.approver, submission.id);
  });

  // Step 3: Wait for approval (max 48 hours)
  let approved = false;
  const deadline = Date.now() + 48 * 60 * 60 * 1000;
  
  while (!approved && Date.now() < deadline) {
    const status = await step(`check-${Date.now()}`, async () => {
      return await db.requests.findById(submission.id);
    });
    
    if (status.approved) {
      approved = true;
      break;
    }
    
    // Check every 5 minutes
    await sleep('5m');
  }

  if (!approved) {
    // Auto-reject after timeout
    await step('auto-reject', async () => {
      await db.requests.update(submission.id, { status: 'rejected' });
    });
    return { status: 'rejected', reason: 'timeout' };
  }

  // Step 4: Execute approved action
  const result = await step('execute', async () => {
    return await executeAction(request.action);
  });

  return { status: 'approved', result };
}
```

### Parallel Task Execution

```typescript
'use workflow';

import { step } from '@vercel/workflow';

export async function parallelWorkflow(tasks: string[]) {
  // Execute all tasks in parallel
  const results = await Promise.all(
    tasks.map((task, i) =>
      step(`task-${i}`, async () => {
        return await processTask(task);
      })
    )
  );

  // Aggregate results
  const summary = await step('aggregate', async () => {
    return {
      total: results.length,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
    };
  });

  return summary;
}
```

## Integration

### Next.js App Router

```typescript
// app/api/workflow/route.ts
import { myWorkflow } from '@/workflows/my-workflow';

export async function POST(req: Request) {
  const { input } = await req.json();
  
  try {
    const result = await myWorkflow(input);
    return Response.json({ success: true, result });
  } catch (error) {
    return Response.json({ success: false, error: error.message }, { status: 500 });
  }
}
```

### Vercel AI SDK

```typescript
'use workflow';

import { step } from '@vercel/workflow';
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function aiWorkflow(prompt: string) {
  return await step('generate', async () => {
    const { text } = await streamText({
      model: openai('gpt-4-turbo'),
      prompt,
    });
    return text;
  });
}
```

### Database Integration

```typescript
'use workflow';

import { step } from '@vercel/workflow';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function databaseWorkflow(data: any) {
  const created = await step('create', async () => {
    return await prisma.item.create({ data });
  });

  const processed = await step('process', async () => {
    return await processItem(created);
  });

  const updated = await step('update', async () => {
    return await prisma.item.update({
      where: { id: created.id },
      data: { processed: true, result: processed },
    });
  });

  return updated;
}
```

## Best Practices

### 1. Idempotent Steps

```typescript
// Use stable step IDs
await step('fetch-data', async () => {
  // This will only run once
  return await fetchData();
});

// Avoid dynamic step IDs that change on retry
// Bad: await step(`fetch-${Date.now()}`, ...)
// Good: await step('fetch', ...)
```

### 2. Error Handling

```typescript
'use workflow';

import { step } from '@vercel/workflow';

export async function robustWorkflow(input: string) {
  try {
    const result = await step('risky-operation', async () => {
      return await riskyOperation(input);
    });
    return result;
  } catch (error) {
    // Handle error gracefully
    const fallback = await step('fallback', async () => {
      return await fallbackOperation(input);
    });
    return fallback;
  }
}
```

### 3. Monitoring

```typescript
'use workflow';

import { step } from '@vercel/workflow';

export async function monitoredWorkflow(input: string) {
  const start = Date.now();
  
  const result = await step('main', async () => {
    return await operation(input);
  });
  
  await step('log-metrics', async () => {
    await logMetric('workflow-duration', Date.now() - start);
    await logMetric('workflow-result', result);
  });
  
  return result;
}
```

## Troubleshooting

### Workflow Not Resuming

```typescript
// Ensure step IDs are stable
// Bad - changes on each run:
await step(`step-${Math.random()}`, ...)

// Good - consistent ID:
await step('my-step', ...)
```

### Sleep Not Working

```typescript
// Use correct time format
await sleep('5s');  // 5 seconds
await sleep('5m');  // 5 minutes
await sleep('5h');  // 5 hours
await sleep('5d');  // 5 days
```

## See Also

- **vercel-ai-sdk** - AI integration for workflows
- **vercel-platform** - Deploy workflows on Vercel
- **cloudflare-durable-objects** - Alternative durable execution
- **cloudflare-queues** - Message queue alternative
