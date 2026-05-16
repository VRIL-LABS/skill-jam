---
name: website-building-css-and-tailwind
description: CSS and Tailwind guidance — Tailwind v4 for Next.js 16+, Tailwind v3 for legacy/template projects, shadcn/ui component system, and cutting-edge CSS.
---

# CSS & Tailwind

Modern CSS features, Tailwind CSS (v3 and v4), shadcn/ui component system, and cutting-edge CSS.

---

## Tailwind CSS — Version Selection

**Tailwind CSS v4** is now the current stable version (v4.0.4+, released January 2025). It uses a CSS-first configuration approach with no `tailwind.config.ts` needed.

| Project Type | Tailwind Version | Reason |
|---|---|---|
| **Next.js 16+** (new projects) | **v4** — use `@import "tailwindcss"` + `@theme` | Next.js 16 ships with Tailwind v4 by default |
| **Legacy/template projects** (webapp template, older Next.js) | **v3** — use `tailwind.config.ts` + `@tailwind` directives | Template is pre-wired for v3; v4 will crash the dev server |
| **React Native (NativeWind)** | **v3** — NativeWind v4 uses Tailwind v3 under the hood | NativeWind v4 does not yet support Tailwind v4 |

---

## Tailwind v4 — Next.js 16+ Projects

Tailwind v4 uses a radically simpler, CSS-first approach. No `tailwind.config.ts` needed.

### Installation

```bash
# For Next.js 16+ (uses @tailwindcss/postcss under the hood — zero config needed)
npm install tailwindcss@latest

# For Vite-based projects
npm install tailwindcss@latest @tailwindcss/vite
```

### CSS Entry Point

```css
/* globals.css — replace the old @tailwind directives with a single import */
@import "tailwindcss";
```

No `@tailwind base; @tailwind components; @tailwind utilities;` directives needed.

### Theme Customization via `@theme`

All design token overrides go in `@theme` in CSS — no config file:

```css
@import "tailwindcss";

@theme {
  /* Type scale — fluid with clamp() */
  --font-size-xs:   clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --font-size-sm:   clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --font-size-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --font-size-lg:   clamp(1.125rem, 1rem + 0.75vw, 1.5rem);
  --font-size-xl:   clamp(1.5rem, 1.2rem + 1.25vw, 2.25rem);
  --font-size-2xl:  clamp(2rem, 1.2rem + 2.5vw, 3.5rem);
  --font-size-hero: clamp(3rem, 0.5rem + 7vw, 8rem);

  /* Nexus color palette */
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
```

### Dark Mode in v4

**Media-based (system preference):**
```css
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

**Class-based (manual toggle):**
```css
@variant dark (.dark &) {
  --color-background: #171614;
}
```

Then toggle `dark` class on `<html>`:
```tsx
<html lang="en" className={isDark ? "dark" : ""}>
```

### v4 Compatibility Notes

- `@apply` still works in v4
- Arbitrary values (`text-[clamp(1rem,3vw,2rem)]`) still work
- `@tailwindcss/vite` is faster than PostCSS plugin for Vite projects; both work
- Automatic content detection — no `content` array needed

---

## Tailwind v3 (Legacy/Template Projects)

All legacy and webapp template projects use **Tailwind CSS v3** with a `tailwind.config.ts` and PostCSS. Do NOT use Tailwind v4 syntax (`@import "tailwindcss"`, `@theme`) — it is incompatible with the webapp template and will crash the dev server. Stick to v3 patterns throughout.

### CSS Directives

Use the `@tailwind` directives — **not** `@import "tailwindcss"`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Configuration via `tailwind.config.ts`

Tailwind uses a config file for customization. The template's config extends colors via CSS custom properties with the HSL `<alpha-value>` pattern:

```ts
// tailwind.config.ts (already in template — extend, don't replace)
import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./client/index.html", "./client/src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background) / <alpha-value>)",
        foreground: "hsl(var(--foreground) / <alpha-value>)",
        primary: {
          DEFAULT: "hsl(var(--primary) / <alpha-value>)",
          foreground: "hsl(var(--primary-foreground) / <alpha-value>)",
        },
        // ... full color map in template
      },
    },
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
} satisfies Config;
```

### HSL Color Variable Format

When defining custom properties in `index.css`, use **space-separated H S% L%** (no `hsl()` wrapper):

```css
:root {
  --background: 45 24% 96%;
  --foreground: 44 23% 14%;
  --primary: 183 98% 22%;
  --primary-foreground: 0 0% 98%;
}

