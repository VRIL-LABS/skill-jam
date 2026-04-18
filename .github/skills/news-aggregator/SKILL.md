---
name: news-aggregator
description: Fetches, deduplicates, and categorizes news articles from multiple sources on a given topic or keyword list. Invoke when asked to find news, aggregate news articles, get headlines, monitor a topic in the news, or compile a news briefing on any subject.
---

# News Aggregator

Collects, deduplicates, categorizes, and summarizes news articles from multiple sources on any topic or keyword — delivering curated briefings, headline digests, topic-tagged story clusters, and trend signals across any domain or time window.

## When to Use

- User asks for news on a specific topic, company, person, or keyword
- A daily or weekly news briefing needs to be compiled
- User wants to know "what's happening" in an industry or domain
- A topic needs to be monitored for breaking news and emerging stories
- Multiple news sources need to be aggregated into a single curated feed
- User wants to understand the narrative around a story by seeing multiple source perspectives
- Background research on a current event requires recent news coverage

## Process

1. **Define the query and parameters**:
   - **Topic/keywords**: extract main subject, entity names, and related terms from the user's request
   - **Time range**: breaking news (last 24 hours), recent (last 7 days), or custom window
   - **Source types**: news wire, mainstream press, trade/industry press, local news, blogs — note which the user wants
   - **Geography**: global coverage, country-specific, or local
   - **Language**: default to English; specify if other languages are needed
   - **Exclusions**: types of sources or topics to suppress (e.g., "no opinion pieces", "US coverage only")

2. **Fetch articles from multiple sources**:
   - Query news APIs (NewsAPI, GDELT, Google News RSS, Bing News, or individual publication RSS feeds)
   - Retrieve: headline, publication name, author, publication timestamp, URL, article description/lead paragraph, category tags
   - Aim for ≥3 distinct sources per story to enable perspective comparison

3. **Deduplicate and cluster**:
   - Identify articles covering the same underlying story (same event, announcement, or development)
   - Cluster by: headline similarity (>70% token overlap), shared named entities, and publication time proximity (within 24 hours of original report)
   - Within each cluster: designate the original/breaking story and treat others as follow-ups or reactions
   - Remove true duplicates (same article syndicated across multiple sites)

4. **Categorize and tag**:
   - Assign primary category: Business, Technology, Politics, Health, Science, Finance, Sports, Entertainment, World, etc.
   - Tag secondary topics: specific companies, people, geographies, or themes mentioned
   - Assign importance tier: Breaking / Major Development / Background / Analysis / Opinion
   - Flag: satire or opinion pieces that could be mistaken for factual news reporting

5. **Assess source diversity**:
   - Note if coverage is dominated by one source or outlet family (e.g., all Murdoch-owned)
   - Flag if a story is covered by only one source (unverified / developing)
   - Identify left-leaning, right-leaning, and centrist sources when covering political topics, for balanced briefings

6. **Summarize each story cluster**:
   - Write a 1–3 sentence synthesis of what happened, drawing from multiple sources
   - Include the most significant facts and quotes
   - Note any discrepancies between sources' accounts

7. **Format the briefing**:
   - Headline digest: ranked list of top stories with single-line summaries
   - Full briefing: grouped by topic/category with story summaries and source links
   - Data/trend note: if multiple stories signal a broader trend, surface the meta-narrative

## Output Format

### Headline Digest
```
📰 Top Headlines — AI Industry | June 1, 2025

1. OpenAI announces GPT-5 release date set for September [Reuters, FT, WSJ]
2. EU AI Act enforcement begins; tech firms face first compliance audits [BBC, Politico]
3. Google DeepMind publishes breakthrough in protein structure prediction [Nature, NYT]
4. Anthropic raises $2B Series E at $50B valuation [Bloomberg, TechCrunch]
5. AI chip shortage eases as TSMC expands 3nm capacity [Reuters, The Verge]
```

### Full Briefing
```
## News Briefing: Electric Vehicles | June 1–7, 2025

### 🔴 Breaking
**Tesla Q2 Deliveries Miss Estimates by 8%**
Tesla reported 420,000 vehicle deliveries in Q2 2025, falling short of the 455,000 analyst consensus. CEO Elon Musk attributed the miss to production delays at the Berlin Gigafactory. Tesla stock fell 7% in after-hours trading.
Sources: Reuters · Bloomberg · CNBC | June 1, 2025

### 📌 Major Developments
**EU Mandates Vehicle-to-Grid Standards by 2027**
The European Commission finalized regulations requiring all new EVs sold in the EU from 2027 to support bidirectional charging (V2G). Automakers praised the clarity; grid operators called for faster rollout.
Sources: Electrek · Financial Times | June 3, 2025

### 📊 Trend Signal
Four separate stories this week cite charging infrastructure as the #1 barrier to EV adoption in the US — a growing narrative pointing to policy pressure on the Biden administration's infrastructure bill implementation.
```

## Examples

### Example Input
```
Give me a 5-story briefing on what's happening in the biotech industry this week.
```

### Example Output
```
## Biotech Briefing — Week of June 1, 2025

1. **FDA Approves Eli Lilly's Alzheimer Drug**
The FDA granted full approval to donanemab, Lilly's amyloid-targeting Alzheimer's therapy, citing 35% slowing of cognitive decline in Phase 3 trials. Shares rose 12%.
[NYT · Reuters · STAT News]

2. **Moderna Begins mRNA Cancer Vaccine Phase 3 Trials**
Moderna and Merck launched a 1,000-patient Phase 3 trial of mRNA-4157 in combination with Keytruda for melanoma. Full data expected 2027.
[Bloomberg · BioPharma Dive]

3. **CRISPR Gene Editing Approved for Sickle Cell Disease in EU**
The European Medicines Agency approved Casgevy (exa-cel) for sickle cell disease and beta thalassemia, becoming the first approved CRISPR therapy in the EU.
[BBC · Fierce Biotech]

4. **Biotech IPO Market Rebounds in Q2**
18 biotech IPOs raised $4.2B in Q2 2025, a 60% increase over Q2 2024, driven by AI-drug-discovery platforms.
[Wall Street Journal · Endpoints News]

5. **WHO Warns of Growing Antimicrobial Resistance Crisis**
A new WHO report estimates AMR could kill 10M people annually by 2050 without urgent antibiotic pipeline investment. Three pharma companies announced new R&D commitments.
[The Lancet · Guardian · Reuters]
```

## Boundaries

- Do NOT fabricate news stories, quotes, or publication names — only surface content from actual retrieved sources.
- Always include source attribution (publication name) and publication date for every story.
- Flag when a story comes from only a single source (unverified or developing) vs. multiple independent sources.
- Clearly distinguish factual news reporting from opinion, editorial, and analysis pieces.
- Do NOT present satire as news — flag satirical outlets explicitly if they appear in results.
- For politically sensitive topics, surface coverage from multiple ideological perspectives when possible.
- News data ages quickly — always display the retrieval timestamp and recommend refreshing for breaking situations.
