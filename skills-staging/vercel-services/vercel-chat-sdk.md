---
name: Vercel Chat SDK
description: Build unified chat bots for Slack, Teams, Discord, and other platforms with the Vercel Chat SDK. Features event-driven architecture, type-safe handlers, JSX cards, streaming AI responses, thread subscriptions, and state management. Trigger phrases include "chat bot", "Slack bot", "Teams bot", "Discord bot", "chat SDK", "bot framework", "messaging platform".
license: MIT
---

# Vercel Chat SDK

The Vercel Chat SDK is a unified framework for building chat bots across multiple platforms (Slack, Teams, Discord) with a single codebase. It provides event-driven architecture, type-safe handlers, JSX-based UI components, and seamless AI integration.

## When to Use

Use the Vercel Chat SDK when you need to:

- **Build cross-platform chat bots** for Slack, Teams, Discord, etc.
- **Create AI-powered bots** with streaming responses
- **Handle chat events** with type-safe handlers
- **Render rich UI components** using JSX cards
- **Manage conversation threads** and subscriptions
- **Build interactive workflows** with buttons and forms
- **Integrate with AI models** for intelligent responses
- **Maintain conversation state** across interactions
- **Deploy bots to multiple platforms** from a single codebase
- **Handle slash commands** and mentions

Trigger phrases: "build a Slack bot", "create Teams integration", "Discord bot", "multi-platform chat bot", "chat SDK", "messaging bot", "interactive cards", "bot framework"

## Official Documentation

- **Main Documentation**: https://chat-sdk.dev/docs
- **Getting Started**: https://chat-sdk.dev/docs/getting-started
- **Platform Guides**: https://chat-sdk.dev/docs/platforms
- **Components**: https://chat-sdk.dev/docs/components
- **AI Integration**: https://chat-sdk.dev/docs/ai
- **Examples**: https://chat-sdk.dev/examples
- **API Reference**: https://chat-sdk.dev/docs/reference
- **GitHub Repository**: https://github.com/vercel/chat-sdk

## Quick Start

### Installation

```bash
# Install Chat SDK
npm install @vercel/chat-sdk

# Install platform adapters
npm install @vercel/chat-sdk-slack
npm install @vercel/chat-sdk-teams
npm install @vercel/chat-sdk-discord

# Install AI SDK for intelligent responses
npm install ai @ai-sdk/openai
```

### Basic Slack Bot

```typescript
import { ChatSDK } from '@vercel/chat-sdk';
import { SlackAdapter } from '@vercel/chat-sdk-slack';

const chat = new ChatSDK({
  adapter: new SlackAdapter({
    signingSecret: process.env.SLACK_SIGNING_SECRET!,
    botToken: process.env.SLACK_BOT_TOKEN!,
  }),
});

// Handle mentions
chat.on('message', async ({ message, say }) => {
  if (message.text.includes('hello')) {
    await say('Hello! How can I help you today?');
  }
});

// Handle slash commands
chat.command('/help', async ({ command, respond }) => {
  await respond({
    text: 'Available commands:',
    blocks: [
      {
        type: 'section',
        text: { type: 'mrkdwn', text: '• `/help` - Show this message' },
      },
    ],
  });
});

export default chat;
```

### JSX Components

```typescript
import { ChatSDK } from '@vercel/chat-sdk';
import { Card, Button, Input } from '@vercel/chat-sdk/components';

chat.on('message', async ({ message, say }) => {
  await say(
    <Card>
      <section>
        <h2>Welcome to our bot!</h2>
        <p>Choose an action below:</p>
      </section>
      <actions>
        <Button value="option1">Option 1</Button>
        <Button value="option2">Option 2</Button>
      </actions>
    </Card>
  );
});

// Handle button clicks
chat.on('action', async ({ action, respond }) => {
  if (action.value === 'option1') {
    await respond('You selected Option 1!');
  }
});
```

### AI Integration

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

