---
name: website-building-nextjs
description: Next.js 16+ specific guidance — app router, Tailwind v4, shadcn/ui, deployment to Vercel. Use alongside the parent website-building skill.
user-invocable: false
---

# Next.js 16+ — Setup & Design System

Guidance specific to **Next.js 16+** web projects. Read this alongside the parent `website-building` skill's shared design files.

## Version Requirements

- **Next.js**: 16.x (current LTS — released October 2025)
- **React**: 19.2
- **Node.js**: 20.9+ (required by Next.js 16)
- **TypeScript**: 5.1+
- **Tailwind CSS**: v4.0.4+ (recommended for new Next.js 16 projects)

## Creating a New Next.js 16 Project

```bash
npx create-next-app@latest my-app
# Choose: TypeScript ✓, ESLint ✓, Tailwind CSS ✓, App Router ✓, Turbopack ✓
cd my-app
npm run dev
```

This scaffolds a project with:
- App Router (`app/` directory)
- Turbopack (default bundler — 2-5× faster than Webpack)
- Tailwind CSS v4
- TypeScript

## Project Structure (App Router)

```
my-app/
├── app/
│   ├── layout.tsx          # Root layout (wraps all pages)
│   ├── page.tsx            # Home page (/)
│   ├── globals.css         # Tailwind + custom CSS vars
│   ├── (marketing)/        # Route group (no URL segment)
│   │   ├── about/page.tsx
│   │   └── blog/page.tsx
│   └── dashboard/
│       ├── layout.tsx      # Nested layout
│       └── page.tsx
├── components/
│   └── ui/                 # shadcn/ui components
├── lib/
│   └── utils.ts
├── public/
└── next.config.ts
```

## Tailwind CSS v4 with Next.js 16

Next.js 16 ships with Tailwind v4. The setup is radically simpler than v3.

### CSS Entry Point (`app/globals.css`)

```css
@import "tailwindcss";

/* Design token overrides using @theme */
@theme {
  /* Type scale — fluid with clamp() */
  --font-size-xs:   clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --font-size-sm:   clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --font-size-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --font-size-lg:   clamp(1.125rem, 1rem + 0.75vw, 1.5rem);
  --font-size-xl:   clamp(1.5rem, 1.2rem + 1.25vw, 2.25rem);
  --font-size-2xl:  clamp(2rem, 1.2rem + 2.5vw, 3.5rem);
  --font-size-hero: clamp(3rem, 0.5rem + 7vw, 8rem);

  /* Nexus color palette — light mode */
  --color-background: #F7F6F2;
  --color-surface: #F9F8F5;
  --color-border: #D4D1CA;
  --color-text: #28251D;
  --color-text-muted: #7A7974;
  --color-primary: #01696F;
  --color-primary-hover: #0C4E54;
  --color-error: #A12C7B;

  /* Spacing */
  --spacing-unit: 4px;
  
  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-xl: 24px;
}

/* Dark mode via @variant */
@variant dark {
  --color-background: #171614;
  --color-surface: #1C1B19;
  --color-border: #393836;
  --color-text: #CDCCCA;
  --color-text-muted: #797876;
  --color-primary: #4F98A3;
  --color-primary-hover: #227F8B;
}
```

### Key Differences from Tailwind v3

| v3 | v4 |
|---|---|
| `tailwind.config.ts` for all config | CSS-first: `@theme` in CSS |
| `@tailwind base; @tailwind components; @tailwind utilities;` | `@import "tailwindcss";` |
| Manual `content` array | Automatic content detection |
| `darkMode: ["class"]` in config | `@variant dark (.dark &)` or `@variant dark` (media) |
| Arbitrary values with `[]` | Same syntax, extended in v4 |
| `@apply` still works | `@apply` still works |

### Dark Mode in v4

**Class-based (manual toggle):**
```css
@variant dark (.dark &) {
  --color-background: #171614;
}
```

Then toggle `dark` class on `<html>`:
```tsx
// app/layout.tsx
<html lang="en" className={isDark ? "dark" : ""}>
```

**Media-based (system preference):**
```css
@variant dark {
  --color-background: #171614;
}
```

## shadcn/ui with Next.js 16

shadcn/ui works seamlessly with Next.js 16 and Tailwind v4.

### Setup

```bash
npx shadcn@latest init
# Chooses: New York style, Tailwind v4 config
```

