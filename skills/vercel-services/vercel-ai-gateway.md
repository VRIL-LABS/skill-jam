---
name: Vercel AI Gateway
description: |
  Unified access to 200+ AI models from OpenAI, Anthropic, Google, and more through a single API.
  Use for AI model integration, multi-provider switching, rate limiting, cost tracking, and centralized monitoring.
  Trigger phrases: "AI gateway", "unified AI API", "multi-model access", "AI provider switching", "AI monitoring"
license: MIT
---

# Vercel AI Gateway

Vercel AI Gateway provides unified access to 200+ AI models from multiple providers through a single API endpoint. It simplifies AI integration by eliminating the need to manage multiple API keys, provides built-in rate limiting, cost tracking, and comprehensive monitoring for AI workloads.

## When to Use

Use Vercel AI Gateway when you need to:

- **Access multiple AI providers** through a single unified API interface
- **Switch between AI models** without changing your application code
- **Monitor AI usage** with built-in analytics and cost tracking
- **Implement rate limiting** for AI API calls across your organization
- **Secure AI credentials** using OIDC authentication for Vercel deployments
- **Track costs** across different AI providers and models
- **Test different models** by easily switching providers for A/B testing
- **Implement fallback strategies** when primary AI providers are unavailable

## Official Documentation

- **AI Gateway Overview**: https://vercel.com/docs/ai-gateway
- **API Reference**: https://vercel.com/docs/ai-gateway/api-reference
- **Supported Providers**: https://vercel.com/docs/ai-gateway/providers
- **Authentication**: https://vercel.com/docs/ai-gateway/authentication
- **Monitoring & Analytics**: https://vercel.com/docs/ai-gateway/monitoring
- **Rate Limiting**: https://vercel.com/docs/ai-gateway/rate-limiting
- **Vercel AI SDK**: https://sdk.vercel.ai/docs
- **Pricing**: https://vercel.com/docs/ai-gateway/pricing

## Quick Start

### Enable AI Gateway

```bash
# Install Vercel CLI
npm i -g vercel

# Link your project
vercel link

# Enable AI Gateway via Vercel Dashboard
# Project Settings > AI Gateway > Enable
```

### Configure Provider Credentials

```bash
# Add provider API keys
vercel env add OPENAI_API_KEY
vercel env add ANTHROPIC_API_KEY
vercel env add GOOGLE_GENERATIVE_AI_API_KEY
```

### Basic Usage

```typescript
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: prompt,
  });

  return Response.json({
    text: result.text,
    usage: result.usage,
  });
}
```

### Direct API Access

```typescript
const response = await fetch('https://gateway.vercel.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.VERCEL_AI_GATEWAY_TOKEN}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gpt-4-turbo',
    messages: [{ role: 'user', content: 'Hello!' }],
  }),
});
```

## Core Features

### 1. Unified API Interface

```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

async function generateWithProvider(provider: string, prompt: string) {
  const models = {
    openai: openai('gpt-4-turbo'),
    anthropic: anthropic('claude-3-opus-20240229'),
    google: google('gemini-pro'),
  };

  const result = await generateText({
    model: models[provider],
    prompt: prompt,
  });

  return result.text;
}
```

### 2. OIDC Authentication

```typescript
// Automatic authentication for Vercel deployments
export async function POST(request: Request) {
  // No need to manually manage tokens
  const result = await generateText({
    model: openai('gpt-4'),
    prompt: 'Hello from authenticated endpoint',
  });

  return Response.json({ text: result.text });
}
```

### 3. Rate Limiting

```typescript
// Configure in vercel.json
{
  "aiGateway": {
    "rateLimit": {
      "requests": 100,
      "window": "1m"
    }
  }
}

// Handle rate limits with retry
async function generateWithRetry(prompt: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await generateText({
        model: openai('gpt-4-turbo'),
        prompt: prompt,
      });
    } catch (error) {
      if (error.statusCode === 429 && i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

### 4. Streaming Responses

```typescript
import { streamText } from 'ai';

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const result = await streamText({
    model: openai('gpt-4-turbo'),
    prompt: prompt,
  });

  return result.toAIStreamResponse();
}
```

Client-side:

```typescript
'use client';
import { useCompletion } from 'ai/react';

export default function ChatComponent() {
  const { completion, input, handleInputChange, handleSubmit } = useCompletion();

  return (
    <form onSubmit={handleSubmit}>
      <input value={input} onChange={handleInputChange} />
      <div>{completion}</div>
    </form>
  );
}
```

### 5. Function Calling

```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get weather for a location',
  parameters: z.object({
    location: z.string(),
  }),
  execute: async ({ location }) => ({
    location,
    temperature: 72,
    conditions: 'sunny',
  }),
});

export async function POST(request: Request) {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'What is the weather in San Francisco?',
    tools: { weather: weatherTool },
  });

  return Response.json({ text: result.text });
}
```

### 6. Provider Fallback

```typescript
async function generateWithFallback(prompt: string) {
  const providers = [
    openai('gpt-4-turbo'),
    anthropic('claude-3-opus-20240229'),
  ];

  for (const model of providers) {
    try {
      const result = await generateText({ model, prompt });
      return result.text;
    } catch (error) {
      if (model === providers[providers.length - 1]) {
        throw error;
      }
      continue;
    }
  }
}
```

## Common Use Cases

### Multi-Model Chatbot

```typescript
export async function POST(request: Request) {
  const { messages, model = 'gpt-4' } = await request.json();

  const models = {
    'gpt-4': openai('gpt-4-turbo'),
    'claude': anthropic('claude-3-opus-20240229'),
  };

  const result = await streamText({
    model: models[model],
    messages: messages,
  });

  return result.toAIStreamResponse();
}
```

### Document Analysis

```typescript
import { generateObject } from 'ai';

