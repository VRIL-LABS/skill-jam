---
name: legal-document-reviewer
description: Scans contracts and legal documents for risky clauses, non-standard terms, missing provisions, and regulatory compliance issues. Invoke when asked to review a contract, analyze legal terms, flag risky clauses, check for missing provisions, or summarize legal documents in plain language.
---

# Legal Document Reviewer

Analyzes contracts, agreements, terms of service, NDAs, and other legal documents to identify risky or non-standard clauses, flag missing provisions, surface potential compliance issues, and produce plain-language summaries — accelerating legal review and helping non-lawyers understand what they're agreeing to.

## When to Use

- User provides a contract or legal document and asks for a review
- A vendor agreement, SaaS contract, or NDA needs to be analyzed before signing
- Non-standard or unusual clauses need to be flagged for negotiation
- User asks "what should I watch out for in this contract?"
- A document needs to be summarized in plain language for a non-legal audience
- Compliance requirements (GDPR, HIPAA, SOC 2) need to be verified against contract terms
- A contract needs to be compared against a standard template or prior version

## Process

1. **Identify the document type and context**:
   - Document type: NDA, SaaS/software agreement, employment contract, vendor agreement, service agreement, partnership agreement, consulting agreement, IP assignment, lease, terms of service
   - Governing law and jurisdiction (note if not specified — this is itself a flag)
   - Parties: who is the client/user side, who is the counter-party?
   - Purpose: what business relationship does this document govern?

2. **Extract and analyze key provisions**:

   **Core commercial terms**:
   - Scope of services or license grant — is it broad enough for intended use? Are there unexpected exclusions?
   - Term and renewal: auto-renewal clauses, notice periods for cancellation, evergreen provisions
   - Payment terms: price, payment schedule, late fees, price change rights
   - Deliverables and milestones (for project-based contracts)

   **Liability and risk**:
   - Limitation of liability: is there a cap? Is it reasonable (e.g., 12 months of fees)? Are there carve-outs that effectively eliminate the cap?
   - Indemnification: who indemnifies whom, and for what? Broad mutual indemnification vs. one-sided?
   - Warranties and disclaimers: are key warranties present? Are implied warranties disclaimed aggressively?
   - Insurance requirements: are they proportionate?

   **IP and data rights**:
   - IP ownership: who owns work product, improvements, or derivative works created under this agreement?
   - Data rights: can the vendor use your data for training, benchmarking, or sharing with third parties?
   - License scope: are sublicense rights included or excluded?
   - Background IP protection: are pre-existing IP rights preserved?

   **Confidentiality and privacy**:
   - Definition of confidential information — is it adequately broad to protect your business information?
   - Exclusions from confidentiality — are they standard (public domain, independent development)?
   - Data processing terms: if applicable, is a DPA/Data Processing Agreement included or referenced?
   - GDPR/HIPAA/CCPA compliance: are required contractual provisions present?

   **Termination**:
   - Grounds for termination for cause: are they bilateral? Is cure period adequate?
   - Termination for convenience: available to which parties? Notice period?
   - Post-termination obligations: data return/deletion, wind-down assistance, survival clauses

   **Dispute resolution**:
   - Governing law and jurisdiction — is it favorable or far away?
   - Arbitration clause: binding arbitration, class action waiver?
   - Venue: is it impractical for you to litigate there?

3. **Identify risky or non-standard clauses**:
   - Compare against market-standard terms for the document type
   - Flag: one-sided provisions, unlimited liability exposure, rights to unilaterally change terms, broad IP assignments, aggressive audit rights, automatic renewal with short cancellation windows
   - Rate each flag: 🔴 High Risk · 🟡 Moderate Risk · 🟢 Minor / Standard Negotiation Point

4. **Identify missing provisions**:
   - What provisions are typically present in this contract type but absent here?
   - Examples: no limitation of liability clause, no data security addendum, no IP assignment clause, no dispute resolution provision, no confidentiality obligation

5. **Produce the review output**:
   - **Executive summary**: overall risk level (Low / Medium / High), 3–5 top issues to address
   - **Key terms table**: commercial terms at a glance
   - **Risk flags**: detailed explanation of each flagged clause with location, risk explanation, and suggested negotiation position
   - **Missing provisions**: what should be added before signing
   - **Plain-language summary**: what this contract actually means in plain English

## Output Format

