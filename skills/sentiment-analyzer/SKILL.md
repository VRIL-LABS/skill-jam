---
name: sentiment-analyzer
description: Classifies the sentiment (positive, negative, neutral, mixed) of text at document, sentence, or aspect level. Invoke when asked to analyze sentiment, detect tone, measure opinion, classify feedback, gauge customer satisfaction, or evaluate emotional tone in text.
---

# Sentiment Analyzer

Classifies the emotional tone and opinion expressed in text at multiple granularities — document-level, sentence-level, and aspect-level — with confidence scores and supporting evidence. Handles reviews, support tickets, social media posts, survey responses, and any opinion-bearing text.

## When to Use

- User provides customer reviews, survey responses, or feedback and wants sentiment scores
- Support ticket queue needs to be triaged by urgency or customer frustration level
- Social media posts or brand mentions need to be monitored for sentiment trends
- User asks to "analyze tone", "detect emotion", or "measure satisfaction" in text
- A/B test copy needs to be evaluated for emotional impact
- Product or service feedback needs to be categorized for product teams
- NPS comments or CSAT responses need structured analysis

## Process

1. **Determine the analysis scope**:
   - **Document-level**: single overall sentiment for the entire text
   - **Sentence-level**: per-sentence sentiment breakdown
   - **Aspect-level**: sentiment for specific entities or attributes mentioned (e.g., "price: negative", "delivery: positive")
   - **Emotion detection**: beyond polarity — joy, anger, fear, surprise, sadness, disgust
   - Default to document + aspect level for product reviews; document level for short texts

2. **Preprocess the text**:
   - Detect and handle: sarcasm signals (detect but flag with low confidence), negation ("not great" → negative), intensifiers ("absolutely terrible" → strongly negative), and qualified statements ("usually good, but this time...").
   - Identify the language and adjust analysis accordingly
   - Note: emojis, slang, and abbreviations are valid sentiment signals — interpret them contextually

3. **Classify overall sentiment**:
   - Return one of: **Positive**, **Negative**, **Neutral**, **Mixed**
   - Assign a confidence score (0–1) and a normalized sentiment score (-1.0 to +1.0)
   - **Mixed** = significant positive AND negative sentiment present in the same text

4. **Perform aspect-level analysis** (when applicable):
   - Identify mentioned aspects/entities: price, quality, service, delivery, usability, staff, features, etc.
   - For each aspect: extract the relevant snippet, classify sentiment, and assign a score
   - Map to a structured output so results can be aggregated across many texts

5. **Extract key phrases**:
   - Quote the specific phrases that most strongly drove the sentiment classification
   - Distinguish positive driver phrases from negative driver phrases

6. **Handle edge cases**:
   - **Sarcasm**: flag as potentially sarcastic if linguistic signals are present; lower confidence
   - **Neutral text** (factual statements, questions): classify as Neutral with explanation
   - **Multilingual text**: detect and process each language segment separately
   - **Ambiguous text**: present both possible interpretations with probability estimates

7. **Batch processing** (for multiple inputs):
   - Return an array of results, one per input
   - Include aggregate statistics: sentiment distribution, average score, most common aspects mentioned

## Output Format

### Single Document Analysis
```json
{
  "text": "The product quality is outstanding, but shipping took two weeks longer than promised and customer service was unhelpful.",
  "overall_sentiment": "Mixed",
  "sentiment_score": -0.12,
  "confidence": 0.88,
  "aspects": [
    { "aspect": "product quality", "sentiment": "Positive", "score": 0.92, "snippet": "product quality is outstanding" },
    { "aspect": "shipping", "sentiment": "Negative", "score": -0.75, "snippet": "took two weeks longer than promised" },
    { "aspect": "customer service", "sentiment": "Negative", "score": -0.68, "snippet": "customer service was unhelpful" }
  ],
  "key_phrases": {
    "positive": ["outstanding"],
    "negative": ["two weeks longer than promised", "unhelpful"]
  }
}
```

### Batch Summary (10+ documents)
```
Sentiment Distribution: 62% Positive · 28% Negative · 7% Mixed · 3% Neutral
Average Score: +0.41

Top Positive Aspects: product quality (87%), ease of use (74%), value for money (65%)
Top Negative Aspects: shipping speed (43%), return process (38%), customer support (31%)

Flagged for Review (frustrated customers):
- Review #42: Score -0.91 ("This is the worst experience I've ever had...")
- Review #87: Score -0.85 ("Complete waste of money. Never again.")
```

## Examples

### Example Input
```
Analyze the sentiment of these three customer reviews and tell me which aspects each mentions:

1. "Absolutely love the new interface — so clean and fast!"
2. "Decent product but overpriced. The support team was slow to respond."
3. "Works fine I guess. Nothing special."
```

### Example Output
```
Review 1:
  Overall: Positive (score: +0.93)
  Aspects: interface → Positive ("clean and fast")

Review 2:
  Overall: Mixed (score: -0.22)
  Aspects: product quality → Neutral ("decent"), price → Negative ("overpriced"), customer support → Negative ("slow to respond")

Review 3:
  Overall: Neutral (score: +0.05)
  Aspects: none clearly identified
  Note: Understated tone — low expressiveness, not necessarily indifferent.
```

## Boundaries

- Do NOT conflate factual statements with sentiment — "The battery lasts 4 hours" is Neutral unless paired with a judgment.
- Flag sarcasm explicitly and reduce confidence rather than silently inverting the apparent polarity.
- Do NOT apply sentiment models trained on English to other languages without language detection — always detect language first.
- For mental health or crisis-related text, flag urgency and suggest the user route to appropriate human support rather than reducing it to a sentiment score.
- Confidence scores are estimates, not ground truth — communicate this when presenting scores to stakeholders.
- Do NOT use sentiment analysis results to make high-stakes decisions (hiring, loan approvals) without human review.