const schema = z.object({
  summary: z.string(),
  keyPoints: z.array(z.string()),
  sentiment: z.enum(['positive', 'negative', 'neutral']),
});

export async function analyzeDocument(text: string) {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: schema,
    prompt: `Analyze: ${text}`,
  });

  return result.object;
}
```

### Embeddings for Search

```typescript
import { embed, embedMany } from 'ai';

export async function generateEmbedding(text: string) {
  const { embedding } = await embed({
    model: openai.embedding('text-embedding-3-small'),
    value: text,
  });
  return embedding;
}

export async function semanticSearch(query: string, documents: string[]) {
  const queryEmbedding = await generateEmbedding(query);
  const { embeddings } = await embedMany({
    model: openai.embedding('text-embedding-3-small'),
    values: documents,
  });

  return embeddings.map((emb, idx) => ({
    document: documents[idx],
    similarity: cosineSimilarity(queryEmbedding, emb),
  })).sort((a, b) => b.similarity - a.similarity);
}
```

### Translation Service

```typescript
export async function translate(text: string, targetLanguage: string) {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: `Translate to ${targetLanguage}: ${text}`,
    temperature: 0.3,
  });

  return result.text;
}
```

## Integration

### Next.js

```typescript
// app/api/chat/route.ts
export const runtime = 'edge';

export async function POST(request: Request) {
  const { messages } = await request.json();

  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  return result.toAIStreamResponse();
}
```

### Express.js

```typescript
import express from 'express';
import { generateText } from 'ai';

const app = express();
app.use(express.json());

app.post('/api/generate', async (req, res) => {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: req.body.prompt,
  });

  res.json({ text: result.text });
});

app.listen(3000);
```

## Best Practices

### Error Handling

```typescript
async function safeGenerate(prompt: string) {
  try {
    const result = await generateText({
      model: openai('gpt-4-turbo'),
      prompt: prompt,
    });
    return { success: true, text: result.text };
  } catch (error) {
    if (error.statusCode === 429) {
      return { success: false, error: 'Rate limit exceeded' };
    }
    return { success: false, error: 'Generation failed' };
  }
}
```

### Caching

```typescript
const cache = new Map();
const CACHE_TTL = 3600000;

async function cachedGenerate(prompt: string) {
  const cached = cache.get(prompt);
  if (cached && Date.now() - cached.time < CACHE_TTL) {
    return cached.text;
  }

  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt,
  });

  cache.set(prompt, { text: result.text, time: Date.now() });
  return result.text;
}
```

### Token Management

```typescript
async function generateWithLimit(prompt: string, maxTokens = 1000) {
  const estimated = Math.ceil(prompt.length / 4);
  
  if (estimated > maxTokens * 0.8) {
    throw new Error('Prompt too long');
  }

  return await generateText({
    model: openai('gpt-4-turbo'),
    prompt,
    maxTokens: maxTokens - estimated,
  });
}
```

### Security

```typescript
// Never expose tokens to client - use API routes
export async function POST(request: Request) {
  const session = await getSession(request);
  if (!session) {
    return new Response('Unauthorized', { status: 401 });
  }

  const { messages } = await request.json();
  
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  return result.toAIStreamResponse();
}
```

### Monitoring

```typescript
async function monitoredGenerate(prompt: string, userId: string) {
  const start = Date.now();

  try {
    const result = await generateText({
      model: openai('gpt-4-turbo'),
      prompt,
    });

    await logRequest({
      userId,
      tokens: result.usage.totalTokens,
      duration: Date.now() - start,
      status: 'success',
    });

    return result.text;
  } catch (error) {
    await logRequest({
      userId,
      duration: Date.now() - start,
      status: 'error',
      error: error.message,
    });
    throw error;
  }
}
```

## Troubleshooting

### Authentication Errors

**Problem**: 401 Unauthorized

**Solutions**:
```bash
# Verify environment variables
vercel env ls

# For local development
echo "VERCEL_AI_GATEWAY_TOKEN=token" >> .env.local
```

### Rate Limiting

**Problem**: 429 Too Many Requests

**Solutions**:
```typescript
// Implement exponential backoff
async function retryGenerate(prompt: string) {
  for (let i = 0; i < 3; i++) {
    try {
      return await generateText({
        model: openai('gpt-4-turbo'),
        prompt,
      });
    } catch (error) {
      if (error.statusCode === 429 && i < 2) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

### Streaming Issues

**Problem**: Streaming not working

**Solutions**:
```typescript
// Ensure edge runtime
export const runtime = 'edge';

// Use correct response format
return result.toAIStreamResponse();
```

### Token Limit Exceeded

**Problem**: Token limit exceeded

**Solutions**:
```typescript
function truncate(text: string, maxTokens = 4000): string {
  const estimated = text.length / 4;
  if (estimated > maxTokens) {
    return text.slice(0, maxTokens * 4) + '...';
  }
  return text;
}
```

## See Also

- [Vercel Platform](./vercel-platform.md) - Vercel hosting and deployment
- [Vercel AI SDK](https://sdk.vercel.ai/docs) - AI SDK documentation
- [OpenAI Platform](https://platform.openai.com/docs) - OpenAI docs
- [Anthropic Claude](https://docs.anthropic.com) - Claude docs
- [Google AI](https://ai.google.dev) - Google AI docs
