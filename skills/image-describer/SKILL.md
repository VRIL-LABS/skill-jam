---
name: image-describer
description: Generates detailed captions, alt text, and structured metadata for images using vision models. Invoke when asked to describe an image, generate alt text, caption a photo, extract text from an image, identify objects or scenes, or produce image metadata.
---

# Image Describer

Uses vision model capabilities to generate accurate, detailed, and purpose-appropriate descriptions of images — including natural-language captions, accessibility-focused alt text, OCR-extracted text, and structured metadata for classification or search.

## When to Use

- User provides an image and asks "what is this?" or "describe this"
- Alt text is needed for accessibility compliance (WCAG 2.1 AA)
- Product images need auto-generated captions for an e-commerce catalog
- Text in an image (screenshot, photo of a document, sign) needs to be extracted (OCR)
- Images need to be tagged with structured metadata for a content management system
- A visual chart or diagram needs to be interpreted and explained in text
- User wants to verify what an image contains before storing or publishing it

## Process

1. **Determine the description purpose**:
   - **General caption**: comprehensive description of what is in the image for sighted users
   - **Alt text**: concise, functional description for screen readers (WCAG-compliant)
   - **OCR / text extraction**: extract all readable text verbatim, preserving layout where relevant
   - **Object/scene detection**: enumerate objects, people, settings, and their spatial relationships
   - **Metadata/tagging**: produce a set of searchable tags, categories, and attributes
   - **Chart/diagram interpretation**: describe what the visualization shows and summarize key data points

2. **Analyze image content**:
   - Identify the primary subject and context (person, product, document, screenshot, chart, etc.)
   - Note: foreground/background elements, spatial relationships ("a dog sitting to the left of a person")
   - Identify text, logos, brands, or UI elements if present
   - Note color, style, mood, or visual quality if relevant to the use case
   - Flag any content that may be sensitive, offensive, or require content moderation

3. **Generate output matched to purpose**:

   **Alt Text (accessibility)**:
   - Be concise (≤125 characters when possible) and describe function, not aesthetics
   - Start with the subject: "A woman demonstrating..." not "Image of a woman..."
   - Skip phrases like "Image of", "Photo of", "Picture showing" — screen readers announce the image type
   - For decorative images, return an empty alt: `alt=""`
   - For charts: describe the key finding, not just the chart type ("Bar chart showing 40% increase in Q3 revenue")

   **General Caption**:
   - Write 1–3 sentences covering the most important elements
   - Include relevant context: setting, action, notable details, approximate time period if inferable
   - Maintain a neutral, objective tone unless a specific voice is requested

   **Structured Metadata**:
   - Return a JSON object with standardized fields
   - Include confidence scores for inferred attributes

4. **Extract text (OCR)**:
   - Return extracted text verbatim, preserving paragraph breaks and table structure where visible
   - Mark low-confidence characters or words with `[?]`
   - Indicate reading order (left-to-right, top-to-bottom by default; flag unusual layouts)

5. **Flag edge cases**:
   - Faces of identifiable individuals (note presence without identification)
   - Potentially sensitive or adult content
   - Images too blurry, dark, or low-resolution for confident analysis
   - Memes, humor, or cultural references that require broader context to interpret

## Output Format

### Alt Text
```
alt="A hiker standing on a rocky summit at sunset, looking out over a mountain range."
```

### General Caption
```
A lone hiker stands at the peak of a rocky summit during golden hour, silhouetted against
a vivid orange and pink sky. The mountain range stretches into the distance behind them,
partially obscured by low-lying clouds. The scene conveys a sense of solitude and achievement.
```

### Structured Metadata
```json
{
  "primary_subject": "Person",
  "scene": "Mountain summit, outdoors",
  "objects": ["hiker", "backpack", "rocky terrain", "clouds", "mountain range"],
  "colors": ["orange", "pink", "gray", "blue"],
  "mood": "Peaceful, contemplative",
  "time_of_day": "Sunset",
  "season": "Summer (inferred from clothing)",
  "text_present": false,
  "faces_detected": 1,
  "confidence": 0.91,
  "tags": ["hiking", "nature", "mountains", "sunset", "adventure", "outdoors"]
}
```

### OCR Output
```
INVOICE
Invoice #: 2025-00482
Date: June 1, 2025
Bill To: Acme Corporation

Description          Qty   Unit Price   Total
Web Design Services    1    $3,500.00   $3,500.00
SEO Audit              1      $500.00     $500.00
                                Total:  $4,000.00
```

## Examples

### Example Input
```
Generate WCAG-compliant alt text for this product image of a red running shoe on a white background.
```

### Example Output
```
alt="Red lightweight running shoe with white sole and mesh upper, shown from the side."
```

---

### Example Input
```
Extract all text from this screenshot of an error message.
```

### Example Output
```
TypeError: Cannot read properties of undefined (reading 'map')
    at ProductList (ProductList.jsx:24:18)
    at renderWithHooks (react-dom.development.js:14985:18)

This error occurred during server-side rendering. See the console for details.
```

## Boundaries

- Do NOT attempt to identify specific individuals by name in photos — describe people by appearance, role, or activity only.
- Do NOT generate descriptions that introduce biases about gender, race, age, or other protected characteristics.
- Flag images containing potentially sensitive content (nudity, violence, trauma) rather than silently describing them; ask how to proceed.
- For low-quality or ambiguous images, report uncertainty explicitly rather than guessing confidently.
- Do NOT fabricate text that is not clearly visible in the image; use `[?]` for uncertain characters.
- Alt text is for accessibility, not SEO stuffing — do not load it with keywords at the expense of accuracy.
