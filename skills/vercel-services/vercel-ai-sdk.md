---
name: Vercel AI SDK
description: Master the Vercel AI SDK for building AI-powered applications with unified APIs for multiple LLM providers (OpenAI, Anthropic, Google, xAI). Handles text generation, structured output, tool calling, streaming, and multi-model support. Trigger phrases include "AI SDK", "Vercel AI", "generateText", "streamText", "tool calling", "structured output", "LLM integration", "AI streaming".
license: MIT
---

# Vercel AI SDK

The Vercel AI SDK is a TypeScript toolkit for building AI-powered applications with multiple LLM providers through a unified API. It simplifies working with OpenAI, Anthropic, Google, xAI, and other providers while handling streaming, structured output, and tool calling.

## When to Use

Use the Vercel AI SDK when you need to:

- **Build AI chat applications** with streaming responses
- **Integrate multiple LLM providers** with easy provider switching
- **Generate structured data** from LLMs using Zod schemas
- **Implement tool calling** for AI agents and function execution
- **Stream AI responses** to frontend applications
- **Build AI-powered forms** with validation and extraction
- **Create conversational interfaces** with message history
- **Prototype AI features** quickly with minimal code
- **Switch between AI models** without changing application code
- **Build production AI applications** with type safety

Trigger phrases: "generate text with AI", "stream AI responses", "OpenAI integration", "Anthropic Claude", "structured AI output", "AI tool calling", "multi-model AI", "AI SDK", "LLM streaming"

## Official Documentation

- **Main Documentation**: https://ai-sdk.dev/docs/
- **Getting Started**: https://ai-sdk.dev/docs/getting-started
- **AI SDK Core**: https://ai-sdk.dev/docs/ai-sdk-core
- **AI SDK UI**: https://ai-sdk.dev/docs/ai-sdk-ui
- **Providers**: https://ai-sdk.dev/providers
- **Examples**: https://ai-sdk.dev/examples
- **API Reference**: https://ai-sdk.dev/docs/reference
- **GitHub Repository**: https://github.com/vercel/ai

## Quick Start

### Installation

```bash
# Install AI SDK core
npm install ai

# Install provider packages
npm install @ai-sdk/openai
npm install @ai-sdk/anthropic
npm install @ai-sdk/google
npm install @ai-sdk/xai
```

### Basic Text Generation

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text } = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Explain the theory of relativity in simple terms.',
});

console.log(text);
```

### Streaming Responses

```typescript
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const { textStream } = await streamText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  prompt: 'Write a short story about a robot learning to paint.',
});

for await (const chunk of textStream) {
  process.stdout.write(chunk);
}
```

### Structured Output with Zod

```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { object } = await generateObject({
  model: openai('gpt-4-turbo'),
  schema: z.object({
    name: z.string(),
    age: z.number(),
    occupation: z.string(),
    skills: z.array(z.string()),
  }),
  prompt: 'Generate a fictional character profile for a software engineer.',
});

console.log(object);
// { name: "Alex Chen", age: 28, occupation: "Senior Software Engineer", skills: [...] }
```

## Core Features

### Multi-Provider Support

- **OpenAI**: GPT-4, GPT-3.5, GPT-4 Turbo
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
- **Google**: Gemini Pro, Gemini Ultra
- **xAI**: Grok models
- **Custom Providers**: Extend with your own providers
- **Single Line Swap**: Change providers without code changes

### Text Generation

- **Synchronous Generation**: `generateText()` for complete responses
- **Streaming Generation**: `streamText()` for real-time output
- **Prompt Engineering**: System messages, user messages, assistant messages
- **Temperature Control**: Adjust randomness and creativity
- **Max Tokens**: Control response length
- **Stop Sequences**: Define completion triggers

### Structured Output

- **Zod Schema Integration**: Type-safe structured data
- **JSON Mode**: Force JSON responses
- **Enum Support**: Constrained value selection
- **Nested Objects**: Complex data structures
- **Array Generation**: Lists and collections
- **Validation**: Automatic schema validation

### Tool Calling (Function Calling)

- **Tool Definition**: Describe functions with parameters
- **Automatic Execution**: AI decides when to call tools
- **Multi-Tool Support**: Multiple tools per request
- **Streaming with Tools**: Real-time tool execution
- **Type Safety**: TypeScript types for tool parameters
- **Tool Results**: Return values to the model

### Message Management

- **Conversation History**: Maintain multi-turn conversations
- **Role-based Messages**: System, user, assistant roles
- **Message Arrays**: Sequential conversation flow
- **Context Window**: Automatic token management
- **Message Formatting**: Rich content support

### Error Handling

- **Typed Errors**: Specific error types for different failures
- **Retry Logic**: Automatic retries with exponential backoff
- **Timeout Configuration**: Request timeout controls
- **Rate Limiting**: Handle provider rate limits
- **Fallback Models**: Switch to backup models on failure

## Common Use Cases

### Chat Application with Streaming

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
    system: 'You are a helpful assistant.',
  });

  return result.toAIStreamResponse();
}
```