chat.on('message', async ({ message, say }) => {
  const { textStream } = await streamText({
    model: openai('gpt-4-turbo'),
    prompt: message.text,
  });

  // Stream AI response
  let fullText = '';
  for await (const chunk of textStream) {
    fullText += chunk;
    await say.update(fullText);
  }
});
```

## Core Features

### Event-Driven Architecture

- **Message Events**: Handle incoming messages
- **Slash Commands**: Custom command handlers
- **Action Events**: Button clicks, form submissions
- **App Mentions**: Direct mentions of the bot
- **Thread Events**: Replies and thread updates
- **Typing Indicators**: Show bot is working
- **Presence Events**: User online/offline status

### Type-Safe Handlers

- **TypeScript Support**: Full type safety
- **Event Types**: Strongly typed event objects
- **Context Objects**: Type-safe context access
- **Response Methods**: Type-checked responses
- **Error Handling**: Type-safe error types
- **Payload Validation**: Runtime type checking

### JSX Components

- **Card Components**: Rich message layouts
- **Button Components**: Interactive buttons
- **Input Components**: Form fields
- **Select Components**: Dropdown menus
- **Image Components**: Embedded images
- **Divider Components**: Visual separators
- **Section Components**: Structured layouts

### Platform Adapters

- **Slack Adapter**: Full Slack API support
- **Teams Adapter**: Microsoft Teams integration
- **Discord Adapter**: Discord bot capabilities
- **Custom Adapters**: Build your own platform support
- **Unified API**: Same code across platforms
- **Platform-Specific Features**: Access unique capabilities

### Thread Management

- **Thread Subscriptions**: Monitor conversation threads
- **Thread Replies**: Respond in threads
- **Thread Context**: Access full thread history
- **Auto-Threading**: Automatic thread creation
- **Thread State**: Persist thread-specific state
- **Thread Notifications**: Alert on new messages

### State Management

- **Conversation State**: Per-conversation data
- **User State**: Per-user preferences
- **Global State**: Application-wide data
- **Persistent Storage**: Database integration
- **Session Management**: Temporary state
- **State Middleware**: Transform state

## Common Use Cases

### AI Customer Support Bot

```typescript
import { ChatSDK } from '@vercel/chat-sdk';
import { SlackAdapter } from '@vercel/chat-sdk-slack';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const supportBot = new ChatSDK({
  adapter: new SlackAdapter({
    signingSecret: process.env.SLACK_SIGNING_SECRET!,
    botToken: process.env.SLACK_BOT_TOKEN!,
  }),
});

supportBot.on('message', async ({ message, say, thread }) => {
  // Get conversation history
  const history = await thread.getHistory();
  
  // Generate AI response
  const { text } = await generateText({
    model: openai('gpt-4-turbo'),
    system: 'You are a helpful customer support agent.',
    messages: history.map(msg => ({
      role: msg.userId === 'bot' ? 'assistant' : 'user',
      content: msg.text,
    })),
  });
  
  await say(text);
});

export default supportBot;
```

### Interactive Form with Validation

```typescript
import { Card, Input, Button, Select } from '@vercel/chat-sdk/components';

chat.command('/feedback', async ({ respond }) => {
  await respond(
    <Card>
      <section>
        <h2>Feedback Form</h2>
      </section>
      <Input
        name="name"
        label="Your Name"
        placeholder="Enter your name"
        required
      />
      <Select name="rating" label="Rating">
        <option value="5">⭐⭐⭐⭐⭐</option>
        <option value="4">⭐⭐⭐⭐</option>
        <option value="3">⭐⭐⭐</option>
        <option value="2">⭐⭐</option>
        <option value="1">⭐</option>
      </Select>
      <Input
        name="comment"
        label="Comment"
        multiline
        placeholder="Tell us more..."
      />
      <actions>
        <Button value="submit" style="primary">Submit</Button>
        <Button value="cancel">Cancel</Button>
      </actions>
    </Card>
  );
});