.dark {
  --background: 40 10% 8%;
  --foreground: 40 3% 80%;
  --primary: 188 35% 47%;
  --primary-foreground: 0 0% 98%;
}
```

The `hsl(var(--primary) / <alpha-value>)` pattern in the config wraps these values at build time, enabling Tailwind's opacity modifier syntax (`bg-primary/50`).

### Dark Mode

Dark mode uses the `.dark` class strategy:

1. Set `darkMode: ["class"]` in `tailwind.config.ts`
2. Define `:root` (light) and `.dark` (dark) variable sets in `index.css`
3. Toggle the `dark` class on `document.documentElement`
4. Use `dark:` prefix for one-off overrides: `className="bg-white dark:bg-black"`

### Key Features

- `@apply` in CSS for reusable utility compositions
- Group/peer modifiers: `group-hover:opacity-100`, `peer-checked:translate-x-full`
- Arbitrary values: `text-[clamp(1rem,3vw,2rem)]`, `grid-cols-[200px_1fr]`
- Arbitrary variants: `[&:nth-child(odd)]:bg-surface`
- `motion-safe:` and `motion-reduce:` for respecting `prefers-reduced-motion`
- Ring utilities for focus indication: `focus:ring-2 focus:ring-primary`

### Elevation System (Webapp Template)

The template includes a custom elevation system for interactive states. Instead of traditional shadows, it uses overlay-based brightness adjustment:

```html
<!-- Hover brightness -->
<div class="hover-elevate">Brightens on hover</div>

<!-- Active press state -->
<button class="active-elevate-2">Darkens on press</button>