### AI Agent with Tools

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { text } = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'What is the weather in San Francisco and what should I wear?',
  tools: {
    getWeather: {
      description: 'Get the current weather for a location',
      parameters: z.object({
        location: z.string().describe('The city name'),
      }),
      execute: async ({ location }) => {
        // Call weather API
        return {
          temperature: 72,
          condition: 'sunny',
          location,
        };
      },
    },
  },
  maxToolRoundtrips: 5,
});

console.log(text);
```

### Form Data Extraction

```typescript
import { generateObject } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

const resumeSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  experience: z.array(z.object({
    company: z.string(),
    role: z.string(),
    years: z.number(),
  })),
  skills: z.array(z.string()),
});

const { object } = await generateObject({
  model: anthropic('claude-3-5-sonnet-20241022'),
  schema: resumeSchema,
  prompt: `Extract structured data from this resume: ${resumeText}`,
});

console.log(object);
```

### Multi-Model Fallback

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

async function generateWithFallback(prompt: string) {
  try {
    return await generateText({
      model: openai('gpt-4-turbo'),
      prompt,
    });
  } catch (error) {
    console.warn('Primary model failed, using fallback');
    return await generateText({
      model: anthropic('claude-3-5-sonnet-20241022'),
      prompt,
    });
  }
}
```

### Streaming Object Generation

```typescript
import { streamObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { partialObjectStream } = await streamObject({
  model: openai('gpt-4-turbo'),
  schema: z.object({
    characters: z.array(z.object({
      name: z.string(),
      class: z.string(),
      backstory: z.string(),
    })),
  }),
  prompt: 'Generate 3 fantasy RPG characters with detailed backstories.',
});

for await (const partialObject of partialObjectStream) {
  console.clear();
  console.log(JSON.stringify(partialObject, null, 2));
}
```

### RAG (Retrieval Augmented Generation)

```typescript
import { generateText, embed } from 'ai';
import { openai } from '@ai-sdk/openai';

// 1. Embed user query
const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'How do I deploy a Next.js app?',
});

// 2. Search vector database (pseudo-code)
const relevantDocs = await vectorDB.search(embedding, { limit: 3 });

// 3. Generate answer with context
const { text } = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: `Answer the question using these documents:
  
Documents:
${relevantDocs.map(doc => doc.content).join('\n\n')}

Question: How do I deploy a Next.js app?`,
});

console.log(text);
```

## Integration

### Next.js Integration

```typescript
// app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  return result.toAIStreamResponse();
}
```

```typescript
// app/page.tsx
'use client';

import { useChat } from 'ai/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

### React Integration

```typescript
import { useCompletion } from 'ai/react';

function CompletionComponent() {
  const { completion, input, handleInputChange, handleSubmit } = useCompletion({
    api: '/api/completion',
  });

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
      <p>{completion}</p>
    </div>
  );
}
```

### Vercel AI Gateway

```typescript
import { openai } from '@ai-sdk/openai';

const model = openai('gpt-4-turbo', {
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: 'https://gateway.ai.cloudflare.com/v1/YOUR_ACCOUNT/YOUR_GATEWAY/openai',
});
```

### Vercel Workflow SDK

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { step } from '@vercel/workflow';

export async function aiWorkflow() {
  const analysis = await step('analyze', async () => {
    const { text } = await generateText({
      model: openai('gpt-4-turbo'),
      prompt: 'Analyze this data...',
    });
    return text;
  });

  return analysis;
}
```

## Best Practices

### 1. Environment Variables

```typescript
// Store API keys securely
const model = openai('gpt-4-turbo', {
  apiKey: process.env.OPENAI_API_KEY,
});
```

