---
name: Vercel Streamdown
description: Drop-in react-markdown replacement for AI streaming with GitHub Flavored Markdown, math equations, mermaid diagrams, code syntax highlighting, and robust handling of incomplete markdown during streaming. Trigger phrases include "stream markdown", "streamdown", "AI markdown", "markdown streaming", "incomplete markdown", "GFM streaming".
license: MIT
---

# Vercel Streamdown

Vercel Streamdown is a React component that renders streaming markdown from AI models. It's a drop-in replacement for react-markdown that handles incomplete markdown gracefully during streaming, with support for GitHub Flavored Markdown, math, mermaid diagrams, and code highlighting.

## When to Use

Use Vercel Streamdown when you need to:

- **Render streaming AI markdown** in real-time
- **Handle incomplete markdown** during streaming
- **Display code blocks** with syntax highlighting
- **Render math equations** (LaTeX/KaTeX)
- **Show mermaid diagrams** from markdown
- **Support GFM** (GitHub Flavored Markdown)
- **Replace react-markdown** for AI applications
- **Show progressive content** as AI generates it
- **Handle streaming errors** gracefully
- **Customize markdown rendering** with plugins

Trigger phrases: "stream markdown", "AI markdown rendering", "streamdown", "incomplete markdown", "markdown streaming", "GFM streaming", "real-time markdown"

## Official Documentation

- **Main Documentation**: https://streamdown.ai/docs
- **Getting Started**: https://streamdown.ai/docs/getting-started
- **API Reference**: https://streamdown.ai/docs/api
- **Plugins**: https://streamdown.ai/docs/plugins
- **Examples**: https://streamdown.ai/examples
- **GitHub Repository**: https://github.com/vercel/streamdown

## Quick Start

### Installation

```bash
# Install Streamdown
npm install @vercel/streamdown

# Install syntax highlighting (optional)
npm install shiki

# Install math support (optional)
npm install remark-math rehype-katex
```

### Basic Usage

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import { useChat } from 'ai/react';

export function ChatMessage() {
  const { messages } = useChat();

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          <Streamdown>{message.content}</Streamdown>
        </div>
      ))}
    </div>
  );
}
```

### With Syntax Highlighting

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import '@vercel/streamdown/dist/code.css'; // Code styles

export function MarkdownWithCode({ content }: { content: string }) {
  return (
    <Streamdown
      components={{
        code: {
          theme: 'github-dark',
          languages: ['javascript', 'typescript', 'python', 'bash'],
        },
      }}
    >
      {content}
    </Streamdown>
  );
}
```

### With Math Support

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import 'katex/dist/katex.min.css'; // Math styles

export function MarkdownWithMath({ content }: { content: string }) {
  return (
    <Streamdown
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
    >
      {content}
    </Streamdown>
  );
}
```

## Core Features

### Streaming Support

- **Incomplete Markdown**: Handles partial markdown gracefully
- **Progressive Rendering**: Shows content as it arrives
- **Error Recovery**: Recovers from malformed markdown
- **Buffer Management**: Smart buffering for performance
- **Real-time Updates**: Updates as new content streams in
- **Backpressure Handling**: Prevents overwhelming the renderer

### GitHub Flavored Markdown

- **Tables**: Render markdown tables
- **Task Lists**: Checkbox lists
- **Strikethrough**: ~~crossed out text~~
- **Autolinks**: Automatic URL linking
- **Emoji**: :emoji: support
- **Footnotes**: Reference-style footnotes

### Code Highlighting

- **Shiki Integration**: High-quality syntax highlighting
- **100+ Languages**: Support for most programming languages
- **Multiple Themes**: VS Code themes
- **Line Numbers**: Optional line numbering
- **Highlighting Lines**: Highlight specific lines
- **Inline Code**: Styled inline code blocks

### Math Rendering

- **LaTeX Support**: Full LaTeX equation support
- **Inline Math**: $E = mc^2$
- **Block Math**: Display equations
- **KaTeX**: Fast math rendering
- **MathJax Alternative**: Lighter weight
- **Chemical Equations**: Chemistry notation

### Mermaid Diagrams

- **Flowcharts**: Process diagrams
- **Sequence Diagrams**: Interaction diagrams
- **Gantt Charts**: Project timelines
- **Class Diagrams**: UML diagrams
- **State Diagrams**: State machines
- **Pie Charts**: Data visualization

### Customization

- **Custom Components**: Override any element
- **Custom Plugins**: Remark/Rehype plugins
- **Styling**: CSS classes and inline styles
- **Component Props**: Pass props to elements
- **Render Hooks**: Intercept rendering
- **Theme Support**: Light/dark themes

## Common Use Cases

### AI Chat with Code

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import { useChat } from 'ai/react';
import '@vercel/streamdown/dist/code.css';

export function AIChat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(message => (
          <div
            key={message.id}
            className={message.role === 'user' ? 'text-right' : 'text-left'}
          >
            <div className={`inline-block max-w-3xl p-4 rounded-lg ${
              message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100'
            }`}>
              <Streamdown
                components={{
                  code: {
                    theme: 'github-dark',
                    showLineNumbers: true,
                  },
                }}
              >
                {message.content}
              </Streamdown>
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Ask anything..."
          className="w-full p-2 border rounded"
        />
      </form>
    </div>
  );
}
```

