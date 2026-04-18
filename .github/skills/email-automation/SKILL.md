---
name: email-automation
description: Composes, sends, classifies, and summarizes emails based on rules, templates, or natural-language instructions. Invoke when asked to draft an email, automate email replies, set up email rules, classify an inbox, parse email content, or build email-based workflows.
---

# Email Automation

Handles the full lifecycle of email tasks — composing context-aware messages, classifying and routing incoming mail, summarizing threads, extracting structured data from messages, and building rule-based or AI-driven email workflows.

## When to Use

- User asks to "draft", "write", or "send" an email
- User wants to automate replies to incoming messages based on content or rules
- An inbox needs to be classified, prioritized, or cleaned up
- User wants to extract data (e.g., order confirmations, meeting invites) from email bodies
- A drip campaign or follow-up sequence needs to be created
- User asks to summarize a long email thread
- User wants to set up auto-responders or filters

## Process

1. **Identify the task type**:
   - **Compose**: Draft a new email from intent, context, or a template
   - **Reply**: Generate a reply to a provided message, matching tone and addressing all points
   - **Classify**: Categorize messages by type (support, sales, newsletter, spam, etc.)
   - **Summarize**: Condense a thread or message into key points and action items
   - **Extract**: Pull structured fields (sender, date, amount, tracking number) from an email body
   - **Workflow**: Build a rule-based pipeline (receive → classify → route → respond)

2. **For composition and replies**:
   - Infer the recipient, subject, and appropriate tone (formal, casual, technical) from context
   - Include all required components: greeting, body paragraphs addressing each point, call to action, and sign-off
   - Match the user's voice if example emails are provided
   - Flag ambiguous instructions ("mention the project") and ask for clarification before drafting

3. **For classification**:
   - Define or infer the category taxonomy (e.g., Urgent / Action Required / FYI / Newsletter / Spam)
   - Score each message against the categories using subject, sender domain, body keywords, and structural signals (unsubscribe links → newsletter)
   - Return category, confidence score, and a one-sentence rationale per message

4. **For summarization**:
   - Identify all participants and their roles in the thread
   - Extract: topic, key decisions made, open questions, and action items with owners
   - Order information by importance, not chronologically

5. **For data extraction**:
   - Define the target schema before parsing (e.g., `{order_id, vendor, amount, due_date}`)
   - Use regex for structured fields (dates, amounts, tracking codes) and NLP for free-form content
   - Flag fields that could not be extracted reliably (confidence < 80%)

6. **For workflow design**:
   - Map out: trigger condition → classification step → action (reply / forward / label / archive)
   - Produce pseudocode or implementation in the user's email platform (Gmail API, Outlook Graph API, SMTP/IMAP)

7. **Validate output before delivering**:
   - Check that composed emails contain no placeholder text (e.g., `[INSERT NAME]`)
   - Confirm extracted data passes basic sanity checks (dates are valid, amounts are numeric)

## Output Format

### Composed Email
```
To: sarah.jones@example.com
Subject: Follow-up: Q3 Partnership Proposal

Hi Sarah,

Thank you for taking the time to speak with us last Tuesday. Following our conversation,
I wanted to share the updated proposal (attached) which incorporates the feedback you
provided on pricing and the implementation timeline.

Could we schedule a 30-minute call this week to walk through the changes? I'm available
Thursday between 2–5 PM EST or Friday morning.

Looking forward to hearing from you.

Best regards,
[Your Name]
```

### Classification Output
```json
[
  { "id": "msg_001", "category": "Urgent", "confidence": 0.94, "reason": "Subject contains 'URGENT' and sender is a known client." },
  { "id": "msg_002", "category": "Newsletter", "confidence": 0.98, "reason": "Contains unsubscribe link and bulk-send headers." }
]
```

### Thread Summary
```
**Thread:** Q3 Budget Review
**Participants:** Alice (Finance), Bob (Engineering), Carol (Product)
**Topic:** Approval process for Q3 engineering headcount

**Decisions Made:**
- 3 new engineering hires approved for Q3
- Budget ceiling set at $450k

**Open Questions:**
- Recruiting timeline not yet confirmed (Bob to follow up)

**Action Items:**
- Bob: Share JD drafts by Friday
- Alice: Update budget tracker by EOD Monday
```

## Examples

### Example Input
```
Write a professional follow-up email to a client who hasn't responded to our proposal in 2 weeks. Keep it brief and not pushy.
```

### Example Output
```
Subject: Checking In — Partnership Proposal

Hi [Client Name],

I hope you're doing well. I wanted to check in on the proposal I sent over on [Date].
I know things can get busy, so I'm happy to answer any questions or adjust any details
to better fit your needs.

If the timing isn't right, no worries — just let me know and we can revisit when it works for you.

Best,
[Your Name]
```

## Boundaries

- Do NOT send emails on behalf of the user without explicit confirmation of the recipient, subject, and content.
- Do NOT access or read email accounts unless the user has configured the appropriate API credentials.
- Do NOT store or log email content beyond the immediate task — treat all email data as sensitive.
- Do NOT generate emails that are deceptive, impersonate someone, or are intended for spam or phishing.
- Always preserve the user's stated tone — do not inject formality that contradicts their request.
- If an email contains PII or sensitive business information, handle it with care and do not include it in logs or summaries that could be exposed.