chat.on('action', async ({ action, respond, state }) => {
  if (action.value === 'submit') {
    const { name, rating, comment } = action.state;
    
    // Save to database
    await db.feedback.create({
      name,
      rating: parseInt(rating),
      comment,
      timestamp: new Date(),
    });
    
    await respond('Thank you for your feedback! 🎉');
  }
});
```

### Multi-Platform Deployment

```typescript
import { ChatSDK } from '@vercel/chat-sdk';
import { SlackAdapter } from '@vercel/chat-sdk-slack';
import { TeamsAdapter } from '@vercel/chat-sdk-teams';
import { DiscordAdapter } from '@vercel/chat-sdk-discord';

// Shared bot logic
function createBot(adapter) {
  const chat = new ChatSDK({ adapter });
  
  chat.on('message', async ({ message, say }) => {
    if (message.text.includes('help')) {
      await say('How can I assist you?');
    }
  });
  
  return chat;
}

// Deploy to multiple platforms
export const slackBot = createBot(new SlackAdapter({
  signingSecret: process.env.SLACK_SIGNING_SECRET!,
  botToken: process.env.SLACK_BOT_TOKEN!,
}));

export const teamsBot = createBot(new TeamsAdapter({
  appId: process.env.TEAMS_APP_ID!,
  appPassword: process.env.TEAMS_APP_PASSWORD!,
}));

export const discordBot = createBot(new DiscordAdapter({
  token: process.env.DISCORD_TOKEN!,
}));
```

### Scheduled Messages with Threads

```typescript
chat.command('/remind', async ({ command, respond, thread }) => {
  const [time, ...messageParts] = command.text.split(' ');
  const message = messageParts.join(' ');
  
  await respond(`I'll remind you in ${time} minutes!`);
  
  // Schedule reminder
  setTimeout(async () => {
    await thread.reply(`⏰ Reminder: ${message}`);
  }, parseInt(time) * 60 * 1000);
});
```

### Workflow Automation

```typescript
import { Card, Button } from '@vercel/chat-sdk/components';

chat.command('/deploy', async ({ respond, user }) => {
  await respond(
    <Card>
      <section>
        <h2>Deploy Application</h2>
        <p>Environment: Production</p>
        <p>Branch: main</p>
        <p>Requested by: {user.name}</p>
      </section>
      <actions>
        <Button value="approve" style="primary">Approve</Button>
        <Button value="reject" style="danger">Reject</Button>
      </actions>
    </Card>
  );
});

chat.on('action', async ({ action, respond, update }) => {
  if (action.value === 'approve') {
    await update('Deploying... ⚙️');
    
    // Trigger deployment
    await triggerDeployment();
    
    await update('✅ Deployment successful!');
  } else if (action.value === 'reject') {
    await respond('Deployment cancelled.');
  }
});
```

### Knowledge Base Search

```typescript
import { generateText, embed } from 'ai';
import { openai } from '@ai-sdk/openai';

chat.on('message', async ({ message, say }) => {
  // Search knowledge base
  const { embedding } = await embed({
    model: openai.embedding('text-embedding-3-small'),
    value: message.text,
  });
  
  const docs = await vectorDB.search(embedding, { limit: 3 });
  
  // Generate answer
  const { text } = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: `Answer using these docs:\n${docs.join('\n\n')}\n\nQuestion: ${message.text}`,
  });
  
  await say(text);
});
```

## Integration

### Next.js Integration

```typescript
// app/api/slack/route.ts
import { slackBot } from '@/lib/chat-bot';

export async function POST(req: Request) {
  return await slackBot.handle(req);
}
```

### Vercel AI SDK

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

chat.on('message', async ({ message, say }) => {
  const { textStream } = await streamText({
    model: openai('gpt-4-turbo'),
    prompt: message.text,
  });
  
  for await (const chunk of textStream) {
    await say.stream(chunk);
  }
});
```

### Database Storage

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