Then add components:
```bash
npx shadcn@latest add button dialog dropdown-menu tabs card
```

Components install to `components/ui/` — you own the code.

### Server vs Client Components

shadcn/ui components that use hooks (state, refs, event handlers) are Client Components. Mark them `"use client"` or wrap in a client boundary:

```tsx
// components/theme-toggle.tsx
"use client"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  // useState, useEffect are allowed here
}
```

Pure display shadcn components (Card, Badge, Table) can be used in Server Components without the directive.

## Next.js 16 Key Patterns

### App Router Layouts

```tsx
// app/layout.tsx — Root layout (Server Component)
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "My App",
  description: "Built with Next.js 16",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

### Caching — `"use cache"` Directive (New in Next.js 16)

Next.js 16 replaces implicit caching with explicit opt-in:

```tsx
// Cached server function
async function getProducts() {
  "use cache"
  const res = await fetch("https://api.example.com/products")
  return res.json()
}

// Cached page — revalidate every hour
export default async function ProductsPage() {
  "use cache"
  cacheLife("1h")
  const products = await getProducts()
  return <ProductList products={products} />
}
```

### proxy.ts — Replaces middleware.ts

```ts
// proxy.ts (was: middleware.ts)
import type { NextRequest } from "next/server"
import { NextResponse } from "next/server"

export function proxy(request: NextRequest) {
  if (!request.cookies.get("auth")) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
}

export const config = {
  matcher: "/dashboard/:path*",
}
```

### Server Components vs Client Components

```tsx
// Server Component (default — no directive needed)
// Can: fetch data, access DB, read env vars
// Cannot: useState, useEffect, event handlers, browser APIs
async function ServerPage() {
  const data = await fetchFromDB() // Direct DB access OK
  return <ClientUI initialData={data} />
}

// Client Component
"use client"
function ClientUI({ initialData }) {
  const [state, setState] = useState(initialData)
  return <button onClick={() => setState(null)}>...</button>
}
```

### Image Optimization

```tsx
import Image from "next/image"

// Always use next/image — never <img> in Next.js
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1280}
  height={720}
  priority // Add for LCP images (above the fold)
  className="rounded-lg object-cover"
/>
```

### Font Optimization

```tsx
// app/layout.tsx
import { Satoshi } from "next/font/local"
// or from Google Fonts:
import { DM_Sans } from "next/font/google"

const dmSans = DM_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
})

// Use in layout:
// <body className={dmSans.variable}>
```

## Design Guidance — Next.js Projects

### When Using the App Router

- **Server Components first** — only add `"use client"` where interactivity is needed
- **Design tokens via CSS variables** — define in `globals.css` under `@theme`, use throughout
- **CSS Modules for component-scoped styles** — `Button.module.css` alongside `Button.tsx`
- **Tailwind v4 for utility classes** — no config file needed, just `@import "tailwindcss"` + `@theme` for overrides

### Deployment to Vercel (Recommended)

```bash
# One-command deploy
npx vercel
```

Next.js is made by Vercel — zero-config deployment. Image optimization, Edge Network CDN, and ISR work out of the box.

**Build for self-hosting:**
```bash
# next.config.ts
export default {
  output: "standalone" // Docker-ready bundle
}
```

### Performance Targets (Next.js)

- **LCP < 2.0s** — Use `priority` on LCP images, `next/font` for font loading
- **CLS < 0.05** — Always set `width`/`height` on images
- **INP < 150ms** — Keep Client Components thin; heavy computation in Server Components
- **Bundle size** — Turbopack tree-shakes automatically; check with `npm run build` output

## Checklist for Next.js 16 Projects

- [ ] Using `create-next-app@latest` with App Router + Turbopack + Tailwind CSS
- [ ] `globals.css` has `@import "tailwindcss"` (not v3 directives)
- [ ] `@theme` block defines design tokens (colors, fonts, spacing)
- [ ] `"use client"` only on components that need it
- [ ] Images use `next/image` with `width`/`height` and `priority` on LCP
- [ ] Fonts via `next/font` (not raw `<link>` tags)
- [ ] `proxy.ts` for auth/routing (not `middleware.ts`)
- [ ] `"use cache"` directive on data-fetching functions
- [ ] shadcn/ui initialized with `npx shadcn@latest init`
- [ ] Dark mode implemented (class-based or media-based via `@variant dark`)
