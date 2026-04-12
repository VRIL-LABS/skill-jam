---
name: customer-support-bot
description: Triages incoming support tickets, suggests resolutions from a knowledge base, and escalates edge cases to humans. Invoke when asked to build a support bot, triage support tickets, auto-respond to customer inquiries, suggest resolutions from a knowledge base, or automate first-line customer support.
---

# Customer Support Bot

Triages incoming customer support tickets, matches issues to knowledge base articles or resolution patterns, generates accurate and empathetic responses, handles multi-step troubleshooting, and intelligently escalates unresolved or high-priority cases to human agents.

## When to Use

- User wants to automate first-line responses to customer support requests
- An incoming ticket queue needs to be triaged by issue type, priority, or sentiment
- A knowledge base or FAQ needs to be searched to suggest resolutions
- A support workflow requires intelligent routing (tier 1 self-service → tier 2 agent → tier 3 specialist)
- User asks to build a support chatbot for their product or service
- Post-resolution summaries need to be generated for support agents
- Support ticket volume needs to be analyzed for common issues and trends

## Process

1. **Intake and parse the ticket**:
   - Extract: customer name, account ID (if provided), product/service affected, issue description, and any attachments or error messages
   - Identify: the core problem type (billing, technical, account, feature request, feedback, complaint)
   - Detect: sentiment and urgency level — a frustrated, long-term customer with a billing issue warrants different urgency than a first-time feature question
   - Classify: ticket priority based on impact (service outage > data loss > incorrect charge > general question)

2. **Check for instant-resolution opportunities**:
   - Search the knowledge base (FAQs, help articles, previous similar tickets) for matching solutions
   - Confidence threshold: suggest a resolution if the match confidence is ≥ 80%
   - For common issue types, apply resolution patterns:
     - "Password reset" → standard reset flow instructions
     - "Can't log in" → check account status, 2FA, recent password change
     - "Charge question" → explain billing policy + direct to invoice
   - If the knowledge base has no match, proceed to guided troubleshooting

3. **Generate the response**:
   - Open with empathy and acknowledgment: recognize the customer's frustration without over-apologizing
   - State what you understand the issue to be (confirm understanding, reduce back-and-forth)
   - Provide the resolution or next troubleshooting step, clearly numbered if multi-step
   - Set expectations: if a manual review is needed, give a realistic time estimate
   - Close with a clear action (what the customer should do next, or what the agent will do)
   - Match tone to sentiment: frustrated customer → warmer, more reassuring tone; technical user → concise, precise

4. **Handle multi-step troubleshooting**:
   - Present one step at a time; wait for the customer to confirm before moving to the next
   - Track which steps have been tried (don't suggest steps already attempted)
   - After 3 unresolved troubleshooting steps, escalate to human agent with full context

5. **Escalation logic**:
   - **Auto-escalate immediately**:
     - Data breach or security concern
     - Service outage affecting multiple users
     - Legal, compliance, or regulatory issue
     - Customer explicitly requests a human
     - Extreme frustration or threat of churn/legal action
   - **Escalate after failed resolution**:
     - 3+ troubleshooting steps failed
     - Issue requires account-level access the bot doesn't have
     - Confidence in available resolution < 60%
   - **Escalation package** (sent to human agent): ticket summary, customer sentiment, steps already tried, recommended next step, relevant knowledge base articles

6. **Log and tag**:
   - Tag tickets with: issue category, product area, resolution type, escalation reason, customer sentiment
   - Track: first response time, resolution time, number of bot turns, escalation rate
   - Surface: trending issues (volume spike in a category signals a product bug or communication gap)

7. **Post-resolution follow-up**:
   - Send satisfaction survey (CSAT) 24 hours after resolution
   - Offer a knowledge base article link for self-service on related topics
   - Flag to product team if 3+ tickets in the same week share the same root cause → potential product bug or documentation gap

## Output Format

### Auto-Response to Customer
```
Hi Sarah,

Thanks for reaching out! I can see you're having trouble logging in to your account.

I understand how frustrating that can be, especially when you need access right away. Let me help you get back in.

**Step 1:** Try resetting your password here: [Reset Password Link]
This covers 80% of login issues and takes about 30 seconds.

If that doesn't work, I'll ask you a couple of quick questions to dig deeper.

If you'd rather speak with a person, just reply "agent" and I'll connect you right away.

— Acme Support

---
Ticket: #84921 | Response time: 45 seconds
```

### Escalation Package (to Human Agent)
```
🔴 Escalation — Ticket #84921
Priority: High | Sentiment: Frustrated (score: -0.72)
Customer: Sarah Chen | Account: PRO plan (2 years) | LTV: ~$2,400

Issue: Unable to log in. Customer says password reset emails are not arriving.

Steps already tried by bot:
✅ Suggested password reset — customer confirmed no email received
✅ Suggested checking spam folder — checked, not there
✅ Confirmed account is active (no suspension flag)

Suspected cause: Email delivery issue — customer's domain (acmecorp.com) may be blocking our transactional emails.

Recommended next step: Manually trigger a password reset from the admin console and check email delivery logs for acmecorp.com.

Relevant KB articles: Email Delivery Troubleshooting (#KB-441), Admin Password Override (#KB-219)
```

### Issue Trend Report
```
📊 Support Trends — Week of June 1, 2025
Total tickets: 1,243 | Bot-resolved: 847 (68%) | Escalated: 396 (32%)

🔴 Spike: "Export to CSV" failures — 87 tickets this week (up from 12 last week)
Likely cause: CSV export regression introduced in v2.4.1 deployment (June 3)
Recommendation: Immediate bug ticket to engineering team

Top issue categories:
1. Login / authentication — 23%
2. Billing questions — 18%
3. Data export — 14% ⬆️ (new spike)
4. Feature how-to — 12%
5. Account management — 11%
```

## Examples

### Example Input
```
A customer says: "I've been charged twice this month and I'm really upset. I need a refund immediately."
```

### Example Output
```
Response to customer:

Hi [Customer Name],

I'm really sorry this happened — being charged twice is absolutely not right, and I completely understand your frustration.

I'm looking into this for you right now. Can you confirm the last 4 digits of the card that was charged? This will help me locate the transactions immediately.

I'll get this resolved as quickly as possible, and if a refund is owed, I'll make sure it's processed right away.

— Support Team

---
[Internal: Ticket tagged as BILLING_DUPLICATE_CHARGE. High priority. If confirmed duplicate, process refund per billing policy and escalate to billing team if > $500.]
```

## Boundaries

- Do NOT promise outcomes you cannot guarantee (e.g., "Your refund will arrive in 24 hours") without confirming the policy applies.
- Always give customers a clear, easy path to reach a human agent — do NOT trap them in an endless bot loop.
- Do NOT access or modify account data without explicit authorization from the user's system.
- Escalate security and legal concerns immediately — do NOT attempt to resolve them through automated responses.
- Do NOT generate responses that are dismissive, shift blame to the customer, or use excessive legalese.
- Treat customer sentiment data with care — do NOT expose internal sentiment scores or ticket summaries to customers.
- Flag any ticket that contains threats of self-harm or harm to others to human staff immediately, bypassing standard routing.
