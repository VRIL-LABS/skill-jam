---
name: competitive-intelligence
description: Monitors competitor websites, pricing, product launches, and job postings to surface strategic insights. Invoke when asked to research competitors, analyze the competitive landscape, track what a competitor is doing, or gather market intelligence.
---

# Competitive Intelligence

Systematically monitors and analyzes competitor activity — including product changes, pricing updates, job postings, marketing messaging, customer reviews, and public financial signals — to surface strategic insights and actionable intelligence for product, sales, and executive teams.

## When to Use

- User asks to research a competitor or "what is [Company X] doing?"
- A competitive landscape analysis is needed for a market, product, or strategy decision
- Pricing strategy requires benchmarking against competitor offerings
- User wants to track a competitor's product launches, feature releases, or website changes
- Job posting analysis is needed to understand a competitor's investment priorities
- Customer review sentiment about competitors needs to be analyzed
- User asks for a competitive battlecard or sales comparison sheet

## Process

1. **Define the intelligence requirements**:
   - **Target competitors**: specific companies to monitor, or ask for help identifying the main competitors in a space
   - **Intelligence domains**: pricing, product, messaging, hiring, customer sentiment, financial, partnerships, marketing
   - **Time horizon**: point-in-time analysis vs. ongoing monitoring
   - **Use case**: product roadmap input, sales battlecard, M&A diligence, market sizing, pricing strategy

2. **Identify and validate competitors**:
   - Confirm that the listed companies are direct competitors (same ICP, overlapping features/services)
   - Distinguish: direct competitors (same product category), indirect competitors (alternative solutions), and emerging threats (different approach to the same problem)
   - Source the competitor list from: industry reports, G2/Capterra categories, LinkedIn "people also viewed", investor portfolios

3. **Collect competitor data by domain**:

   **Product intelligence**:
   - Current product/feature set from their website, documentation, and changelog
   - Recent product announcements from press releases, blog posts, and release notes
   - Known integrations and partnership ecosystems

   **Pricing intelligence**:
   - Public pricing pages (tiers, limits, pricing model: per-seat, usage-based, flat-rate)
   - Free trial / freemium availability
   - Enterprise pricing signals from job postings ("$1M+ deal experience") or Glassdoor reviews
   - Price change history if available

   **Messaging intelligence**:
   - Value proposition from hero section and homepage copy
   - Target customer segment from messaging ("for enterprise teams", "built for developers")
   - Key differentiators and marketing claims
   - Recent ad copy or campaign themes

   **Hiring intelligence**:
   - Current job postings: volume, locations, departments (engineering volume → product investment signal)
   - Recent spikes in hiring in a specific team → strategic priority signal
   - Leadership hires: new VP/C-suite from specific companies or backgrounds → strategic direction signal

   **Customer sentiment**:
   - G2, Capterra, Trustpilot reviews: average rating, top pros/cons, common complaints
   - App store reviews (if mobile product)
   - Reddit or community forum discussion

   **Financial / growth signals** (for public companies or funded startups):
   - Recent funding rounds, investors, valuation
   - Revenue estimates from Crunchbase, PitchBook, or analyst reports
   - Employee count growth trend (LinkedIn headcount) as a proxy for growth

4. **Analyze and synthesize**:
   - Identify each competitor's primary strengths and weaknesses
   - Map the competitive landscape: where do you differentiate vs. where are you at parity or behind?
   - Detect recent strategic shifts: new market entries, pricing changes, partnership announcements
   - Flag emerging threats or white-space opportunities competitors are not addressing

5. **Produce structured deliverables**:
   - **Competitive landscape overview**: summary table across all tracked competitors
   - **Individual competitor profile**: deep dive on one company
   - **Battlecard**: sales-ready one-page comparison for a specific competitor
   - **Trend digest**: what changed in the past 30 days across all tracked competitors

## Output Format

