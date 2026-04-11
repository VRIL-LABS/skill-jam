---
name: accessibility-auditor
description: Scans frontend code and rendered HTML for WCAG 2.1 compliance issues — missing alt text, color contrast, ARIA roles, keyboard navigation. Invoke when asked to check accessibility, audit WCAG compliance, find a11y issues, improve screen reader support, or ensure keyboard navigation works.
---

# Accessibility Auditor

Audits frontend source code and HTML for WCAG 2.1 (AA) compliance issues — identifying missing alt text, insufficient color contrast, improper ARIA usage, keyboard navigation gaps, focus management problems, and semantic HTML violations — with prioritized, actionable remediations.

## When to Use

- User asks to "check accessibility", "audit for a11y issues", or "ensure WCAG compliance"
- A new UI component needs to be verified before shipping
- Screen reader users are reporting issues
- An accessibility audit has been requested (legal compliance, VPAT)
- User asks about ARIA roles, focus management, or keyboard navigation
- Color contrast or font size concerns are raised

## Process

1. **Identify the source type**:
   - HTML source or rendered output
   - React/JSX components
   - Vue/Svelte/Angular templates
   - CSS (for color contrast and focus styles)

2. **Audit against WCAG 2.1 success criteria** organized by the four POUR principles:

   **Perceivable (users can perceive all content)**
   - 1.1.1 Non-text Content: Every `<img>`, `<svg>`, icon button, and canvas needs `alt` text or `aria-label`; decorative images need `alt=""`
   - 1.3.1 Info and Relationships: Use semantic HTML (`<nav>`, `<main>`, `<header>`, `<aside>`, `<section>`, headings hierarchy `h1→h2→h3`)
   - 1.3.3 Sensory Characteristics: Don't rely on color alone to convey information (add icons, patterns, or text labels)
   - 1.4.1 Use of Color: Ensure information is not conveyed by color alone
   - 1.4.3 Contrast (Minimum): Text contrast ratio ≥ 4.5:1 (AA), large text ≥ 3:1
   - 1.4.4 Resize Text: Content must be usable at 200% zoom without loss of functionality
   - 1.4.10 Reflow: Content must not require horizontal scrolling at 320px width

   **Operable (users can operate the interface)**
   - 2.1.1 Keyboard: All functionality available via keyboard; no keyboard traps
   - 2.1.2 No Keyboard Trap: Focus must be able to leave any component
   - 2.4.1 Bypass Blocks: Provide skip navigation link to main content
   - 2.4.3 Focus Order: Focus moves in a logical, meaningful order
   - 2.4.4 Link Purpose: Link text describes the destination (not "click here")
   - 2.4.7 Focus Visible: Keyboard focus indicator must be clearly visible
   - 2.5.3 Label in Name: Visible label text must be included in accessible name

   **Understandable (users can understand the content)**
   - 3.1.1 Language of Page: `<html lang="en">` (or appropriate language code) must be set
   - 3.2.1 On Focus: No unexpected context changes when an element receives focus
   - 3.3.1 Error Identification: Form errors identified in text, not just color
   - 3.3.2 Labels or Instructions: Form inputs must have associated `<label>` elements

   **Robust (content can be interpreted by assistive technologies)**
   - 4.1.1 Parsing: Valid HTML — no duplicate IDs, properly nested elements
   - 4.1.2 Name, Role, Value: Custom widgets must have correct ARIA roles, states, and properties
   - 4.1.3 Status Messages: Live regions (`aria-live`, `role="status"`) for dynamic content

3. **Audit ARIA usage**:
   - Verify ARIA roles are used correctly (don't add `role="button"` to a native `<button>`)
   - `aria-label` / `aria-labelledby` present for elements without visible text
   - `aria-expanded`, `aria-selected`, `aria-checked` state managed correctly for interactive widgets
   - `aria-hidden="true"` not applied to focusable elements

4. **Check interactive component patterns**:
   - Modals/dialogs: focus trapped inside when open, returns to trigger on close, `role="dialog"`, `aria-modal="true"`
   - Dropdowns/menus: keyboard navigation (arrows), `role="menu"`, `role="menuitem"`
   - Tabs: `role="tablist"`, `role="tab"`, `aria-selected`, arrow key navigation
   - Carousels/sliders: pause mechanism, keyboard controls

5. **Categorize findings** by WCAG level (A / AA / AAA) and severity.

## Output Format

```
## Accessibility Audit Report

**Standard:** WCAG 2.1 Level AA
**Component:** `ProductCard.tsx`
**Findings:** 🔴 3 critical · 🟡 2 warnings · 🟢 2 enhancements

---

### 🔴 Critical — Missing alt text (WCAG 1.1.1, Level A)
**Element:** `<img src={product.imageUrl} />`

All product images lack alt text. Screen readers will announce the filename.

**Fix:**
```jsx
<img src={product.imageUrl} alt={product.name} />
// For decorative images:
<img src={decorativeBackground} alt="" role="presentation" />
```

---

### 🔴 Critical — Button has no accessible name (WCAG 4.1.2, Level A)
**Element:** `<button onClick={onAddToCart}><CartIcon /></button>`

Icon-only buttons need an accessible label.

**Fix:**
```jsx
<button onClick={onAddToCart} aria-label={`Add ${product.name} to cart`}>
  <CartIcon aria-hidden="true" />
</button>
```

---

### 🟡 Warning — Insufficient color contrast (WCAG 1.4.3, Level AA)
**Element:** `.product-price` — `color: #aaa` on white background
**Contrast ratio:** 2.32:1 (required: 4.5:1)

**Fix:** Change to `color: #767676` (minimum 4.54:1) or darker.
```

## Examples

### Example Input
```html
<div onclick="navigate('/product/1')" style="color: #ccc">
  View Product
</div>
<img src="shoe.jpg">
<input type="text" placeholder="Search...">
```

### Example Output
```
🔴 Critical — Interactive element is not keyboard accessible (WCAG 2.1.1)
A <div> with onclick is not focusable or operable by keyboard.
Fix: Use <button> or <a href> instead.

🔴 Critical — Image missing alt text (WCAG 1.1.1)
<img src="shoe.jpg"> has no alt attribute.
Fix: <img src="shoe.jpg" alt="White running shoe">

🟡 Warning — Input missing associated label (WCAG 1.3.1)
Placeholder text is not a substitute for a <label>.
Fix: <label for="search">Search</label> <input id="search" type="text">

🟡 Warning — Insufficient contrast on text (WCAG 1.4.3)
#ccc on white = 1.6:1 ratio (required: 4.5:1)
```

## Boundaries

- Do NOT audit color contrast without the actual color values — `color: var(--text-muted)` requires resolving the CSS variable.
- Do NOT audit rendered behavior (focus trapping, live regions) from static source alone — note when dynamic behavior must be tested with a screen reader (NVDA, JAWS, VoiceOver) or automated tool (axe-core, Lighthouse).
- Do NOT recommend `aria-*` attributes as a substitute for semantic HTML — prefer native elements.
- Do NOT recommend removing ARIA attributes that are correctly implemented — only flag incorrect usage.
- WCAG AAA criteria are optional for most compliance requirements — focus on A and AA unless AAA is specified.
- If the codebase uses a design system, check if the design system components are already accessible before flagging usage-level issues.
