---
name: Cloudflare AI
description: Deploy AI inference at the edge with Cloudflare Workers AI. Access model catalog, AI Gateway for caching and rate limiting, and integrate machine learning into your applications. Trigger phrases include "Cloudflare AI", "Workers AI", "edge AI inference", "AI Gateway", "AI models at edge", and "serverless AI".
license: MIT
---

# Cloudflare AI

Cloudflare AI enables you to run machine learning models at the edge using Workers AI, providing low-latency AI inference without managing infrastructure. Combined with AI Gateway for caching, rate limiting, and observability, you can build production-ready AI applications that scale globally.

## When to Use

Use Cloudflare AI when you need to:

- **Run AI inference at the edge** with low latency worldwide
- **Deploy AI models** without managing GPU infrastructure
- **Scale AI applications** globally with serverless architecture
- **Reduce AI costs** with caching and request optimization
- **Implement AI Gateway** for observability and control
- **Process images, text, or audio** with pre-trained models
- **Build chatbots and conversational AI** applications
- **Generate embeddings** for semantic search and RAG
- **Integrate AI** into existing Workers and Pages applications
- **Prototype AI features** quickly without infrastructure setup

Cloudflare AI is ideal for developers building AI-powered applications that require global distribution, low latency, and cost-effective scaling.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/ai/
- **Workers AI**: https://developers.cloudflare.com/workers-ai/
- **AI Gateway**: https://developers.cloudflare.com/ai-gateway/
- **Model Catalog**: https://developers.cloudflare.com/workers-ai/models/
- **Get Started**: https://developers.cloudflare.com/workers-ai/get-started/
- **API Reference**: https://developers.cloudflare.com/api/operations/workers-ai-post-run-model
- **Pricing**: https://developers.cloudflare.com/workers-ai/platform/pricing/

## Quick Start

### Setup Workers AI

**Install Wrangler:**
```bash
npm install -g wrangler
wrangler login
```

**Create AI Worker:**
```bash
# Create new project
wrangler init my-ai-app
cd my-ai-app

# Add AI binding to wrangler.toml
cat >> wrangler.toml <<EOF

[ai]
binding = "AI"
EOF
```

**Basic AI Worker:**
```javascript
// src/index.js
export default {
  async fetch(request, env) {
    const response = await env.AI.run('@cf/meta/llama-2-7b-chat-int8', {
      messages: [
        { role: 'user', content: 'What is Cloudflare?' }
      ]
    });
    
    return new Response(JSON.stringify(response), {
      headers: { 'content-type': 'application/json' }
    });
  }
};
```

**Deploy:**
```bash
wrangler deploy
```

### Text Generation Example

```javascript
export default {
  async fetch(request, env) {
    const { prompt } = await request.json();
    
    const response = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      {
        messages: [
          { role: 'system', content: 'You are a helpful assistant.' },
          { role: 'user', content: prompt }
        ],
        max_tokens: 500
      }
    );
    
    return Response.json(response);
  }
};
```

### Image Classification

```javascript
export default {
  async fetch(request, env) {
    const formData = await request.formData();
    const imageFile = formData.get('image');
    const imageBytes = await imageFile.arrayBuffer();
    
    const response = await env.AI.run(
      '@cf/microsoft/resnet-50',
      {
        image: [...new Uint8Array(imageBytes)]
      }
    );
    
    return Response.json(response);
  }
};
```

### Text Embeddings

```javascript
export default {
  async fetch(request, env) {
    const { text } = await request.json();
    
    const embeddings = await env.AI.run(
      '@cf/baai/bge-base-en-v1.5',
      {
        text: text
      }
    );
    
    return Response.json({ embeddings });
  }
};
```

## Core Features

### 1. Text Generation Models

Generate text with large language models.

**Chat Completion:**
```javascript
export default {
  async fetch(request, env) {
    const { messages } = await request.json();
    
    const response = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      {
        messages: messages,
        temperature: 0.7,
        max_tokens: 1000,
        top_p: 0.9
      }
    );
    
    return Response.json(response);
  }
};
```

**Streaming Responses:**
```javascript
export default {
  async fetch(request, env) {
    const { prompt } = await request.json();
    
    const stream = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      {
        messages: [{ role: 'user', content: prompt }],
        stream: true
      }
    );
    
    return new Response(stream, {
      headers: { 'content-type': 'text/event-stream' }
    });
  }
};
```

