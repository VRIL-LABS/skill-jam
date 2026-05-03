---
name: Vercel Flags SDK
description: Feature flags for Next.js and SvelteKit with the Vercel Flags SDK. Provider-agnostic, TypeScript-first, precompute pattern, Flags Explorer, A/B testing, gradual rollouts, and experimentation. Trigger phrases include "feature flags", "flags SDK", "A/B testing", "gradual rollout", "feature toggles", "experimentation".
license: MIT
---

# Vercel Flags SDK

The Vercel Flags SDK provides a provider-agnostic feature flag solution for Next.js and SvelteKit applications. It enables A/B testing, gradual rollouts, and experimentation with type-safe flag definitions and a powerful precompute pattern.

## When to Use

Use the Vercel Flags SDK when you need to:

- **Enable/disable features** without redeploying
- **Run A/B tests** to compare feature variants
- **Gradual rollouts** to percentages of users
- **Target specific users** or user segments
- **Test in production** safely before full release
- **Experimentation** with multiple variants
- **Flag management** with visual explorer
- **Type-safe flags** with TypeScript
- **Provider flexibility** (Vercel, LaunchDarkly, Split, custom)
- **Precompute flags** at build or request time

Trigger phrases: "feature flags", "A/B testing", "gradual rollout", "canary deployment", "feature toggles", "flags SDK", "experimentation", "variant testing"

## Official Documentation

- **Main Documentation**: https://flags-sdk.dev/
- **Getting Started**: https://flags-sdk.dev/docs/getting-started
- **Quickstart**: https://flags-sdk.dev/docs/quickstart
- **Precompute Pattern**: https://flags-sdk.dev/docs/precompute
- **Flags Explorer**: https://flags-sdk.dev/docs/explorer
- **Providers**: https://flags-sdk.dev/docs/providers
- **API Reference**: https://flags-sdk.dev/docs/api-reference
- **GitHub Repository**: https://github.com/vercel/flags

## Quick Start

### Installation

```bash
# Install Flags SDK
npm install @vercel/flags

# Install provider (optional)
npm install @vercel/flags-vercel
npm install @vercel/flags-launchdarkly
```

### Basic Flag Definition (Next.js)

```typescript
// flags.ts
import { unstable_flag as flag } from '@vercel/flags/next';

export const showNewFeature = flag({
  key: 'show-new-feature',
  async decide() {
    // Default to false
    return false;
  },
});

export const theme = flag({
  key: 'theme',
  options: [
    { value: 'light', label: 'Light' },
    { value: 'dark', label: 'Dark' },
  ],
  async decide() {
    return 'light';
  },
});
```

### Using Flags in Components

```typescript
// app/page.tsx
import { showNewFeature } from './flags';

export default async function Page() {
  const isEnabled = await showNewFeature();
  
  return (
    <div>
      {isEnabled ? (
        <NewFeature />
      ) : (
        <OldFeature />
      )}
    </div>
  );
}
```

### Client-Side Flags

```typescript
'use client';

import { useFlag } from '@vercel/flags/react';
import { showNewFeature } from './flags';

export function ClientComponent() {
  const isEnabled = useFlag(showNewFeature);
  
  return isEnabled ? <NewFeature /> : <OldFeature />;
}
```

### Precompute Pattern

```typescript
// flags.ts
import { unstable_flag as flag, precompute } from '@vercel/flags/next';

export const showNewFeature = flag({
  key: 'show-new-feature',
  decide: precompute(async () => {
    // This runs at build time or on-demand
    const config = await fetch('https://api.example.com/config');
    const data = await config.json();
    return data.enableNewFeature;
  }),
});
```

## Core Features

### Flag Types

- **Boolean Flags**: Simple on/off toggles
- **String Flags**: Multiple string options
- **Number Flags**: Numeric values
- **Variant Flags**: Complex object variants
- **Enum Flags**: Predefined set of options
- **Custom Types**: TypeScript-based custom types

### Decision Logic

- **Static Values**: Return constant values
- **User-Based**: Target specific users
- **Percentage Rollouts**: Gradual rollout to user percentage
- **Segment-Based**: Target user segments
- **Time-Based**: Enable/disable at specific times
- **Geo-Based**: Target by geography
- **Custom Logic**: Any async decision function

### Providers

- **Vercel Provider**: Native Vercel integration
- **LaunchDarkly**: Enterprise feature management
- **Split.io**: Feature delivery platform
- **Custom Providers**: Build your own
- **Multi-Provider**: Use multiple providers
- **Provider Fallbacks**: Graceful degradation

### Precompute Pattern

- **Build-Time Evaluation**: Compute at build
- **Request-Time Evaluation**: Compute per request
- **Cache Control**: Custom cache strategies
- **Revalidation**: On-demand revalidation
- **ISR Support**: Incremental Static Regeneration
- **Edge Support**: Works with Edge Runtime

### Type Safety

- **TypeScript Integration**: Full type inference
- **Flag Types**: Strongly typed flag values
- **Option Types**: Type-safe options
- **Generic Support**: Generic flag definitions
- **Type Checking**: Compile-time validation
- **IntelliSense**: Auto-completion support

