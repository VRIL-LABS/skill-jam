---
name: social-media-monitor
description: Tracks brand mentions, hashtags, and engagement metrics across social platforms and surfaces sentiment trends. Invoke when asked to monitor social media, track brand mentions, analyze hashtags, measure engagement, or detect sentiment trends on social platforms.
---

# Social Media Monitor

Tracks and analyzes brand mentions, hashtags, keywords, and competitor activity across social media platforms — surfacing engagement metrics, sentiment trends, emerging conversations, and actionable insights for brand management and marketing strategy.

## When to Use

- User wants to track how their brand, product, or campaign is being discussed online
- A hashtag or keyword campaign needs performance monitoring
- Competitive intelligence is needed on a competitor's social presence
- A PR crisis or negative sentiment spike needs to be detected early
- User asks to measure the impact of a launch, announcement, or campaign on social
- Influencer or community conversations around a topic need to be tracked
- Monthly or weekly social performance reports are needed

## Process

1. **Define monitoring parameters**:
   - **Entities to track**: brand names, product names, competitor names, campaign hashtags, executive names, industry keywords
   - **Platforms**: specify which platforms to cover (Twitter/X, LinkedIn, Reddit, Instagram, TikTok, Facebook, YouTube comments, forums)
   - **Time window**: real-time, last 24 hours, last 7 days, last 30 days, or custom range
   - **Languages and geographies**: global or targeted by region/language
   - **Exclusions**: suppress noise (unrelated uses of a common word, competitor's brand terms that appear in complaints against you)

2. **Collect mentions and data**:
   - Query platform APIs or search interfaces for each tracked entity
   - Capture: post URL, platform, author/handle, follower count, post text, media type, timestamp, engagement metrics (likes, shares, comments, views)
   - Deduplicate cross-posted content (same text across multiple platforms)
   - Filter: remove spam, bot-generated content, and irrelevant matches using signal patterns

3. **Analyze volume and trends**:
   - Total mention count by platform, day, and keyword
   - Volume trend: is mention rate increasing, decreasing, or stable vs. prior period?
   - Spike detection: flag hours/days where mention volume exceeds 2× the rolling 7-day average
   - Reach: estimated total impressions (mentions × average follower count of authors)

4. **Sentiment analysis**:
   - Apply document-level sentiment to each mention (Positive / Negative / Neutral / Mixed)
   - Compute sentiment ratio: % positive vs. % negative
   - Track sentiment trend over time — is brand perception improving or declining?
   - Surface the most positive and most negative posts for manual review

5. **Identify emerging themes**:
   - Cluster mentions by topic/theme using keyword co-occurrence and semantic grouping
   - Surface top themes discussed alongside the tracked entity (e.g., "pricing", "customer support", "new feature")
   - Identify newly emerging themes that weren't present in the prior reporting period

6. **Competitive benchmarking** (when requested):
   - Compare share of voice: your brand's mention volume vs. competitors
   - Compare sentiment: positive sentiment ratio vs. competitor baseline
   - Surface gaps: topics where competitors are praised that you are not mentioned

7. **Influencer and author analysis**:
   - Identify top authors by reach (follower count × engagement rate)
   - Flag verified accounts, journalists, or high-follower influencers posting about the brand
   - Detect repeated critics or brand advocates

8. **Alert generation**:
   - Flag posts requiring urgent response: negative high-reach posts, potential crises, viral negative threads
   - Prioritize by: reach (high follower authors first), sentiment (strongly negative), engagement velocity (rapidly accumulating likes/shares)

## Output Format

```
## Social Media Monitoring Report
**Brand:** Acme Corp | **Period:** June 1–7, 2025 | **Platforms:** Twitter/X, LinkedIn, Reddit

### Volume Summary
Total Mentions: 4,821 (+18% vs prior week)
Estimated Reach: 12.3M impressions

| Platform   | Mentions | Change | Sentiment (Pos/Neg/Neu) |
|------------|----------|--------|--------------------------|
| Twitter/X  | 3,102    | +22%   | 61% / 23% / 16%          |
| LinkedIn   | 891      | +8%    | 74% / 10% / 16%          |
| Reddit     | 828      | +14%   | 48% / 38% / 14%          |

### Sentiment Trend
Positive ratio: 63% (up from 57% last week) ✅
Negative ratio: 22% (down from 28% last week) ✅

### Top Themes Mentioned
1. New product launch "ProMax" — 1,841 mentions (38%) · Sentiment: Positive
2. Pricing concerns — 612 mentions (13%) · Sentiment: Negative
3. Customer support — 498 mentions (10%) · Sentiment: Mixed

### Spike Alert 🚨
June 4, 2:00–4:00 PM: 340 mentions in 2 hours (5× normal rate)
Trigger: Viral Twitter/X thread by @techreviewer (280K followers) comparing Acme to competitors.
Sentiment of spike: 55% Positive (product praise)

### Urgent Posts Requiring Response
1. @frustrated_user (12K followers): "Acme's support has been unresponsive for 2 weeks. Escalating publicly." [Negative, 847 engagements]
2. Reddit r/tech: Thread "Is Acme worth it in 2025?" — top upvoted comment is negative [412 upvotes]

### Top Positive Posts
- @happycustomer: "Just switched to Acme ProMax and honestly blown away. 10/10." [3.2K likes]

### Competitor Benchmark
Share of Voice: Acme 34% · Competitor A 41% · Competitor B 25%
Acme sentiment vs. Competitor A: 63% positive vs. 58% positive ✅
```

## Examples

### Example Input
```
Monitor Twitter/X and Reddit for mentions of "Acme Corp" over the past 7 days. Tell me sentiment breakdown and flag any posts that need urgent response.
```

### Example Output
```
Monitoring complete. 4,821 mentions found across Twitter/X and Reddit (June 1–7).

Sentiment: 63% Positive · 22% Negative · 15% Neutral
Trend: Improving — negative ratio dropped from 28% to 22% vs. last week.

🚨 2 posts flagged for urgent response:
1. @frustrated_user (12K followers) — public support complaint, 847 engagements
2. Reddit thread — top negative comment gaining traction (412 upvotes)

Top trending theme: "ProMax" launch driving the volume spike on June 4.
```

## Boundaries

- Do NOT access private or direct messages — only analyze publicly available content.
- Respect platform API rate limits and terms of service; do NOT scrape at rates that violate platform policies.
- Do NOT publish, share, or quote individual users' posts without consent in any public-facing output.
- Sentiment classifications are probabilistic estimates — flag low-confidence results rather than presenting them as definitive.
- Do NOT use monitored data to target or harass specific individuals; surface posts for brand response only.
- Flag when monitored keywords are common words that may produce false positives (e.g., brand name = common English word).
