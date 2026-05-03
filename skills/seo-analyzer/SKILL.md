---
name: seo-analyzer
description: Audits web pages for on-page SEO best practices — title tags, meta descriptions, keyword density, Core Web Vitals, and structured data. Invoke when asked to audit SEO, improve search rankings, check on-page optimization, analyze page performance for search, or review structured data markup.
---

# SEO Analyzer

Performs comprehensive on-page SEO audits — evaluating title tags, meta descriptions, heading hierarchy, content quality, keyword optimization, internal linking, structured data, Core Web Vitals signals, and technical SEO factors — and delivers a prioritized action plan to improve search visibility.

## When to Use

- User asks to "audit SEO" or "check the SEO" on a page or website
- A page is ranking poorly and the cause needs to be identified
- New content needs to be optimized before publishing
- User wants to improve Core Web Vitals scores
- Technical SEO issues (crawlability, canonicalization, structured data errors) need diagnosis
- A competitor's page needs to be analyzed to understand why it ranks better
- User asks to add or validate schema.org structured data markup

## Process

1. **Define the audit scope**:
   - **Single page**: full deep audit
   - **Site-wide**: crawl all pages, surface issues by type and severity
   - **Keyword-focused**: evaluate a specific page against a target keyword
   - **Technical only**: crawlability, indexability, structured data, sitemaps
   - **Content quality**: evaluate topic depth, readability, and E-E-A-T signals

2. **On-page element analysis**:

   **Title tag**:
   - Length: 50–60 characters ideal (flag if <30 or >70)
   - Contains target keyword (ideally near the start)
   - Unique across the site (flag duplicates)
   - Compelling for click-through (value proposition or question hook)

   **Meta description**:
   - Length: 140–160 characters (flag if truncated in SERPs)
   - Contains target keyword naturally
   - Includes a clear call to action
   - Unique and not auto-generated

   **Heading hierarchy (H1–H6)**:
   - One H1 per page, containing the primary keyword
   - Logical hierarchy: H1 → H2 → H3 (no skipped levels)
   - H2s cover main topics the page targets
   - Headings are descriptive, not generic ("Overview" → "How X Works in 2025")

   **URL structure**:
   - Short, readable, hyphen-separated
   - Contains the primary keyword
   - No unnecessary parameters, session IDs, or uppercase letters
   - HTTPS enforced

3. **Content quality analysis**:
   - **Word count**: appropriate for content type (informational pages: 1,200–2,500 words typical)
   - **Keyword usage**: target keyword in first 100 words, natural density (0.5–2%), not stuffed
   - **LSI/semantic terms**: related terms that demonstrate topical depth
   - **Readability**: Flesch-Kincaid score — flag if below 50 (too complex for general audience)
   - **E-E-A-T signals**: author bio, publication date, citations, expertise indicators
   - **Content freshness**: publication/update date visible; stale content (>2 years on fast-moving topics) flagged

4. **Technical SEO checks**:
   - **Canonical tag**: present, self-referencing (unless paginated), no conflicting canonicals
   - **Robots meta tag**: check for accidental `noindex` or `nofollow` on important pages
   - **Structured data**: detect existing schema.org markup; validate against Google's guidelines; check for errors
   - **Image optimization**: alt text present and descriptive, images compressed (flag files >200 KB), WebP format preferred
   - **Internal links**: minimum 2–3 relevant internal links per page; check for broken internal links
   - **Page speed signals**: detect render-blocking resources, large JavaScript bundles, missing lazy loading

5. **Core Web Vitals assessment**:
   - **LCP (Largest Contentful Paint)**: flag if >2.5s (identify the LCP element)
   - **INP (Interaction to Next Paint)**: flag if >200ms
   - **CLS (Cumulative Layout Shift)**: flag if >0.1 (identify shifting elements)
   - Source: use PageSpeed Insights API or Lighthouse data if available; otherwise note that real-user data is needed

6. **SERP feature opportunities**:
   - Identify if the page could earn: featured snippet, FAQ, How-To, review stars, sitelinks, video carousel
   - Note schema types needed to qualify for each opportunity

