---
name: Vercel AI Elements
description: Production-ready React components for AI chat UIs built on shadcn/ui and integrated with the Vercel AI SDK. Includes Conversation, Message, PromptInput, Reasoning components, customizable themes, and streaming support. Trigger phrases include "AI components", "chat UI", "AI elements", "conversation UI", "shadcn AI", "React AI components".
license: MIT
---

# Vercel AI Elements

Vercel AI Elements provides production-ready React components for building AI chat interfaces. Built on shadcn/ui and deeply integrated with the Vercel AI SDK, these components handle streaming, theming, and common chat UI patterns out of the box.

## When to Use

Use Vercel AI Elements when you need to:

- **Build AI chat interfaces** quickly with pre-built components
- **Handle streaming AI responses** with automatic UI updates
- **Customize chat UI** with shadcn/ui-based theming
- **Display AI reasoning** and thinking processes
- **Create conversational interfaces** with message history
- **Add prompt input** with suggestions and validation
- **Show typing indicators** and loading states
- **Render markdown** in AI responses
- **Build production-ready chat UIs** without starting from scratch
- **Maintain consistent design** across AI features

Trigger phrases: "AI chat components", "chat UI", "conversation interface", "AI elements", "shadcn AI", "React chat components", "AI UI library"

## Official Documentation

- **Main Documentation**: https://elements.ai-sdk.dev/
- **Getting Started**: https://elements.ai-sdk.dev/docs
- **Components**: https://elements.ai-sdk.dev/docs/components
- **Examples**: https://elements.ai-sdk.dev/examples
- **Customization**: https://elements.ai-sdk.dev/docs/customization
- **Theming**: https://elements.ai-sdk.dev/docs/theming
- **API Reference**: https://elements.ai-sdk.dev/docs/reference
- **GitHub Repository**: https://github.com/vercel/ai-elements

## Quick Start

### Installation

```bash
# Install AI Elements and dependencies
npm install @vercel/ai-elements ai

# Install peer dependencies
npm install react react-dom

# Optional: shadcn/ui for theming
npx shadcn-ui@latest init
```

### Basic Chat Interface

```typescript
'use client';

import { Conversation, Message, PromptInput } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen">
      <Conversation className="flex-1 overflow-y-auto">
        {messages.map(message => (
          <Message
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}
      </Conversation>
      
      <PromptInput
        value={input}
        onChange={handleInputChange}
        onSubmit={handleSubmit}
        placeholder="Ask me anything..."
      />
    </div>
  );
}
```

### Streaming Messages

```typescript
'use client';

import { Conversation, Message } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export function StreamingChat() {
  const { messages, isLoading } = useChat();

  return (
    <Conversation>
      {messages.map(message => (
        <Message
          key={message.id}
          role={message.role}
          content={message.content}
          streaming={message.id === messages[messages.length - 1].id && isLoading}
        />
      ))}
    </Conversation>
  );
}
```

## Core Features

### Components

- **Conversation**: Container for message history
- **Message**: Individual message with role-based styling
- **PromptInput**: Input field with submit and suggestions
- **Reasoning**: Show AI thinking process
- **Avatar**: User and AI avatars
- **LoadingIndicator**: Typing indicators
- **ErrorMessage**: Error display
- **Toolbar**: Action buttons and controls

### Styling

- **Built on shadcn/ui**: Consistent design system
- **Customizable Themes**: Light/dark mode support
- **CSS Variables**: Easy color customization
- **Tailwind Integration**: Utility-first styling
- **Component Variants**: Multiple style options
- **Responsive Design**: Mobile-friendly layouts

### AI SDK Integration

- **useChat Hook**: Automatic message handling
- **Streaming Support**: Real-time response updates
- **Tool Calling**: Display function calls
- **Error Handling**: Built-in error states
- **Loading States**: Automatic indicators
- **Message History**: Persistent conversations

### Markdown Support