### Flags Explorer

- **Visual Interface**: Browse all flags
- **Override Flags**: Test different values
- **Flag History**: See flag changes
- **User Context**: Test with different users
- **Share Links**: Share flag configurations
- **Debug Mode**: Inspect flag decisions

## Common Use Cases

### Gradual Rollout by Percentage

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';
import { cookies } from 'next/headers';

function hashUserId(userId: string): number {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = ((hash << 5) - hash) + userId.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash);
}

export const betaFeature = flag({
  key: 'beta-feature',
  async decide() {
    const cookieStore = cookies();
    const userId = cookieStore.get('user_id')?.value || 'anonymous';
    
    // Enable for 20% of users
    const percentage = hashUserId(userId) % 100;
    return percentage < 20;
  },
});
```

### A/B Test with Variants

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';

export const checkoutFlow = flag({
  key: 'checkout-flow',
  options: [
    { value: 'single-page', label: 'Single Page Checkout' },
    { value: 'multi-step', label: 'Multi-Step Checkout' },
  ],
  async decide() {
    const userId = await getUserId();
    const variant = hashUserId(userId) % 2 === 0 
      ? 'single-page' 
      : 'multi-step';
    
    // Log to analytics
    await analytics.track('checkout_variant_assigned', {
      userId,
      variant,
    });
    
    return variant;
  },
});

// Usage
const variant = await checkoutFlow();

if (variant === 'single-page') {
  return <SinglePageCheckout />;
} else {
  return <MultiStepCheckout />;
}
```

### User Segment Targeting

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';

export const premiumFeatures = flag({
  key: 'premium-features',
  async decide() {
    const user = await getCurrentUser();
    
    // Enable for premium users
    if (user?.subscription === 'premium') {
      return true;
    }
    
    // Enable for beta testers
    if (user?.betaTester) {
      return true;
    }
    
    return false;
  },
});
```

### Geographic Targeting

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';
import { geolocation } from '@vercel/edge';

export const regionalFeature = flag({
  key: 'regional-feature',
  async decide() {
    const geo = geolocation();
    
    // Enable for US and Canada
    return ['US', 'CA'].includes(geo.country || '');
  },
});
```

### Time-Based Features

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';

export const holidaySale = flag({
  key: 'holiday-sale',
  async decide() {
    const now = new Date();
    const startDate = new Date('2024-12-20');
    const endDate = new Date('2024-12-31');
    
    return now >= startDate && now <= endDate;
  },
});
```

### Feature Flag with External API

```typescript
import { unstable_flag as flag, precompute } from '@vercel/flags/next';

export const dynamicFeature = flag({
  key: 'dynamic-feature',
  decide: precompute(async () => {
    const response = await fetch('https://api.example.com/features', {
      next: { revalidate: 60 }, // Cache for 60 seconds
    });
    
    const data = await response.json();
    return data.features.dynamicFeature.enabled;
  }),
});
```

### Multi-Variant Experiment

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';

export const buttonColor = flag({
  key: 'button-color',
  options: [
    { value: 'blue', label: 'Blue Button' },
    { value: 'green', label: 'Green Button' },
    { value: 'red', label: 'Red Button' },
  ],
  async decide() {
    const userId = await getUserId();
    const variants = ['blue', 'green', 'red'];
    const index = hashUserId(userId) % variants.length;
    
    return variants[index];
  },
});

// Track conversion
export async function trackConversion() {
  const variant = await buttonColor();
  
  await analytics.track('button_clicked', {
    variant,
    timestamp: Date.now(),
  });
}
```

## Integration

### Next.js App Router

```typescript
// app/flags/route.ts
import { type NextRequest } from 'next/server';
import { unstable_serialize as serialize } from '@vercel/flags/next';
import * as flags from '@/flags';

export async function GET(request: NextRequest) {
  return serialize({ flags });
}
```

```typescript
// app/layout.tsx
import { FlagsProvider } from '@vercel/flags/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <FlagsProvider>
          {children}
        </FlagsProvider>
      </body>
    </html>
  );
}
```

### SvelteKit

```typescript
// src/flags.ts
import { flag } from '@vercel/flags/sveltekit';

export const showNewFeature = flag({
  key: 'show-new-feature',
  decide: async () => false,
});
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { showNewFeature } from './flags';
  
  const isEnabled = await showNewFeature();
</script>

{#if isEnabled}
  <NewFeature />
{:else}
  <OldFeature />
{/if}
```

### Vercel Toolbar

```typescript
// next.config.js
module.exports = {
  experimental: {
    vercelToolbar: true,
  },
};
```

Access Flags Explorer at `/_vercel/flags` when running locally or in preview deployments.

### Analytics Integration

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';
import { track } from '@vercel/analytics';

export const experimentFlag = flag({
  key: 'experiment',
  options: [
    { value: 'control', label: 'Control' },
    { value: 'variant', label: 'Variant' },
  ],
  async decide() {
    const userId = await getUserId();
    const variant = hashUserId(userId) % 2 === 0 ? 'control' : 'variant';
    
    // Track variant assignment
    track('experiment_assigned', { variant, userId });
    
    return variant;
  },
});
```

### Vercel KV Storage

```typescript
import { unstable_flag as flag } from '@vercel/flags/next';
import { kv } from '@vercel/kv';