7. **Prioritized recommendations**:
   - Classify each finding: 🔴 Critical (indexing/crawl issues, missing H1) → 🟡 High impact (title, meta, Core Web Vitals) → 🟢 Medium (content depth, internal links) → 💬 Minor (formatting, minor copy tweaks)
   - Order by estimated effort vs. impact
   - Provide concrete fix instructions for each finding

## Output Format

```
## SEO Audit Report
**URL:** https://example.com/product/widget-pro
**Target Keyword:** "best project management software for small teams"
**Audit Date:** June 1, 2025

### Overall Score: 62/100

---

### 🔴 Critical Issues (fix immediately)

**1. Missing H1 Tag**
The page has no H1 element. H1 is the primary on-page signal for search engines to understand the page topic.
✅ Fix: Add `<h1>Best Project Management Software for Small Teams in 2025</h1>` at the top of the content.

**2. Page Not Indexable — robots meta tag**
`<meta name="robots" content="noindex">` found. This page is excluded from search indexing.
✅ Fix: Remove the noindex directive or change to `<meta name="robots" content="index, follow">`.

---

### 🟡 High Impact Issues

**3. Title Tag Too Short (28 characters)**
Current: "Widget Pro | Product"
Ideal length: 50–60 characters. Missing target keyword.
✅ Fix: "Widget Pro: Best Project Management for Small Teams"

**4. LCP: 4.2 seconds (Poor)**
LCP element: Hero image (1.8 MB PNG). Target: ≤ 2.5s.
✅ Fix: Convert to WebP format, serve via CDN, add `loading="eager"` and explicit dimensions.

---

### 🟢 Medium Issues

**5. No Internal Links to Key Service Pages**
0 internal links from this page to other pages. Minimum recommended: 3–5.
✅ Fix: Add contextual links to pricing page, features comparison, and customer case studies.

**6. Missing FAQ Schema**
Page contains FAQ-style content but no FAQ schema markup. Adding it could earn a featured snippet.
✅ Fix: Add FAQ schema using JSON-LD for the Q&A section.

---

### Summary
| Priority | Issues | Estimated Impact |
|----------|--------|-----------------|
| 🔴 Critical | 2 | Immediate ranking recovery |
| 🟡 High | 3 | +15–30% click-through improvement |
| 🟢 Medium | 4 | Incremental gains over 60–90 days |
```

## Examples

### Example Input
```
Audit the SEO for this blog post. Target keyword: "how to write a business plan". Here's the HTML: [...]
```

### Example Output
```
SEO Audit — "How to Write a Business Plan"
Target keyword: "how to write a business plan"

Title: "Writing Business Plans — A Complete Guide" (46 chars) ✅ length OK ⚠️ keyword not exact-match
H1: "A Complete Guide to Writing Business Plans" ✅ (present, contains keyword)
Meta description: Missing ❌ — add 140–160 char description with keyword + CTA
Content: 1,840 words ✅ | Keyword in first 100 words ✅ | Keyword density: 1.2% ✅
Images: 3 images — 2 missing alt text ⚠️
Internal links: 1 (low) ⚠️ — add 2–3 more

Top Recommendation: Add meta description. It is the single highest-impact fix with the least effort.
```

## Boundaries

- SEO audits are based on current best practices and public guidelines (Google Search Central, Core Web Vitals docs) — search algorithm specifics are not publicly documented and recommendations are evidence-based, not guaranteed.
- Do NOT make promises about specific ranking positions or timelines — SEO results depend on many factors outside this audit's scope.
- For Core Web Vitals, distinguish between lab data (Lighthouse, simulated) and field data (CrUX, real users) — they can differ significantly.
- Do NOT recommend black-hat tactics: keyword stuffing, hidden text, link schemes, or cloaking.
- Structured data recommendations must comply with Google's schema.org guidelines; invalid or misleading schema can result in manual actions.
- When auditing competitor pages, only analyze publicly accessible content — do not attempt to access login-gated analytics or internal tools.
