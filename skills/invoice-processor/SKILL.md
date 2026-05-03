---
name: invoice-processor
description: Extracts structured line items, totals, and vendor data from invoice PDFs or images and routes them for approval. Invoke when asked to process an invoice, extract invoice data, parse a bill, automate accounts payable, or route invoices for approval.
---

# Invoice Processor

Extracts structured financial data from invoice PDFs, scanned images, and email attachments — capturing vendor details, line items, totals, and payment terms — and routes invoices through configurable approval workflows with validation and exception handling.

## When to Use

- User provides an invoice PDF or image and needs the data extracted
- Accounts payable workflow requires automated invoice ingestion
- Multiple invoices need to be batch-processed and entered into a system
- An invoice needs to be validated against a purchase order or contract
- Invoice data needs to be exported to an accounting system (QuickBooks, Xero, SAP, NetSuite)
- User asks to automate the invoice approval routing process
- Duplicate or fraudulent invoices need to be detected

## Process

1. **Ingest the document**:
   - Accept: PDF, JPEG/PNG scan, TIFF, email attachment, or forwarded email body
   - Detect document type: standard invoice, credit memo, pro forma invoice, receipt, or statement
   - Assess quality: if the document is blurry, skewed, or low-resolution, attempt deskewing and enhance contrast before extraction; flag if quality is too low for reliable extraction

2. **Extract structured fields using OCR and NLP**:

   **Header fields**:
   - Invoice number / reference ID
   - Invoice date and due date
   - PO number (if referenced)
   - Vendor name, address, tax ID / VAT number, contact email/phone
   - Bill-to name and address
   - Ship-to name and address (if different)
   - Payment terms (e.g., "Net 30", "Due on receipt")
   - Currency

   **Line items** (for each line):
   - Description / item name
   - Quantity
   - Unit price
   - Discount (if applicable)
   - Line total (quantity × unit price − discount)

   **Footer fields**:
   - Subtotal
   - Tax amount and tax rate(s)
   - Shipping / handling charges
   - Total amount due
   - Bank details / payment instructions (IBAN, ACH, wire)

3. **Validate extracted data**:
   - Verify arithmetic: confirm subtotal = sum of line totals; total = subtotal + tax + shipping
   - Flag discrepancies (e.g., line items sum to $1,480 but subtotal reads $1,450) as extraction errors or document errors
   - Cross-reference against any provided PO: check vendor, amounts, and line items match
   - Detect potential duplicates: flag invoices with same vendor + amount + invoice number as a prior processed invoice
   - Validate dates: due date should be ≥ invoice date; invoice date should not be more than 90 days in the past (flag as stale)

4. **Flag exceptions**:
   - 🔴 **High priority**: arithmetic mismatch, duplicate invoice, missing mandatory fields (invoice number, amount, vendor), amounts above approval threshold
   - 🟡 **Medium**: missing PO reference, date anomalies, unfamiliar vendor name, unusually large line item
   - 🟢 **Low**: minor formatting issues, optional fields absent

5. **Route for approval**:
   - Apply approval routing rules based on: invoice amount, vendor, department/cost center, or expense category
   - Default rules (customizable):
     - ≤ $500: auto-approve if PO matches
     - $500–$5,000: line manager approval
     - > $5,000: finance director approval
   - Output: approval task assigned to the appropriate approver with invoice summary attached

6. **Export to accounting system**:
   - Format the extracted data as the target system's required format (JSON, CSV, XML, API payload)
   - Map fields to accounting system schema (e.g., vendor → supplier_name, total_due → invoice_amount)
   - Include: extracted values, confidence scores, and flags for human review

## Output Format

### Extracted Invoice Data
```json
{
  "document_type": "Invoice",
  "extraction_confidence": 0.97,
  "flags": [],
  "header": {
    "invoice_number": "INV-2025-00482",
    "invoice_date": "2025-06-01",
    "due_date": "2025-07-01",
    "payment_terms": "Net 30",
    "po_number": "PO-8821",
    "currency": "USD",
    "vendor": {
      "name": "Acme Design Studio",
      "address": "123 Creative Blvd, Austin, TX 78701",
      "tax_id": "82-1234567",
      "email": "billing@acmedesign.com"
    },
    "bill_to": {
      "name": "Globex Corporation",
      "address": "456 Corporate Ave, New York, NY 10001"
    }
  },
  "line_items": [
    { "description": "Logo Redesign", "qty": 1, "unit_price": 2500.00, "total": 2500.00 },
    { "description": "Brand Style Guide", "qty": 1, "unit_price": 1500.00, "total": 1500.00 }
  ],
  "totals": {
    "subtotal": 4000.00,
    "tax_rate_pct": 8.25,
    "tax_amount": 330.00,
    "shipping": 0.00,
    "total_due": 4330.00
  },
  "payment_instructions": {
    "bank": "Chase Bank",
    "account": "****4821",
    "routing": "021000021"
  },
  "validation": {
    "arithmetic_check": "PASS",
    "duplicate_check": "PASS",
    "po_match": "PASS"
  },
  "routing": {
    "approval_required": true,
    "approver": "finance_director@globex.com",
    "reason": "Amount $4,330 exceeds $5,000 manager threshold — routed to Finance Director"
  }
}
```

### Exception Report
```
🔴 EXCEPTION: INV-2025-00483
Issue: Arithmetic mismatch — line items sum to $1,480.00 but subtotal reads $1,450.00. Difference: $30.00.
Action: Flagged for manual review. Do NOT auto-approve until vendor confirms correct total.
Assigned to: ap-review@company.com
```

## Examples

### Example Input
```
Extract all data from this invoice PDF and check if the math is correct. Route it for approval.
```

### Example Output
```
✅ Extraction complete (confidence: 96%)

Invoice: INV-2025-00482 | Vendor: Acme Design Studio | Total Due: $4,330.00
Due Date: July 1, 2025 | PO Match: ✅ PO-8821

Line Items:
1. Logo Redesign × 1 — $2,500.00
2. Brand Style Guide × 1 — $1,500.00
Subtotal: $4,000.00 + 8.25% tax ($330.00) = $4,330.00 ✅ Math verified.

No duplicates found. Routing to finance_director@globex.com for approval ($4,330 > $5,000 threshold).
```

## Boundaries

- Do NOT auto-approve invoices without human sign-off when amounts exceed the defined threshold.
- Flag all arithmetic mismatches and duplicate invoice candidates for human review — never process them silently.
- Do NOT store invoice data, including bank account or tax ID details, beyond the immediate processing task.
- Treat all extracted financial data as confidential — do not log or expose vendor banking details in plain-text outputs that could be intercepted.
- If extraction confidence is below 85% for critical fields (total amount, vendor name, invoice number), flag for manual re-entry rather than proceeding with low-quality data.
- Do NOT make payment on behalf of the user — output is for review and system ingestion only.