### 2. Error Handling

```typescript
import { generateText } from 'ai';
import { APICallError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof APICallError) {
    console.error('API call failed:', error.message);
    console.error('Status:', error.statusCode);
  }
}
```

### 3. Streaming for Better UX

```typescript
// Use streaming for long responses
const { textStream } = await streamText({
  model: openai('gpt-4-turbo'),
  prompt: 'Write a long essay...',
});

// Show progressive results to users
for await (const chunk of textStream) {
  displayToUser(chunk);
}
```

### 4. Cost Optimization

```typescript
// Use appropriate models for tasks
const simpleTask = await generateText({
  model: openai('gpt-3.5-turbo'), // Cheaper for simple tasks
  prompt: 'Summarize: ...',
});

const complexTask = await generateText({
  model: openai('gpt-4-turbo'), // Use GPT-4 when needed
  prompt: 'Complex reasoning...',
});
```

### 5. Type Safety with Zod

```typescript
// Always use Zod schemas for structured output
const schema = z.object({
  field: z.string(),
});

const { object } = await generateObject({
  model: openai('gpt-4-turbo'),
  schema,
  prompt: '...',
});

// TypeScript knows the exact shape
object.field; // string
```

### 6. Rate Limiting

```typescript
import pLimit from 'p-limit';

const limit = pLimit(5); // Max 5 concurrent requests

const promises = prompts.map(prompt =>
  limit(() => generateText({ model, prompt }))
);

const results = await Promise.all(promises);
```

### 7. Prompt Engineering

```typescript
const { text } = await generateText({
  model: openai('gpt-4-turbo'),
  system: 'You are an expert programmer. Be concise and accurate.',
  prompt: 'Explain async/await in JavaScript',
  temperature: 0.7,
  maxTokens: 500,
});
```

### 8. Caching and Deduplication

```typescript
import { cache } from 'react';

export const getCachedCompletion = cache(async (prompt: string) => {
  return await generateText({
    model: openai('gpt-4-turbo'),
    prompt,
  });
});
```

## Troubleshooting

### API Key Issues

```typescript
// Verify API key is set
if (!process.env.OPENAI_API_KEY) {
  throw new Error('OPENAI_API_KEY is not set');
}

// Test with a simple request
const { text } = await generateText({
  model: openai('gpt-3.5-turbo'),
  prompt: 'Say hello',
});
```

### Streaming Not Working

```typescript
// Ensure you return AIStreamResponse in Next.js
export async function POST(req: Request) {
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });

  // Use this for Next.js
  return result.toAIStreamResponse();
  
  // Or this for raw ReadableStream
  return new Response(result.textStream);
}
```

### Type Errors with Zod

```typescript
// Ensure schema matches expected output
const schema = z.object({
  name: z.string(),
  age: z.number(), // Not string!
});

const { object } = await generateObject({
  model: openai('gpt-4-turbo'),
  schema,
  prompt: 'Generate person data',
});
```

### Tool Calling Not Triggering

```typescript
// Use clear descriptions and prompts
const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Get the weather in New York', // Clear intent
  tools: {
    getWeather: {
      description: 'Get current weather for a city', // Clear description
      parameters: z.object({
        city: z.string().describe('The city name'), // Describe parameters
      }),
      execute: async ({ city }) => {
        return { temp: 72, city };
      },
    },
  },
});
```

### Rate Limit Errors

```typescript
// Implement exponential backoff
async function generateWithRetry(prompt: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await generateText({
        model: openai('gpt-4-turbo'),
        prompt,
      });
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
}
```

### Memory Issues with Large Contexts

```typescript
// Truncate conversation history
function truncateMessages(messages: Message[], maxTokens = 4000) {
  // Keep system message and recent messages
  return [
    messages[0], // system
    ...messages.slice(-10), // last 10 messages
  ];
}

const { text } = await generateText({
  model: openai('gpt-4-turbo'),
  messages: truncateMessages(allMessages),
});
```

## See Also

- **vercel-ai-elements** - React components for AI chat UIs
- **vercel-chat-sdk** - Unified chat bot framework
- **vercel-workflow-sdk** - Durable workflows and AI agents
- **vercel-ai-gateway** - Unified access to AI models
- **vercel-streamdown** - Markdown streaming for AI responses
- **cloudflare-ai** - AI inference at the edge
- **edge-ai-platform** - AI deployment across platforms