<!-- Toggle state (e.g., selected tab) -->
<div class="toggle-elevate toggle-elevated">Currently active</div>
```

This system works in both light and dark mode via `--elevate-1` / `--elevate-2` CSS variables (light mode uses `rgba(0,0,0,…)`, dark mode uses `rgba(255,255,255,…)`).

**When using Tailwind, handle container queries, arbitrary properties, stateful variants, and responsive design entirely in markup.** Minimize context-switches between HTML and CSS files.

---

## shadcn/ui — The Component System

shadcn/ui is the standard component system for React projects. It is not a dependency you install — it copies source code into your project, giving you full ownership and zero version lock-in. Components are built on Radix UI primitives (accessible, keyboard-navigable, WAI-ARIA compliant) and styled with Tailwind CSS.

**When to use shadcn/ui:**
- The project uses React (Next.js, Remix, Vite, Astro with React)
- You need interactive components: dialogs, dropdowns, tabs, popovers, command palettes, data tables, accordions, tooltips, sheets, toasts
- You want accessibility handled correctly out of the box — focus management, keyboard nav, screen reader support
- You'd rather customize source code than fight a library's theming API

**When NOT to use it:**
- Vanilla HTML/CSS/JS projects — shadcn/ui is React-only. For non-React projects, build components from scratch using the base CSS, Tailwind, and the Popover/Dialog APIs from native HTML
- Simple landing pages with no interactive UI beyond links and scroll — the overhead isn't worth it

**Most projects are vanilla HTML** (static to S3, no build step). Only use shadcn when the user requests React or the project needs complex interactive components (data tables, command palettes, drawers). Landing pages, portfolios, editorial → build by hand.

### Setup — Webapp Template (Pre-installed)

The webapp template ships with shadcn pre-installed (52 components in `client/src/components/ui/`). No setup needed — just import and use:

```tsx
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
```

To add additional components not in the template:
```bash
npx shadcn@latest add command tooltip accordion
```

### Setup — From Scratch

For non-template React projects:
```bash
npm create vite@latest myapp -- --template react-ts
cd myapp && npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npx shadcn@latest init
# Choose: New York style (smaller, shadow-based — matches this skill's aesthetic)
```

Then add components as needed:
```bash
npx shadcn@latest add button dialog dropdown-menu tabs tooltip
```

### Theming — Bridge shadcn/ui to Design Tokens

shadcn/ui uses its own CSS variable naming convention. Map your palette to shadcn's expected variables in `index.css` using **space-separated HSL** (no `hsl()` wrapper) so both systems work together:

```css
:root {
  /* Nexus light → shadcn variables (H S% L% format) */
  --background: 45 24% 96%;       /* --color-bg #F7F6F2 */
  --foreground: 44 23% 14%;       /* --color-text #28251D */
  --card: 45 25% 97%;             /* --color-surface #F9F8F5 */
  --card-foreground: 44 23% 14%;
  --primary: 183 98% 22%;         /* --color-primary #01696F */
  --primary-foreground: 0 0% 98%;
  --muted-foreground: 50 3% 47%;  /* --color-text-muted #7A7974 */
  --destructive: 320 57% 40%;     /* --color-error #A12C7B */
  --border: 36 8% 81%;            /* --color-border #D4D1CA */
  --ring: 183 98% 22%;
}
```

This way, every shadcn/ui component automatically inherits the skill's color system, including dark mode.

### Key Components and When to Reach for Them

| Component | When to use |
|---|---|
| `Button` | All clickable actions. Use the variant system (default, secondary, outline, ghost, destructive) |
| `Dialog` / `Sheet` | Modal content. Dialog for centered, Sheet for slide-from-edge |
| `DropdownMenu` | Context menus, action menus on cards/rows |
| `Command` | Command palette (⌘K). Pairs with `Dialog` for a spotlight search |
| `Tabs` | Switching between views in a contained area |
| `Tooltip` | Hover hints for icon-only buttons and truncated text |
| `Table` + `DataTable` | Data-heavy layouts. Built on TanStack Table for sort/filter/pagination |
| `Form` | Any multi-field form. Built on React Hook Form + Zod validation |
| `Popover` | Floating content anchored to a trigger — filters, pickers, mini-panels |
| `Toast` / `Sonner` | Non-blocking feedback. Use for background confirmations, not critical errors |
| `Accordion` | Progressive disclosure. FAQ sections, settings panels |
| `Card` | Content containers with consistent padding, border, and radius |

**Principles:**
- **Add only what you use.** Each `add` command copies one component. Don't bulk-install everything — keep the project lean.
- **Customize after copying.** The whole point is that you own the code. Adjust the Tailwind classes, swap out Radix primitives, add motion — it's your file.
- **Compose upward.** Build semantic components from shadcn primitives: a `<UserCard>` that composes `Card` + `Avatar` + `Badge`, a `<ConfirmDialog>` that wraps `Dialog` with standard confirm/cancel actions.
- **Use the 180ms golden curve on all interactive states** within shadcn components — override any default transitions to use `var(--transition-interactive)`.

---

## Modern CSS Features (Well-Supported, Use Freely)

**90%+ support (use freely):** CSS Nesting, `oklch()`/`oklab()`, container queries, `@layer`, `@property`, `clamp()`, `color-mix()`, `:has()`, Popover API, `subgrid`, `content-visibility`, `text-wrap: balance`.

**80-90% (use with fallbacks):** Scroll-driven animations, view transitions, `@starting-style`, Anchor Positioning, `text-wrap: pretty`.

---

## Cutting-Edge CSS (Interop 2026)

Use with `@supports` fallbacks:

**`contrast-color()`** — auto-accessible text: `color: contrast-color(var(--color-primary))`. Safari first, cross-browser via Interop 2026.

**Advanced `attr()` typing** (Chrome 133+) — data attributes as CSS values:
```css
.chip { background-color: attr(data-color type(<color>)); }
.bar  { width: calc(attr(data-value type(<number>)) * 1%); }
```

**`shape()`** — responsive clip-paths with %, vw, calc (unlike pixel-only `path()`).

**`sibling-index()`** — CSS-only staggered animations: `animation-delay: calc(sibling-index() * 60ms)`.