### Competitive Landscape Summary
```
## Competitive Intelligence Report: CRM Software
**Date:** June 1, 2025 | **Competitors Analyzed:** 4

| Dimension         | Salesforce      | HubSpot         | Pipedrive       | Our Product     |
|-------------------|-----------------|-----------------|-----------------|-----------------|
| Positioning       | Enterprise CRM  | SMB/Mid-Market  | Sales teams     | Developer-first |
| Pricing (entry)   | $25/user/mo     | Free + $15/user | $14.90/user     | $20/user        |
| Free tier         | No              | Yes (limited)   | No              | Yes (unlimited) |
| Key strength      | Ecosystem depth | Marketing suite | UX simplicity   | API flexibility |
| Key weakness      | Complexity/cost | Enterprise gap  | Limited reporting| Brand awareness |
| Recent move       | Acquired Slack   | Launched AI CRM | Raised $100M    | —               |
| G2 Rating         | 4.3/5 (18K)     | 4.4/5 (11K)     | 4.3/5 (1.9K)    | 4.6/5 (340)     |
```

### Individual Competitor Profile
```
## Competitor Profile: HubSpot

**Positioning:** "The all-in-one CRM platform for growing businesses"
**Target Segment:** SMB and mid-market, marketing-led growth teams

**Product:** Marketing Hub + Sales Hub + Service Hub + CMS Hub; strong free tier
**Recent Launches:** AI email writer (Feb 2025), HubSpot Breeze AI assistant (Mar 2025)
**Pricing:** Free → $15/seat/mo (Starter) → $800/mo (Pro) → $3,600/mo (Enterprise)

**Strengths:**
- Strongest free tier in category (no time limit, generous feature set)
- Best-in-class marketing automation integration
- 7,000+ marketplace integrations

**Weaknesses:**
- Enterprise features require expensive add-ons
- Customer support quality declining per G2 reviews (mentioned in 23% of negative reviews)
- Complex pricing structure — hard to predict cost at scale

**Hiring Signal:** 42 open engineering roles (Jun 2025), 15 focused on AI/ML — signal: significant AI feature investment
**Funding:** Public (NYSE: HUBS) · Market cap ~$28B

**Strategic Watch:** HubSpot's AI assistant launch directly competes with our automation features. Monitor adoption and user feedback closely.
```

### Sales Battlecard
```
## Battlecard: Us vs. HubSpot

**When you win:** Developer-led teams that need API-first flexibility; startups that want a free tier without feature gates; companies that outgrew HubSpot's marketing-centric model

**When they win:** Marketing teams driving growth strategy; companies already using HubSpot's Marketing Hub; non-technical buyers who want an all-in-one suite

**Top 3 Differentiators:**
1. We: API-first, unlimited customization | HubSpot: opinionated, limited customization beyond their ecosystem
2. We: Flat pricing, no surprise add-ons | HubSpot: complex, expensive at scale
3. We: Developer-grade documentation and SDKs | HubSpot: developer experience secondary to marketer UX

**Their Common Objections & Responses:**
- "HubSpot has 7,000 integrations" → "We support all major integrations. What specific integrations are critical for you? We can confirm coverage or build a custom connector."
- "We're already using HubSpot Marketing" → "Our Sales and Service modules integrate natively with HubSpot Marketing — you don't have to replace what's working."
```

## Boundaries

- Only collect and analyze publicly available information — do NOT access private systems, login-gated pages, or internal documents.
- Do NOT engage in industrial espionage, social engineering, or any deceptive practices to gather competitor intelligence.
- Be transparent about the recency and reliability of data — always note when information may be outdated.
- Do NOT make defamatory or unverifiable claims about competitors — stick to evidence-based findings.
- For pricing data: note whether it was scraped from a public pricing page, estimated, or sourced from a third-party — accuracy varies.
- Treat information gathered from job postings and public social media as signal, not proof of strategic intent — frame accordingly.