export const remoteFlag = flag({
  key: 'remote-flag',
  async decide() {
    const enabled = await kv.get<boolean>('feature:remote-flag');
    return enabled ?? false;
  },
});

// Update flag remotely
export async function updateFlag(enabled: boolean) {
  await kv.set('feature:remote-flag', enabled);
}
```

## Best Practices

### 1. Use Descriptive Keys

```typescript
// Good
export const showNewCheckoutFlow = flag({
  key: 'show-new-checkout-flow',
  // ...
});

// Avoid
export const flag1 = flag({
  key: 'f1',
  // ...
});
```

### 2. Document Flag Purpose

```typescript
/**
 * Controls the new checkout flow experiment
 * Target: 50% of users
 * Expected removal: Q2 2024
 */
export const newCheckoutFlow = flag({
  key: 'new-checkout-flow',
  async decide() {
    // ...
  },
});
```

### 3. Use Precompute for Static Data

```typescript
import { precompute } from '@vercel/flags/next';

export const staticFlag = flag({
  key: 'static-flag',
  decide: precompute(async () => {
    // This only runs at build time
    const config = await loadConfig();
    return config.enabled;
  }),
});
```

### 4. Handle Flag Cleanup

```typescript
// Create a flag registry
export const flagRegistry = {
  showNewFeature: {
    flag: showNewFeature,
    createdAt: '2024-01-01',
    expiresAt: '2024-06-01',
    owner: 'team-checkout',
  },
};

// Monitor old flags
export function getExpiredFlags() {
  const now = new Date();
  return Object.entries(flagRegistry)
    .filter(([_, meta]) => new Date(meta.expiresAt) < now);
}
```

### 5. Consistent Hashing for Experiments

```typescript
function consistentHash(userId: string, flagKey: string): number {
  const combined = `${userId}:${flagKey}`;
  let hash = 0;
  for (let i = 0; i < combined.length; i++) {
    hash = ((hash << 5) - hash) + combined.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash);
}

export const experiment = flag({
  key: 'my-experiment',
  async decide() {
    const userId = await getUserId();
    const percentage = consistentHash(userId, 'my-experiment') % 100;
    return percentage < 50; // 50% rollout
  },
});
```

### 6. Error Handling

```typescript
export const robustFlag = flag({
  key: 'robust-flag',
  async decide() {
    try {
      const response = await fetch('https://api.example.com/flags');
      const data = await response.json();
      return data.enabled;
    } catch (error) {
      console.error('Flag decision error:', error);
      // Return safe default
      return false;
    }
  },
});
```

### 7. Testing Flags

```typescript
// flags.test.ts
import { showNewFeature } from './flags';

describe('showNewFeature', () => {
  it('should return false by default', async () => {
    const result = await showNewFeature();
    expect(result).toBe(false);
  });
  
  it('should enable for premium users', async () => {
    mockUser({ subscription: 'premium' });
    const result = await showNewFeature();
    expect(result).toBe(true);
  });
});
```

## Troubleshooting

### Flags Not Updating

```typescript
// Check cache settings
export const cachedFlag = flag({
  key: 'cached-flag',
  decide: precompute(async () => {
    const response = await fetch('https://api.example.com/flags', {
      next: { revalidate: 10 }, // Revalidate every 10 seconds
    });
    return response.json();
  }),
});

// Force revalidation
import { revalidateTag } from 'next/cache';

export async function updateFlags() {
  revalidateTag('flags');
}
```

### Type Errors with Options

```typescript
// Ensure options are correctly typed
export const typedFlag = flag({
  key: 'typed-flag',
  options: [
    { value: 'option1' as const, label: 'Option 1' },
    { value: 'option2' as const, label: 'Option 2' },
  ],
  async decide(): Promise<'option1' | 'option2'> {
    return 'option1';
  },
});
```

### Flags Explorer Not Showing

```typescript
// Ensure experimental flag is enabled
// next.config.js
module.exports = {
  experimental: {
    vercelToolbar: true, // Required for Flags Explorer
  },
};

// Access at /_vercel/flags
```

### Hydration Errors

```typescript
// Use consistent flag values between server and client
'use client';

import { useFlag } from '@vercel/flags/react';
import { showNewFeature } from './flags';

export function HydrationSafeComponent() {
  const [mounted, setMounted] = useState(false);
  const isEnabled = useFlag(showNewFeature);
  
  useEffect(() => setMounted(true), []);
  
  if (!mounted) {
    return <LoadingPlaceholder />;
  }
  
  return isEnabled ? <NewFeature /> : <OldFeature />;
}
```

## See Also

- **vercel-platform** - Deploy flag-driven applications
- **vercel-ai-sdk** - A/B test AI features
- **cloudflare-workers** - Edge-based flag evaluation
- **vercel-workflow-sdk** - Workflow-based feature rollouts
