---
name: lead-qualifier
description: Scores, enriches, and prioritizes inbound sales leads using firmographic data, behavioral signals, and ICP criteria. Invoke when asked to qualify leads, score prospects, prioritize a sales pipeline, enrich contact data, or evaluate if a lead matches the ideal customer profile.
---

# Lead Qualifier

Scores, enriches, and prioritizes inbound sales leads by evaluating firmographic fit, behavioral engagement signals, and alignment with the Ideal Customer Profile (ICP) — delivering a ranked, actionable lead queue with qualification rationale to help sales teams focus on the highest-probability opportunities.

## When to Use

- User provides a list of leads or a CRM export and wants them scored and prioritized
- An inbound lead needs to be quickly evaluated for sales follow-up urgency
- User asks to "qualify", "score", or "enrich" a prospect or lead list
- A sales pipeline needs to be triaged to focus effort on the best opportunities
- An ICP needs to be defined and then applied to a set of prospects
- Lead routing logic needs to be designed (which rep gets which type of lead)
- User wants to identify the characteristics of their best-fit customers

## Process

1. **Define or confirm the Ideal Customer Profile (ICP)**:
   If no ICP is provided, ask for or infer from context:
   - **Firmographic criteria**: company size (employees, revenue range), industry/vertical, geography, business model (B2B/B2C), growth stage (startup/SMB/mid-market/enterprise)
   - **Technographic criteria**: tech stack signals (e.g., "uses Salesforce", "runs on AWS", "built with React")
   - **Behavioral criteria**: visited pricing page, started trial, engaged with specific content, attended webinar
   - **Intent signals**: recent funding round, job posting for roles that use your product, leadership change
   - **Disqualifiers**: industries you don't serve, company sizes below minimum deal size, geographies outside your market

2. **Enrich the lead data**:
   For each lead, gather missing data from available signals:
   - Company: industry, size, revenue, funding history, headquarters, tech stack
   - Contact: title, seniority level, department, LinkedIn profile
   - Behavioral: pages visited, content downloaded, email opens/clicks, trial activity, time-on-site
   - Intent: third-party intent data signals (G2 reviews browsed, competitor comparisons, job postings)

3. **Score each lead**:
   Apply a weighted scoring model across dimensions:

   **Firmographic fit (up to 40 points)**:
   - Industry match: +15 if in target vertical, +5 if adjacent
   - Company size: +15 at ideal size range, scaled down for smaller/larger
   - Geography: +10 if in target market
   - Revenue/stage: +10 if aligned with your ACV range

   **Behavioral engagement (up to 30 points)**:
   - Visited pricing page: +10
   - Started free trial or demo request: +15
   - Returned to site 3+ times: +8
   - Engaged with email / attended webinar: +5 each

   **Intent signals (up to 20 points)**:
   - Active buying intent (recent RFP, comparison browsing): +15
   - Recent relevant job posting: +10
   - New funding round (can afford your product): +8
   - Leadership change: +5

   **Contact quality (up to 10 points)**:
   - Decision-maker or budget holder: +10
   - Influencer/evaluator: +5
   - Unknown seniority: +0

   **Total score → tier**:
   - 80–100: 🔥 Hot — immediate outreach (same business day)
   - 60–79: 🟡 Warm — nurture + outreach within 48 hours
   - 40–59: 🟢 Qualified — add to nurture sequence
   - <40: ❌ Not yet qualified — add to long-term nurture or disqualify

4. **Apply disqualifier checks**:
   - If a hard disqualifier is met (blocked industry, too small, wrong geography): mark as Disqualified regardless of score and note the reason
   - Soft disqualifiers (e.g., no budget signals): lower score but don't auto-disqualify

5. **Generate qualification summary per lead**:
   - Score and tier
   - Top 3 reasons for the score (positive signals)
   - Top 1–2 disqualifying or derisking factors
   - Recommended next action: call, email, personalized outreach, nurture sequence, or disqualify
   - Suggested talk track or messaging angle based on the strongest qualifying signals

6. **Route lead to the appropriate owner**:
   - Apply routing rules: enterprise leads → enterprise AE, SMB leads → SDR, specific verticals → vertical specialist
   - Output: lead card with all enriched data, score, and recommended action attached

## Output Format

```
## Lead Qualification Report
**Date:** June 1, 2025 | **ICP:** B2B SaaS companies, 50–500 employees, US/Canada, using Salesforce

---

### Lead #1: Jordan Martinez — VP Sales, Acme Corp
**Score: 84/100 🔥 HOT**
**Recommended Action:** Immediate outreach — personalized email + call within 24 hours

| Dimension          | Score | Signal                                                  |
|--------------------|-------|---------------------------------------------------------|
| Firmographic fit   | 35/40 | B2B SaaS ✅ · 180 employees ✅ · San Francisco ✅        |
| Behavioral         | 28/30 | Visited pricing page ✅ · Started trial (Day 3) ✅      |
| Intent             | 12/20 | 3 open SDR roles posted this month (scaling signal)     |
| Contact quality    | 9/10  | VP Sales — budget holder / decision-maker ✅            |

**Key Qualifiers:** Trial activity, decision-maker title, scaling sales team
**Risk Factors:** Trial engagement dropped after Day 3 — possible blocker
**Talk Track:** "We saw you were exploring [feature] in your trial — many VP Sales at [similar company] use that to [outcome]. Can I show you how?"

**Route to:** Enterprise AE — Sarah K.

---

### Lead #2: Anonymous Form Fill — marketing@genericco.com
**Score: 28/100 ❌ NOT YET QUALIFIED**
**Recommended Action:** Add to nurture email sequence (monthly touchpoints)

| Dimension          | Score | Signal                            |
|--------------------|-------|-----------------------------------|
| Firmographic fit   | 10/40 | Industry unknown · Company unknown |
| Behavioral         | 8/30  | Downloaded 1 ebook                |
| Intent             | 5/20  | No intent signals                 |
| Contact quality    | 5/10  | Generic email — unknown seniority  |

**Risk Factors:** No company data available for enrichment. Generic email address.
**Action:** Trigger enrichment workflow; if company is identified, re-score.
```

## Examples

### Example Input
```
Here are 5 inbound leads from this week. Our ICP is B2B SaaS companies, 100–1000 employees, in the US. Score and prioritize them.
[lead data]
```

### Example Output
```
Lead Prioritization — Week of June 1

1. 🔥 Jordan Martinez (VP Sales, Acme Corp) — Score: 84 · Immediate outreach
2. 🟡 Priya Sharma (Head of Ops, Beta Inc) — Score: 67 · 48-hour follow-up
3. 🟢 Chris Wong (Marketing Manager, Gamma LLC) — Score: 52 · Nurture sequence
4. 🟢 Taylor Reed (Developer, Delta Co) — Score: 44 · Technical nurture track
5. ❌ Anonymous — Score: 28 · Enrich before contacting

Top priority: Jordan — trial activity + decision-maker title = highest close probability this week.
```

## Boundaries

- Lead scoring models are probabilistic guides, not predictions — always frame scores as directional signals that require sales judgment.
- Do NOT use protected characteristics (gender, race, age, nationality, religion) as scoring signals — ever.
- Be transparent about the scoring model: share weights and criteria so sales teams can understand and calibrate.
- If enrichment data is missing, reduce confidence in the score and flag it rather than inflating the score with assumed data.
- Do NOT auto-send outreach on behalf of the user — surface recommendations and let the sales team execute.
- Treat all lead contact data as PII — do not log or expose it beyond the immediate task.