### Technical Documentation

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import '@vercel/streamdown/dist/code.css';

export function TechnicalDoc({ content }: { content: string }) {
  return (
    <article className="prose prose-lg max-w-4xl mx-auto">
      <Streamdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code: {
            theme: 'nord',
            showLineNumbers: true,
          },
          h1: ({ children }) => (
            <h1 className="text-4xl font-bold mt-8 mb-4">{children}</h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-3xl font-semibold mt-6 mb-3">{children}</h2>
          ),
        }}
      >
        {content}
      </Streamdown>
    </article>
  );
}
```

### Mermaid Diagrams

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';

export function DiagramDoc({ content }: { content: string }) {
  return (
    <Streamdown
      components={{
        mermaid: {
          theme: 'default',
        },
      }}
    >
      {content}
    </Streamdown>
  );
}

// Markdown content with mermaid:
const content = `
# System Architecture

\`\`\`mermaid
graph TD
    A[Client] -->|HTTP| B[API Gateway]
    B --> C[Service 1]
    B --> D[Service 2]
    C --> E[Database]
    D --> E
\`\`\`
`;
```

### Custom Components

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import { CopyButton } from './copy-button';

export function CustomMarkdown({ content }: { content: string }) {
  return (
    <Streamdown
      components={{
        code: ({ children, className, ...props }) => {
          const language = className?.replace('language-', '');
          return (
            <div className="relative">
              <CopyButton code={String(children)} />
              <code className={className} {...props}>
                {children}
              </code>
            </div>
          );
        },
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            {children}
          </a>
        ),
        table: ({ children }) => (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              {children}
            </table>
          </div>
        ),
      }}
    >
      {content}
    </Streamdown>
  );
}
```

### Streaming with Progress

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import { useState } from 'react';

export function StreamingMarkdown() {
  const [content, setContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  async function startStream() {
    setIsStreaming(true);
    setContent('');

    const response = await fetch('/api/stream');
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value);
      setContent(prev => prev + chunk);
    }

    setIsStreaming(false);
  }

  return (
    <div>
      <button onClick={startStream} disabled={isStreaming}>
        {isStreaming ? 'Streaming...' : 'Start Stream'}
      </button>

      <div className="mt-4">
        <Streamdown>{content}</Streamdown>
      </div>

      {isStreaming && (
        <div className="mt-2 text-gray-500">
          Receiving content...
        </div>
      )}
    </div>
  );
}
```

## Integration

### Vercel AI SDK

```typescript
'use client';

import { Streamdown } from '@vercel/streamdown';
import { useChat } from 'ai/react';

export function AIMarkdown() {
  const { messages } = useChat({
    api: '/api/chat',
  });

  const lastMessage = messages[messages.length - 1];
  const isAssistant = lastMessage?.role === 'assistant';

  return (
    <div>
      {isAssistant && (
        <Streamdown>{lastMessage.content}</Streamdown>
      )}
    </div>
  );
}
```

### Next.js App Router

```typescript
// app/chat/page.tsx
'use client';

import { Streamdown } from '@vercel/streamdown';
import { useChat } from 'ai/react';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div className="container mx-auto p-4">
      {messages.map(m => (
        <div key={m.id} className="mb-4">
          <div className="font-bold">{m.role}</div>
          <Streamdown>{m.content}</Streamdown>
        </div>
      ))}
      
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

### Tailwind CSS

```typescript
// Component with Tailwind
export function StyledMarkdown({ content }: { content: string }) {
  return (
    <div className="prose prose-slate max-w-none dark:prose-invert">
      <Streamdown>{content}</Streamdown>
    </div>
  );
}
```

## Best Practices

### 1. Handle Loading States

```typescript
export function LoadingMarkdown({ content, isStreaming }) {
  return (
    <div>
      <Streamdown>{content}</Streamdown>
      {isStreaming && content.length > 0 && (
        <span className="animate-pulse">▊</span>
      )}
    </div>
  );
}
```

### 2. Optimize Performance

```typescript
import { memo } from 'react';

const MemoizedStreamdown = memo(Streamdown);

export function OptimizedChat({ messages }) {
  return (
    <>
      {messages.map(msg => (
        <MemoizedStreamdown key={msg.id}>
          {msg.content}
        </MemoizedStreamdown>
      ))}
    </>
  );
}
```

### 3. Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary';

export function SafeMarkdown({ content }) {
  return (
    <ErrorBoundary
      fallback={<div>Failed to render markdown</div>}
    >
      <Streamdown>{content}</Streamdown>
    </ErrorBoundary>
  );
}
```

## Troubleshooting

### Code Highlighting Not Working

```bash
# Install required packages
npm install shiki

# Import CSS
import '@vercel/streamdown/dist/code.css';
```

### Math Not Rendering

```bash
# Install math packages
npm install remark-math rehype-katex

# Import KaTeX CSS
import 'katex/dist/katex.min.css';
```

## See Also

- **vercel-ai-sdk** - AI streaming backend
- **vercel-ai-elements** - Complete AI UI components
- **vercel-chat-sdk** - Chat bot framework