- **Syntax Highlighting**: Code blocks with highlighting
- **Tables**: Formatted table rendering
- **Lists**: Ordered and unordered lists
- **Links**: Clickable hyperlinks
- **Images**: Embedded images
- **Custom Renderers**: Override markdown elements

### Accessibility

- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard control
- **Focus Management**: Proper focus handling
- **Semantic HTML**: Accessible markup
- **Color Contrast**: WCAG compliant
- **Screen Reader Announcements**: Dynamic updates

## Common Use Cases

### Chat with Reasoning Display

```typescript
'use client';

import { Conversation, Message, Reasoning, PromptInput } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export function ReasoningChat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen">
      <Conversation>
        {messages.map(message => (
          <div key={message.id}>
            {message.reasoning && (
              <Reasoning steps={message.reasoning} />
            )}
            <Message
              role={message.role}
              content={message.content}
            />
          </div>
        ))}
      </Conversation>
      
      <PromptInput
        value={input}
        onChange={handleInputChange}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
```

### Custom Message Rendering

```typescript
'use client';

import { Conversation, Message } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export function CustomMessageChat() {
  const { messages } = useChat();

  return (
    <Conversation>
      {messages.map(message => (
        <Message
          key={message.id}
          role={message.role}
          content={message.content}
          renderContent={(content) => (
            <div className="custom-message">
              <ReactMarkdown>{content}</ReactMarkdown>
              {message.role === 'assistant' && (
                <div className="actions">
                  <button onClick={() => copyToClipboard(content)}>
                    Copy
                  </button>
                  <button onClick={() => regenerate(message.id)}>
                    Regenerate
                  </button>
                </div>
              )}
            </div>
          )}
        />
      ))}
    </Conversation>
  );
}
```

### Prompt Suggestions

```typescript
'use client';

import { PromptInput } from '@vercel/ai-elements';
import { useState } from 'react';

export function PromptWithSuggestions() {
  const [input, setInput] = useState('');
  
  const suggestions = [
    'Explain quantum computing',
    'Write a haiku about coding',
    'Debug this code snippet',
  ];

  return (
    <PromptInput
      value={input}
      onChange={(e) => setInput(e.target.value)}
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit(input);
      }}
      suggestions={suggestions}
      onSuggestionClick={(suggestion) => setInput(suggestion)}
      placeholder="Ask anything or choose a suggestion..."
    />
  );
}
```

### Multi-Modal Messages

```typescript
'use client';

import { Message } from '@vercel/ai-elements';

export function MultiModalMessage({ message }) {
  return (
    <Message
      role={message.role}
      content={
        <div>
          <p>{message.text}</p>
          {message.images?.map((img, i) => (
            <img key={i} src={img} alt="" className="mt-2 rounded-lg" />
          ))}
          {message.code && (
            <pre className="mt-2">
              <code>{message.code}</code>
            </pre>
          )}
        </div>
      }
    />
  );
}
```

### Custom Avatars

```typescript
'use client';

import { Conversation, Message, Avatar } from '@vercel/ai-elements';

export function CustomAvatarChat({ messages }) {
  return (
    <Conversation>
      {messages.map(message => (
        <Message
          key={message.id}
          role={message.role}
          content={message.content}
          avatar={
            <Avatar
              src={message.role === 'user' ? userAvatar : aiAvatar}
              alt={message.role}
              fallback={message.role === 'user' ? 'U' : 'AI'}
            />
          }
        />
      ))}
    </Conversation>
  );
}
```

### Loading States

```typescript
'use client';

import { Conversation, Message, LoadingIndicator } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export function LoadingChat() {
  const { messages, isLoading } = useChat();

  return (
    <Conversation>
      {messages.map(message => (
        <Message key={message.id} role={message.role} content={message.content} />
      ))}
      {isLoading && (
        <div className="flex items-center gap-2 p-4">
          <LoadingIndicator />
          <span className="text-muted-foreground">AI is thinking...</span>
        </div>
      )}
    </Conversation>
  );
}
```

