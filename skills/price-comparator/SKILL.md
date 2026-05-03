---
name: price-comparator
description: Searches multiple e-commerce platforms for a product and returns a ranked comparison of prices, sellers, and shipping. Invoke when asked to compare prices, find the best deal, search for a product across stores, or check if a price is competitive.
---

# Price Comparator

Searches multiple e-commerce platforms and retailers for a specified product, collects current price, seller, shipping cost, and availability data, and returns a ranked comparison table with a clear best-deal recommendation.

## When to Use

- User wants to find the cheapest price for a specific product
- User asks "where can I buy X?" or "what's the best deal on Y?"
- A purchasing decision needs to be supported with current market pricing
- User wants to know if a given price is competitive or above market rate
- Product procurement requires vetting multiple vendors before purchase
- User is price-monitoring a product for purchase timing (price drop detection)

## Process

1. **Parse the product query**:
   - Extract: product name, model number (if given), key specifications (size, color, variant), preferred condition (new/used/refurbished), and target geography/currency
   - Resolve ambiguities: if multiple products match the name, list the top candidates and ask for confirmation
   - Note any constraints: max budget, preferred retailers, shipping speed requirements

2. **Search target platforms**:
   - Default platforms: Amazon, Walmart, eBay, Best Buy, Target, Google Shopping, and any retailer the user specifies
   - Match only exact or verified-equivalent products — do NOT include look-alike products with different model numbers
   - Collect for each listing: seller name, price (item only), shipping cost, estimated delivery date, seller rating, stock availability, and listing URL

3. **Normalize data for comparison**:
   - Compute **total landed cost** = item price + shipping cost (excluding tax, which varies by location)
   - Convert currencies to a single target currency if listings span multiple regions
   - Standardize condition labels: New / Used / Refurbished / Open-Box
   - Note: "free shipping" → $0.00 shipping cost; "price includes shipping" → list as combined total

4. **Validate listing quality**:
   - Flag third-party sellers with < 95% positive feedback rating or < 50 reviews
   - Flag listings where the price is significantly below market (>40% under next-lowest price) as potentially counterfeit or fraudulent
   - Check stock status: "In Stock", "Limited Stock" (≤5 units), "Pre-Order", "Out of Stock"

5. **Rank results**:
   - Primary sort: total landed cost (lowest first)
   - Secondary sort: delivery speed (faster preferred at equal price)
   - Tertiary sort: seller reputation (higher rating preferred)
   - Separate tables for: New / Used / Refurbished if multiple conditions are found

6. **Compute price statistics**:
   - Lowest price, highest price, median price, average price across all valid listings
   - Percentage saved vs. MSRP (if MSRP is known)
   - Price trend note: if this is a newly released product vs. mature market

7. **Generate recommendation**:
   - Best overall deal (lowest landed cost from a reputable seller)
   - Best for speed (fastest delivery at reasonable price premium)
   - Best trusted seller (largest, most reputable retailer, useful if trust matters more than price)

## Output Format

```
## Price Comparison: Sony WH-1000XM5 Headphones (New)
**Searched:** Amazon, Best Buy, Walmart, eBay | **Currency:** USD | **As of:** June 1, 2025

| Rank | Seller       | Item Price | Shipping | Total Cost | Delivery     | Seller Rating | Stock       |
|------|--------------|-----------|----------|------------|--------------|---------------|-------------|
| 1    | Walmart      | $279.00   | Free     | $279.00    | 2–3 days     | Official      | In Stock ✅  |
| 2    | Amazon       | $279.00   | Free     | $279.00    | 1–2 days     | Official      | In Stock ✅  |
| 3    | Best Buy     | $299.00   | Free     | $299.00    | 2 days       | Official      | In Stock ✅  |
| 4    | eBay (3rdPty)| $259.00   | $12.99   | $271.99    | 5–8 days     | 98.2% (1.2K)  | 3 left ⚠️   |
| 5    | eBay (3rdPty)| $245.00   | Free     | $245.00    | 7–10 days    | 94.1% (87)    | In Stock ⚠️ |

**⚠️ Flag:** eBay listing at $245.00 is 12% below lowest major retailer price and seller has < 100 reviews — exercise caution.

### Summary Statistics
- Lowest price (trusted seller): **$279.00** (Walmart or Amazon)
- MSRP: $349.00 | Savings vs. MSRP: **20%**
- Market median: $289.00

### Recommendation
🏆 **Best Deal:** Amazon at $279.00 with free 1–2 day Prime shipping — same price as Walmart but faster delivery.
⚡ **Best for Speed:** Amazon Prime (1–2 days).
🏪 **Best Trusted Retailer:** Amazon or Best Buy (official warranty, easy returns).
```

## Examples

### Example Input
```
Compare prices for the iPad Air 11-inch M2 (128GB, Wi-Fi, Space Gray) across major US retailers.
```

### Example Output
```
Searching Amazon, Best Buy, Walmart, Apple, Target for iPad Air 11" M2 128GB Wi-Fi Space Gray...

Found 6 listings from official retailers.

| Rank | Seller    | Price    | Shipping | Total    | Delivery   |
|------|-----------|----------|----------|----------|------------|
| 1    | Walmart   | $499.00  | Free     | $499.00  | 2 days     |
| 2    | Amazon    | $499.00  | Free     | $499.00  | 1–2 days   |
| 3    | Apple     | $599.00  | Free     | $599.00  | 2–3 days   |
| 4    | Best Buy  | $599.00  | Free     | $599.00  | Same-day ⚡ |

Best deal: Amazon or Walmart at $499.00 (save $100 vs. Apple). For same-day pickup, Best Buy matches Apple's price.
```

## Boundaries

- Only compare identical products (same model number, condition, and variant) — never substitute a similar product without flagging it clearly.
- Do NOT include listings with suspiciously low prices from unverified sellers without a prominent warning.
- Prices are time-sensitive — always display the timestamp of data collection and advise the user to verify before purchasing.
- Do NOT make purchasing decisions on behalf of the user — surface options and recommendations only.
- Flag affiliate or sponsored listings if detectable; prioritize organic results.
- If data for a requested platform is unavailable, note the gap rather than silently omitting it.