```
## Contract Review Report
**Document:** Software Subscription Agreement — VendorCo
**Reviewer Role:** Customer (signing party)
**Governing Law:** Delaware | **Effective Date:** [TBD]
**Overall Risk Level:** 🟡 MEDIUM (4 high/moderate risk items identified)

---

### Key Commercial Terms
| Term                  | Detail                                      |
|-----------------------|---------------------------------------------|
| Subscription term     | 1 year, auto-renews annually                |
| Cancellation notice   | 90 days before renewal ⚠️ (unusually long) |
| Pricing change notice | 30 days (vendor can increase price)         |
| Liability cap         | 3 months of fees paid ⚠️ (below market)    |
| Governing law         | Delaware, exclusive jurisdiction            |

---

### 🔴 High Risk Flags

**1. Unlimited IP License to Customer Data (Section 8.3)**
> "Customer grants VendorCo a perpetual, irrevocable, worldwide license to use Customer Data for any purpose, including product improvement and third-party sharing."

**Risk:** VendorCo can use your data — including confidential business data — to improve their product, share with third parties, and potentially train AI models, with no restrictions and no ability to revoke.
**Negotiation Position:** Limit data use to "providing the Services only." Add: "VendorCo shall not use Customer Data for any purpose other than to provide the Services and shall not share Customer Data with third parties without Customer's prior written consent."

---

### 🟡 Moderate Risk Flags

**2. Limitation of Liability Cap: 3 Months of Fees (Section 14.2)**
Liability cap is 3 months of fees paid (~$750 for a $3K/year contract). Market standard is 12 months.
**Negotiation Position:** Request 12 months of fees paid, and ensure IP infringement and data breach claims are carved out from the cap entirely.

**3. 90-Day Cancellation Notice for Annual Renewal (Section 3.1)**
You must cancel 90 days before the renewal date or auto-renew for another full year.
**Negotiation Position:** Request 30-day notice period, which is market standard. Also request a reminder notification from VendorCo 120 days before renewal.

---

### ⚠️ Missing Provisions

1. **No Data Processing Agreement (DPA)** — Required for GDPR compliance if any EU personal data is processed. Request a DPA addendum before signing.
2. **No Security Incident Notification** — Contract does not require VendorCo to notify you of data breaches. Request: notification within 72 hours of discovering a security incident involving your data.
3. **No Service Level Agreement (SLA)** — No uptime commitments or remedies for downtime. Request minimum 99.9% uptime SLA with service credits.

---

### Plain-Language Summary
This is a standard SaaS subscription agreement, but it has three areas of concern before signing:

1. **VendorCo wants very broad rights to your data.** The current language allows them to use your business data for almost anything, including sharing with third parties. This is unusual and should be narrowed.

2. **Your liability protections are weaker than normal.** If something goes wrong, VendorCo's financial responsibility is capped at just 3 months of what you paid them — market standard is 12 months.

3. **Cancellation timing is tricky.** If you want to leave at the annual renewal, you must tell them 90 days before — that's a longer window than most contracts. Miss it and you're locked in for another year.

The rest of the contract is fairly standard. Fixing these three points through negotiation would bring this agreement to a reasonable market standard.
```

## Examples

### Example Input
```
Review this NDA I received from a potential partner. Flag anything unusual and give me a plain-language summary.
```

### Example Output
```
NDA Review — Mutual Non-Disclosure Agreement
Parties: You (Disclosing/Receiving) ↔ PartnerCo (Disclosing/Receiving)
Overall Risk: 🟢 Low (1 minor flag)

Key Terms:
- Confidentiality period: 3 years from disclosure (standard)
- Definition of confidential info: broad, covers both written and oral disclosures (standard)
- Exclusions: public domain, independent development, compelled disclosure (standard)
- Governing law: New York (common for commercial NDAs)

⚠️ Minor Flag — No Return/Destruction of Materials Clause (Section 6)
Standard NDAs require that confidential information be returned or destroyed upon request or agreement end. This NDA is silent on this. Add: "Upon written request, each party shall promptly return or certify destruction of all confidential materials."

Plain English: This is a straightforward mutual NDA — both parties agree to keep each other's information confidential for 3 years. The only thing missing is a clear process for returning or destroying confidential materials when the relationship ends. Everything else looks standard.
```

## Boundaries

- **THIS IS NOT LEGAL ADVICE.** Always remind the user that this analysis is for informational purposes only and does not constitute legal advice. Recommend review by a qualified attorney before signing any legally binding agreement.
- Do NOT make definitive legal conclusions about enforceability, liability, or regulatory compliance — flag issues and recommend professional review.
- Do NOT fabricate legal citations, case law, or statutory references — only reference laws or standards you can accurately name.
- For documents involving GDPR, HIPAA, SOC 2, or other regulatory frameworks, provide a checklist-style flag but recommend a compliance specialist confirm.
- Treat all contract content as confidential — do NOT log, store, or reproduce contract terms outside the immediate review task.
- Flag when a contract is in a jurisdiction or language you cannot reliably analyze, rather than providing a low-quality review.
