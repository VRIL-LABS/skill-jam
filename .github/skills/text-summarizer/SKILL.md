---
name: text-summarizer
description: Condenses long-form documents, papers, or transcripts into concise summaries, bullet points, or executive briefs. Invoke when asked to summarize, condense, TL;DR, extract key points, create an abstract, or generate an executive summary from a document or transcript.
---

# Text Summarizer

Transforms long-form content — research papers, legal documents, meeting transcripts, articles, reports, and books — into concise, accurate, and purpose-matched summaries at any desired length and format, preserving the most important information while discarding redundancy.

## When to Use

- User provides a long document and asks for a summary, TL;DR, or key points
- A research paper or technical report needs an abstract or executive summary
- A meeting transcript needs action items and decisions extracted
- A legal contract needs a plain-English summary of key terms
- User asks to "shorten", "condense", or "distill" any piece of content
- Multiple documents need to be summarized and compared side by side
- A newsletter or report needs an intro paragraph based on the full content

## Process

1. **Determine the summary requirements**:
   - **Length**: one sentence (headline), one paragraph (~100 words), bullet list, or full brief (1–2 pages)
   - **Format**: prose, bullet points, structured report sections, or Q&A
   - **Audience**: technical expert, executive, general public, or specific role
   - **Focus**: overall summary, or focus on a specific aspect (findings, risks, action items, decisions)
   - Default: bullet-point key takeaways + one-paragraph overview if not specified

2. **Read and structure the source content**:
   - Identify the document type: article, research paper, legal document, transcript, report, book chapter
   - Map the document's own structure: sections, headings, abstract, conclusion
   - For research papers: intro, methodology, results, discussion/conclusions are the key sections
   - For legal documents: parties, obligations, key dates, limitations, and penalty clauses are priority
   - For transcripts: speakers, topic shifts, decisions, and action items

3. **Extract key information by importance**:
   - **Main thesis or purpose**: What is this document about? What problem does it address?
   - **Key findings or claims**: What are the most important conclusions or assertions?
   - **Supporting evidence**: What are the strongest pieces of data or argument?
   - **Action items and decisions**: What needs to be done, by whom, by when?
   - **Caveats and limitations**: What did the authors/speakers acknowledge as limitations?

4. **Draft the summary**:
   - Lead with the most important point (inverted pyramid — don't bury the lede)
   - Use the audience's vocabulary — simplify jargon for general audiences, preserve technical precision for experts
   - Do NOT introduce information not in the source — only compress, do not synthesize or editorialize
   - Maintain the source's position and tone — do not add judgment or spin
   - Flag where the source is ambiguous, contradictory, or where data was missing

5. **Format output to requested style**:
   - **TL;DR / headline**: 1–2 sentences, the single most critical point
   - **Bullet list**: 5–10 bullets, each beginning with a strong verb or key term
   - **Executive summary**: structured with Overview, Key Findings, Implications, Recommended Actions
   - **Meeting notes**: Attendees, Decisions Made, Action Items (owner + deadline), Open Questions
   - **Abstract**: 150–250 words, covers purpose, methods, results, and conclusion

6. **Quality check**:
   - Verify no key claims from the source are omitted or distorted
   - Check that numbers, dates, names, and cited facts are reproduced accurately
   - Flag any section where the source text was unclear, truncated, or contradicted itself

## Output Format

### TL;DR
```
TL;DR: The study found that remote workers report 18% higher productivity but 24% lower sense of team belonging compared to in-office peers, suggesting a hybrid model addresses both concerns.
```

### Bullet-Point Summary
```
**Key Points: "The Future of Remote Work" (2025 Report)**

- Remote workers show 18% higher individual productivity on average vs. in-office workers
- Team collaboration scores drop 24% in fully remote environments
- Hybrid models (2–3 days/week in office) score highest on both productivity and belonging metrics
- 67% of surveyed managers report difficulty tracking remote employee performance
- Report recommends: invest in async-first tooling and quarterly in-person offsites
- Sample: 4,200 knowledge workers across 18 industries, surveyed Jan–Mar 2025
```

### Executive Summary
```
## Executive Summary

**Overview:** This report analyzes productivity and engagement outcomes for remote, hybrid, and in-office knowledge workers across 18 industries (n=4,200, Jan–Mar 2025).

**Key Findings:**
- Individual productivity is highest in fully remote settings (+18% vs. in-office baseline)
- Team cohesion and collaboration are weakest in fully remote settings (-24%)
- Hybrid arrangements (2–3 office days/week) optimize across both dimensions

**Implications:** Organizations pursuing full remote adoption risk long-term damage to culture and collaboration quality. Hybrid models represent the evidence-backed balance point.

**Recommended Actions:**
1. Shift policy default to hybrid (2–3 days/week) by Q3
2. Invest in async communication tooling to support remote days
3. Budget for quarterly in-person team gatherings

**Limitations:** Self-reported data; productivity definitions vary by role and industry.
```

### Meeting Notes
```
**Meeting:** Product Roadmap Review — June 1, 2025
**Attendees:** Alice (PM), Bob (Eng Lead), Carol (Design), Dave (Marketing)

**Decisions Made:**
- v2.3 launch date confirmed: July 15, 2025
- Dark mode feature deprioritized to v2.4

**Action Items:**
| Owner | Task | Due |
|-------|------|-----|
| Bob   | Finalize API migration plan | June 8 |
| Carol | Deliver updated design specs | June 10 |
| Dave  | Prepare launch comms brief | June 12 |

**Open Questions:**
- Pricing for v2.3 premium tier not yet decided (Alice to schedule separate session)
```

## Examples

### Example Input
```
Summarize the following 3,000-word research paper abstract and conclusions section into a 5-bullet executive summary for a non-technical business audience.
[paper content]
```

### Example Output
```
**Executive Summary — [Paper Title]**
1. The research confirms that machine learning models can reduce customer churn prediction errors by 35% compared to traditional rule-based systems.
2. The improvement requires at least 12 months of historical transaction data to be effective.
3. Implementation cost averages $180K for mid-size companies, with ROI breakeven at 8 months based on reduced churn.
4. Key limitation: the model underperforms for new customers with <3 months of history.
5. Recommended next step: pilot deployment with a single customer segment before full rollout.
```

## Boundaries

- Do NOT add facts, opinions, or interpretations not present in the source — summaries must be strictly extractive or compressive.
- Do NOT alter the meaning of findings, especially in scientific, legal, or financial documents — accuracy is critical.
- Always note when the source is truncated or when important sections were not available for summarization.
- For very long documents, acknowledge if portions were weighted more heavily (e.g., conclusions over the full methodology).
- Flag contradictions within the source document rather than silently choosing one side.
- Do NOT present a summary as a substitute for reading the original in legal or regulatory contexts — recommend review of the full document.