**Code Generation:**
```javascript
const response = await env.AI.run(
  '@cf/meta/llama-2-7b-chat-int8',
  {
    messages: [
      { role: 'system', content: 'You are a code assistant.' },
      { role: 'user', content: 'Write a Python function to reverse a string' }
    ]
  }
);
```

### 2. Text Embeddings

Generate vector embeddings for semantic search.

**Single Text Embedding:**
```javascript
const embedding = await env.AI.run(
  '@cf/baai/bge-base-en-v1.5',
  { text: 'The quick brown fox jumps over the lazy dog' }
);
```

**Batch Embeddings with Vectorize:**
```javascript
export default {
  async fetch(request, env) {
    const { texts } = await request.json();
    
    // Generate embeddings
    const embeddings = await Promise.all(
      texts.map(text => 
        env.AI.run('@cf/baai/bge-base-en-v1.5', { text })
      )
    );
    
    // Store in Vectorize
    const vectors = embeddings.map((emb, i) => ({
      id: `doc-${i}`,
      values: emb.data[0],
      metadata: { text: texts[i] }
    }));
    
    await env.VECTORIZE_INDEX.upsert(vectors);
    
    return Response.json({ inserted: vectors.length });
  }
};
```

**Semantic Search:**
```javascript
export default {
  async fetch(request, env) {
    const { query } = await request.json();
    
    // Generate query embedding
    const queryEmbedding = await env.AI.run(
      '@cf/baai/bge-base-en-v1.5',
      { text: query }
    );
    
    // Search similar vectors
    const matches = await env.VECTORIZE_INDEX.query(
      queryEmbedding.data[0],
      { topK: 5 }
    );
    
    return Response.json(matches);
  }
};
```

### 3. Image Models

Process and classify images.

**Image Classification:**
```javascript
export default {
  async fetch(request, env) {
    const imageUrl = new URL(request.url).searchParams.get('url');
    const imageResponse = await fetch(imageUrl);
    const imageBytes = await imageResponse.arrayBuffer();
    
    const classification = await env.AI.run(
      '@cf/microsoft/resnet-50',
      { image: [...new Uint8Array(imageBytes)] }
    );
    
    return Response.json(classification);
  }
};
```

**Image-to-Text (Captioning):**
```javascript
const caption = await env.AI.run(
  '@cf/unum/uform-gen2-qwen-500m',
  {
    image: imageArray,
    prompt: 'Describe this image',
    max_tokens: 100
  }
);
```

**Object Detection:**
```javascript
const objects = await env.AI.run(
  '@cf/meta/detr-resnet-50',
  { image: imageArray }
);
```

### 4. AI Gateway

Add caching, rate limiting, and analytics to AI requests.

**Configure AI Gateway:**
```javascript
export default {
  async fetch(request, env) {
    const gateway = 'https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/workers-ai';
    
    const response = await fetch(gateway, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.CF_API_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: '@cf/meta/llama-2-7b-chat-int8',
        messages: [{ role: 'user', content: 'Hello!' }]
      })
    });
    
    return response;
  }
};
```

**Caching with AI Gateway:**
```javascript
// Gateway automatically caches identical requests
const gatewayUrl = `https://gateway.ai.cloudflare.com/v1/${ACCOUNT_ID}/${GATEWAY_ID}/openai`;