chat.use(async ({ message, next }) => {
  // Log message
  await prisma.message.create({
    data: {
      text: message.text,
      userId: message.userId,
      channelId: message.channelId,
      timestamp: new Date(),
    },
  });
  
  await next();
});
```

### Vercel Workflow SDK

```typescript
import { workflow, step } from '@vercel/workflow';

chat.on('message', async ({ message, say }) => {
  await workflow('process-message', async () => {
    const analysis = await step('analyze', async () => {
      return analyzeMessage(message.text);
    });
    
    const response = await step('generate', async () => {
      return generateResponse(analysis);
    });
    
    await say(response);
  });
});
```

## Best Practices

### 1. Error Handling

```typescript
chat.use(async ({ message, say, next }) => {
  try {
    await next();
  } catch (error) {
    console.error('Error:', error);
    await say('Sorry, something went wrong. Please try again.');
  }
});
```

### 2. Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = new Map();

chat.use(async ({ message, next }) => {
  const key = message.userId;
  const now = Date.now();
  const userLimit = limiter.get(key) || { count: 0, resetAt: now + 60000 };
  
  if (now > userLimit.resetAt) {
    userLimit.count = 0;
    userLimit.resetAt = now + 60000;
  }
  
  if (userLimit.count >= 10) {
    throw new Error('Rate limit exceeded');
  }
  
  userLimit.count++;
  limiter.set(key, userLimit);
  
  await next();
});
```

### 3. Logging and Monitoring

```typescript
chat.use(async ({ message, next }) => {
  const start = Date.now();
  
  await next();
  
  const duration = Date.now() - start;
  console.log(`Message processed in ${duration}ms`, {
    userId: message.userId,
    channelId: message.channelId,
  });
});
```

### 4. Environment-Specific Configuration

```typescript
const chat = new ChatSDK({
  adapter: new SlackAdapter({
    signingSecret: process.env.SLACK_SIGNING_SECRET!,
    botToken: process.env.SLACK_BOT_TOKEN!,
  }),
  debug: process.env.NODE_ENV === 'development',
});
```

### 5. Middleware Chain

```typescript
// Authentication
chat.use(async ({ message, next }) => {
  const user = await authenticateUser(message.userId);
  if (!user) throw new Error('Unauthorized');
  await next();
});

// Authorization
chat.use(async ({ message, command, next }) => {
  if (command?.name === '/admin') {
    const isAdmin = await checkAdmin(message.userId);
    if (!isAdmin) throw new Error('Forbidden');
  }
  await next();
});
```

## Troubleshooting

### Webhook Verification Failed

```typescript
// Ensure signing secret is correct
const adapter = new SlackAdapter({
  signingSecret: process.env.SLACK_SIGNING_SECRET!, // Check this value
  botToken: process.env.SLACK_BOT_TOKEN!,
});

// Enable debug mode
const chat = new ChatSDK({
  adapter,
  debug: true, // See verification details
});
```

### Messages Not Received

```typescript
// Check bot permissions in platform settings
// Slack: Add to channel, enable events
// Teams: Enable bot in manifest
// Discord: Add bot to server with message permissions

// Verify webhook URL is correct
console.log('Webhook URL:', process.env.WEBHOOK_URL);
```

### JSX Components Not Rendering

```typescript
// Enable JSX in tsconfig.json
{
  "compilerOptions": {
    "jsx": "react",
    "jsxImportSource": "@vercel/chat-sdk"
  }
}

// Import components correctly
import { Card, Button } from '@vercel/chat-sdk/components';
```

### Thread Replies Not Working

```typescript
// Ensure thread_ts is passed
chat.on('message', async ({ message, thread }) => {
  // Reply in thread
  await thread.reply('This is a threaded reply', {
    threadTs: message.threadTs || message.ts,
  });
});
```

## See Also

- **vercel-ai-sdk** - AI SDK for intelligent bot responses
- **vercel-workflow-sdk** - Durable workflows for bot automation
- **vercel-ai-elements** - React components for chat UIs
- **vercel-platform** - Deploy bots on Vercel
- **cloudflare-workers** - Alternative deployment platform