### Error Handling

```typescript
'use client';

import { Conversation, Message, ErrorMessage } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export function ErrorHandlingChat() {
  const { messages, error, reload } = useChat();

  return (
    <div>
      <Conversation>
        {messages.map(message => (
          <Message key={message.id} role={message.role} content={message.content} />
        ))}
      </Conversation>
      
      {error && (
        <ErrorMessage
          error={error}
          onRetry={reload}
          message="Something went wrong. Please try again."
        />
      )}
    </div>
  );
}
```

## Integration

### Next.js App Router

```typescript
// app/chat/page.tsx
'use client';

import { Conversation, Message, PromptInput } from '@vercel/ai-elements';
import { useChat } from 'ai/react';

export default function ChatPage() {
  const chat = useChat({ api: '/api/chat' });

  return (
    <div className="container mx-auto h-screen flex flex-col">
      <Conversation className="flex-1">
        {chat.messages.map(m => (
          <Message key={m.id} role={m.role} content={m.content} />
        ))}
      </Conversation>
      <PromptInput {...chat} />
    </div>
  );
}
```

### Tailwind CSS

```typescript
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './node_modules/@vercel/ai-elements/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'ai-primary': '#0070f3',
        'ai-secondary': '#7928ca',
      },
    },
  },
};
```

### shadcn/ui Theming

```typescript
// app/globals.css
@layer base {
  :root {
    --ai-background: 0 0% 100%;
    --ai-foreground: 222.2 84% 4.9%;
    --ai-primary: 221.2 83.2% 53.3%;
    --ai-secondary: 210 40% 96.1%;
  }
  
  .dark {
    --ai-background: 222.2 84% 4.9%;
    --ai-foreground: 210 40% 98%;
    --ai-primary: 217.2 91.2% 59.8%;
    --ai-secondary: 217.2 32.6% 17.5%;
  }
}
```

### Vercel AI SDK

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

## Best Practices

### 1. Optimize Performance

```typescript
'use client';

import { memo } from 'react';
import { Message } from '@vercel/ai-elements';

const MemoizedMessage = memo(Message);

export function OptimizedChat({ messages }) {
  return (
    <Conversation>
      {messages.map(message => (
        <MemoizedMessage
          key={message.id}
          role={message.role}
          content={message.content}
        />
      ))}
    </Conversation>
  );
}
```

### 2. Virtualize Long Conversations

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

export function VirtualizedChat({ messages }) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: messages.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100,
  });

  return (
    <div ref={parentRef} className="h-full overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(item => (
          <div key={item.key} style={{ transform: `translateY(${item.start}px)` }}>
            <Message {...messages[item.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 3. Accessibility

```typescript
import { Conversation, Message } from '@vercel/ai-elements';

export function AccessibleChat({ messages }) {
  return (
    <Conversation
      role="log"
      aria-live="polite"
      aria-label="Chat conversation"
    >
      {messages.map(message => (
        <Message
          key={message.id}
          role={message.role}
          content={message.content}
          aria-label={`${message.role} message: ${message.content}`}
        />
      ))}
    </Conversation>
  );
}
```

## Troubleshooting

### Components Not Styling

```bash
# Ensure Tailwind is configured
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Add to tailwind.config.js
content: [
  './node_modules/@vercel/ai-elements/**/*.{js,ts,jsx,tsx}',
]
```

### Streaming Not Working

```typescript
// Ensure proper streaming setup
export async function POST(req: Request) {
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  // Use toAIStreamResponse()
  return result.toAIStreamResponse();
}
```

## See Also

- **vercel-ai-sdk** - AI SDK for backend logic
- **vercel-streamdown** - Markdown streaming
- **vercel-chat-sdk** - Chat bot framework
- **vercel-platform** - Deploy AI applications