const response = await fetch(`${gatewayUrl}/chat/completions`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${OPENAI_API_KEY}`,
    'Content-Type': 'application/json',
    'cf-aig-cache-ttl': '3600' // Cache for 1 hour
  },
  body: JSON.stringify({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: 'What is AI?' }]
  })
});
```

**Rate Limiting:**
```javascript
// Configure rate limits in AI Gateway dashboard
// Per user, per API key, or global limits
// Example: 100 requests per minute per user
```

### 5. Translation

Translate text between languages.

```javascript
const translation = await env.AI.run(
  '@cf/meta/m2m100-1.2b',
  {
    text: 'Hello, how are you?',
    source_lang: 'english',
    target_lang: 'french'
  }
);
```

### 6. Speech Recognition

Transcribe audio to text.

```javascript
export default {
  async fetch(request, env) {
    const formData = await request.formData();
    const audioFile = formData.get('audio');
    const audioBytes = await audioFile.arrayBuffer();
    
    const transcription = await env.AI.run(
      '@cf/openai/whisper',
      {
        audio: [...new Uint8Array(audioBytes)]
      }
    );
    
    return Response.json(transcription);
  }
};
```

## Common Use Cases

### 1. AI-Powered Chatbot

```javascript
export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }
    
    const { message, conversationHistory = [] } = await request.json();
    
    // Build conversation context
    const messages = [
      { role: 'system', content: 'You are a helpful customer support assistant.' },
      ...conversationHistory,
      { role: 'user', content: message }
    ];
    
    // Generate response
    const response = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      { messages, max_tokens: 500 }
    );
    
    return Response.json({
      reply: response.response,
      conversationHistory: [
        ...conversationHistory,
        { role: 'user', content: message },
        { role: 'assistant', content: response.response }
      ]
    });
  }
};
```

### 2. Document Q&A with RAG

```javascript
export default {
  async fetch(request, env) {
    const { question } = await request.json();
    
    // Generate question embedding
    const questionEmbedding = await env.AI.run(
      '@cf/baai/bge-base-en-v1.5',
      { text: question }
    );
    
    // Find relevant documents
    const matches = await env.VECTORIZE_INDEX.query(
      questionEmbedding.data[0],
      { topK: 3 }
    );
    
    // Build context from matches
    const context = matches.matches
      .map(m => m.metadata.text)
      .join('\n\n');
    
    // Generate answer
    const answer = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      {
        messages: [
          { role: 'system', content: `Answer based on this context:\n${context}` },
          { role: 'user', content: question }
        ]
      }
    );
    
    return Response.json({ answer: answer.response, sources: matches });
  }
};
```

### 3. Content Moderation

```javascript
export default {
  async fetch(request, env) {
    const { content } = await request.json();
    
    const moderation = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      {
        messages: [
          {
            role: 'system',
            content: 'Classify if content is appropriate or inappropriate. Reply with only "APPROPRIATE" or "INAPPROPRIATE".'
          },
          { role: 'user', content: content }
        ]
      }
    );
    
    const isAppropriate = moderation.response.includes('APPROPRIATE');
    
    return Response.json({
      allowed: isAppropriate,
      classification: moderation.response
    });
  }
};
```

### 4. Image Analysis API

```javascript
export default {
  async fetch(request, env) {
    const formData = await request.formData();
    const image = formData.get('image');
    const imageBytes = await image.arrayBuffer();
    const imageArray = [...new Uint8Array(imageBytes)];
    
    // Run multiple models
    const [classification, caption] = await Promise.all([
      env.AI.run('@cf/microsoft/resnet-50', { image: imageArray }),
      env.AI.run('@cf/unum/uform-gen2-qwen-500m', {
        image: imageArray,
        prompt: 'What is in this image?'
      })
    ]);
    
    return Response.json({
      classification: classification,
      caption: caption.description
    });
  }
};
```

### 5. Multi-Language Support

```javascript
export default {
  async fetch(request, env) {
    const { text, targetLanguage } = await request.json();
    
    // Detect language (simplified)
    const translation = await env.AI.run(
      '@cf/meta/m2m100-1.2b',
      {
        text: text,
        source_lang: 'english',
        target_lang: targetLanguage
      }
    );
    
    return Response.json({ translatedText: translation.translated_text });
  }
};
```

## Integration

### 1. Integration with Vectorize

```javascript
// Store and search embeddings
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/index') {
      const { documents } = await request.json();
      
      const vectors = await Promise.all(
        documents.map(async (doc) => {
          const embedding = await env.AI.run(
            '@cf/baai/bge-base-en-v1.5',
            { text: doc.text }
          );
          
          return {
            id: doc.id,
            values: embedding.data[0],
            metadata: { text: doc.text }
          };
        })
      );
      
      await env.VECTORIZE.upsert(vectors);
      return Response.json({ indexed: vectors.length });
    }
    
    if (url.pathname === '/search') {
      const { query } = await request.json();
      
      const embedding = await env.AI.run(
        '@cf/baai/bge-base-en-v1.5',
        { text: query }
      );
      
      const results = await env.VECTORIZE.query(embedding.data[0], { topK: 5 });
      return Response.json(results);
    }
  }
};
```

### 2. Integration with D1 Database

```javascript
export default {
  async fetch(request, env) {
    const { query } = await request.json();
    
    // Convert to SQL using AI
    const sqlGeneration = await env.AI.run(
      '@cf/meta/llama-2-7b-chat-int8',
      {
        messages: [
          {
            role: 'system',
            content: 'Convert natural language to SQL. Only output the SQL query.'
          },
          { role: 'user', content: query }
        ]
      }
    );
    
    // Execute on D1
    const results = await env.DB.prepare(sqlGeneration.response).all();
    
    return Response.json(results);
  }
};
```

### 3. Integration with R2 Storage

```javascript
export default {
  async fetch(request, env) {
    // Process uploaded images
    const formData = await request.formData();
    const image = formData.get('image');
    const imageBytes = await image.arrayBuffer();
    
    // Analyze image
    const analysis = await env.AI.run(
      '@cf/microsoft/resnet-50',
      { image: [...new Uint8Array(imageBytes)] }
    );
    
    // Store in R2 with metadata
    const key = `images/${Date.now()}.jpg`;
    await env.R2_BUCKET.put(key, imageBytes, {
      customMetadata: {
        classification: JSON.stringify(analysis)
      }
    });
    
    return Response.json({ key, analysis });
  }
};
```

### 4. Integration with Pages

```javascript
// functions/api/chat.js
export async function onRequestPost(context) {
  const { message } = await context.request.json();
  
  const response = await context.env.AI.run(
    '@cf/meta/llama-2-7b-chat-int8',
    {
      messages: [{ role: 'user', content: message }]
    }
  );
  
  return Response.json(response);
}
```

## Best Practices

### 1. Model Selection
- Choose appropriate model size for task complexity
- Balance latency vs accuracy requirements
- Use streaming for long-form content
- Cache embeddings for frequently accessed data
- Test multiple models to find best fit

### 2. Cost Optimization
- Implement AI Gateway caching
- Use smaller models when possible
- Batch requests when appropriate
- Set reasonable token limits
- Monitor usage and costs

### 3. Error Handling
- Implement retry logic for transient failures
- Validate inputs before model calls
- Handle rate limits gracefully
- Provide fallback responses
- Log errors for debugging

### 4. Performance
- Use streaming for better UX
- Cache common queries
- Run models in parallel when possible
- Optimize prompt engineering
- Monitor response times

### 5. Security
- Validate and sanitize user inputs
- Implement rate limiting per user
- Use AI Gateway for request filtering
- Monitor for abuse patterns
- Protect API keys and tokens

## Troubleshooting

### Issue: Model Not Found

```javascript
// Verify model name
const models = await fetch('https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/models/search');
const modelList = await models.json();
console.log(modelList);
```

### Issue: Rate Limited

```javascript
// Implement retry with backoff
async function runWithRetry(env, model, input, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await env.AI.run(model, input);
    } catch (error) {
      if (error.message.includes('rate limit') && i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
        continue;
      }
      throw error;
    }
  }
}
```

### Issue: Timeout Errors

```javascript
// Use streaming for long responses
const stream = await env.AI.run(model, {
  ...input,
  stream: true
});
```

### Issue: High Costs

```javascript
// Implement caching
const cacheKey = `ai-response:${JSON.stringify(input)}`;
let cached = await env.KV.get(cacheKey);

if (!cached) {
  const response = await env.AI.run(model, input);
  await env.KV.put(cacheKey, JSON.stringify(response), { expirationTtl: 3600 });
  return response;
}

return JSON.parse(cached);
```

## See Also

- **[Cloudflare Workers](cloudflare-workers.md)** - Serverless compute platform
- **[Cloudflare Vectorize](cloudflare-vectorize.md)** - Vector database for embeddings
- **[Cloudflare D1](cloudflare-d1.md)** - Serverless SQL database
- **[Cloudflare R2](cloudflare-r2.md)** - Object storage for AI assets
- **[Cloudflare Pages](cloudflare-pages.md)** - Deploy AI-powered applications
