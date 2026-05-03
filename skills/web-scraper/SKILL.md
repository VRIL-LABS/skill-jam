---
name: web-scraper
description: Extracts structured data from websites, handling pagination, JavaScript rendering, and rate limiting. Invoke when asked to scrape a website, extract data from web pages, crawl URLs, harvest structured content, or automate web data collection.
---

# Web Scraper

Extracts structured data from any website — handling static HTML, JavaScript-rendered pages, pagination, authentication walls, and rate limiting — and returns clean, structured output ready for downstream processing.

## When to Use

- User wants to extract product listings, prices, or reviews from an e-commerce site
- User needs to harvest article text, metadata, or links from a news or blog site
- A dataset must be built by collecting structured records across many pages
- User asks to "scrape", "crawl", "extract data from", or "harvest" a URL
- An automated pipeline needs to pull live data from a website on a schedule
- User needs to monitor a page for changes and capture diffs over time

## Process

1. **Analyze the target URL and content type**:
   - Determine whether the page is static HTML or JavaScript-rendered (check for `<script>` tags that load content dynamically)
   - Identify the data schema: what fields are needed and where do they appear in the DOM?
   - Check for a `robots.txt` and note any disallowed paths or crawl delays

2. **Select the extraction strategy**:
   - **Static HTML**: Use `requests` + `BeautifulSoup` (Python) or `cheerio` (Node.js)
   - **JavaScript-rendered**: Use `Playwright` or `Puppeteer` to render the page before parsing
   - **APIs hiding behind the UI**: Inspect network traffic (XHR/fetch calls) — hitting the API directly is faster and more reliable
   - **Structured data already present**: Check for JSON-LD (`<script type="application/ld+json">`), Open Graph tags, or schema.org microdata

3. **Handle pagination and navigation**:
   - Detect pagination pattern: URL query parameter (`?page=2`), path segment (`/page/2`), infinite scroll, or "Load More" button
   - For query-parameter pagination: iterate pages until response is empty or a sentinel value is reached
   - For infinite scroll: scroll the viewport incrementally with Playwright, waiting for new content to load

4. **Implement rate limiting and politeness**:
   - Respect `Crawl-delay` from `robots.txt`; default to 1–2 seconds between requests if none specified
   - Randomize delay within ±50% of the target to avoid fingerprinting
   - Use rotating user-agent strings drawn from a realistic pool
   - Back off exponentially on 429 or 503 responses (2s → 4s → 8s → give up after 3 retries)

5. **Extract and normalize fields**:
   - Use CSS selectors or XPath to target each field precisely
   - Strip HTML entities, extra whitespace, and boilerplate text
   - Normalize dates to ISO 8601, prices to a `{amount, currency}` object, and URLs to absolute form

6. **Handle errors and gaps**:
   - Log missing fields per record rather than dropping the entire record
   - Detect CAPTCHAs or login walls and surface them as explicit errors with remediation advice
   - Validate extracted records against the expected schema before returning

7. **Return structured output**:
   - Default format: JSON array of objects (one per scraped record)
   - Include scrape metadata: `source_url`, `scraped_at` (ISO 8601), `page_count`, `record_count`

## Output Format

```json
{
  "metadata": {
    "source_url": "https://example.com/products",
    "scraped_at": "2025-06-01T14:32:00Z",
    "page_count": 5,
    "record_count": 120
  },
  "records": [
    {
      "title": "Wireless Headphones Pro",
      "price": { "amount": 79.99, "currency": "USD" },
      "rating": 4.5,
      "review_count": 312,
      "url": "https://example.com/products/wireless-headphones-pro"
    }
  ]
}
```

## Examples

### Example Input
```
Scrape all product names and prices from https://books.toscrape.com — there are multiple pages.
```

### Example Output
```python
import requests
from bs4 import BeautifulSoup
import time, random, json
from datetime import datetime, timezone

BASE_URL = "https://books.toscrape.com/catalogue/"
records = []
page = 1

while True:
    url = f"{BASE_URL}page-{page}.html" if page > 1 else "https://books.toscrape.com/catalogue/"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code == 404:
        break
    soup = BeautifulSoup(resp.text, "html.parser")
    for article in soup.select("article.product_pod"):
        records.append({
            "title": article.h3.a["title"],
            "price": article.select_one(".price_color").text.strip(),
            "url": "https://books.toscrape.com/catalogue/" + article.h3.a["href"]
        })
    page += 1
    time.sleep(random.uniform(0.8, 1.5))

print(json.dumps({
    "metadata": {"scraped_at": datetime.now(timezone.utc).isoformat(), "record_count": len(records)},
    "records": records
}, indent=2))
```

## Boundaries

- Always check `robots.txt` before scraping and respect `Disallow` rules and `Crawl-delay`.
- Do NOT bypass authentication mechanisms or scrape content behind a login without explicit user confirmation that they are authorized to do so.
- Do NOT extract personally identifiable information (PII) unless the user explicitly needs it and confirms they have legal authority to collect it.
- Do NOT ignore HTTP 429/503 responses — always back off before retrying.
- Do NOT scrape at rates that could constitute a denial-of-service — cap at one request per second by default.
- Flag CAPTCHA walls as an explicit blocker; do NOT attempt to solve CAPTCHAs automatically.
- Remind users that scraping may violate a site's Terms of Service — this is their responsibility to verify.
