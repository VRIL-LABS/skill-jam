---
name: language-translator
description: Translates text across 100+ languages while preserving tone, formatting, and domain-specific terminology. Invoke when asked to translate text, localize content, convert between languages, or adapt copy for a specific locale or audience.
---

# Language Translator

Translates text across 100+ languages with high fidelity, preserving the original tone, formatting, intent, and domain-specific terminology — and optionally adapting content for cultural nuance and locale-specific conventions.

## When to Use

- User provides text and asks to translate it to another language
- Marketing, legal, technical, or UI copy needs to be localized for a new market
- A document needs to be rendered in multiple languages simultaneously
- User asks to "localize" content, not just translate it
- Translation quality needs to be checked or improved for an existing translation
- A glossary of domain terms must be applied consistently across a large document
- User needs to detect the language of unknown input text

## Process

1. **Detect source language** (if not specified):
   - Identify the source language and confidence score
   - Flag if the text appears to be multilingual (code-switching) and ask how to handle it

2. **Understand the translation requirements**:
   - Target language and locale/region (e.g., `pt-BR` vs `pt-PT`; `zh-CN` vs `zh-TW`)
   - Domain: legal, medical, technical, marketing, casual, UI strings, etc.
   - Tone: formal, informal, business, conversational — match the source unless instructed otherwise
   - Any glossary or terminology overrides (e.g., "always translate 'widget' as 'componente'")
   - Formatting constraints: preserve HTML tags, Markdown, placeholders (`{{name}}`), or YAML keys

3. **Translate with fidelity**:
   - Preserve paragraph structure, bullet points, headers, and inline formatting
   - Do NOT translate: proper nouns (people, brands, product names) unless a translation is standard, code blocks, URLs, HTML/Markdown syntax, or placeholder variables (e.g., `{{user_name}}`, `%s`)
   - Maintain register (formal ↔ informal) consistent with the source and audience context
   - When multiple valid translations exist, choose the most idiomatic phrasing for native speakers

4. **Handle domain-specific terminology**:
   - Apply user-provided glossary terms without deviation
   - For technical, legal, or medical content: use established domain terminology rather than literal word-for-word translation
   - Flag terms with no direct equivalent in the target language and propose transliterations or descriptive phrases

5. **Cultural localization** (when requested):
   - Adapt idioms, metaphors, and cultural references to equivalents that resonate in the target culture
   - Adjust date/time formats, number formats, currency symbols, and units for the locale
   - Flag any content that may be inappropriate, offensive, or misinterpreted in the target culture

6. **Format the output**:
   - Return the translation in the same structural format as the input (Markdown → Markdown, JSON → JSON)
   - If translating multiple languages, return a labeled block per language
   - When a glossary was used, list the applied term mappings at the end

7. **Quality assurance**:
   - Review for back-translation accuracy on key phrases
   - Flag any segments that were ambiguous in the source and may have been translated with assumptions
   - Note any missing context that would improve translation quality

## Output Format

### Single Translation
```
**Source (EN):** The settings panel allows you to configure user permissions and notification preferences.

**Translation (FR):** Le panneau des paramètres vous permet de configurer les autorisations des utilisateurs et les préférences de notification.
```

### Multi-Language Output
```
**EN (source):** Welcome to your dashboard.

**FR:** Bienvenue sur votre tableau de bord.
**DE:** Willkommen in Ihrem Dashboard.
**ES:** Bienvenido a su panel de control.
**JA:** ダッシュボードへようこそ。
**ZH-CN:** 欢迎来到您的仪表板。
```

### JSON Localization File
```json
{
  "welcome_message": "Bienvenue sur votre tableau de bord.",
  "settings_label": "Paramètres",
  "save_button": "Enregistrer",
  "cancel_button": "Annuler"
}
```

### With Glossary Notes
```
**Translation (DE):** Bitte überprüfen Sie die Nutzungsbedingungen, bevor Sie Ihr Konto aktivieren.

**Applied Glossary Terms:**
- "Terms of Service" → "Nutzungsbedingungen" (per glossary)
- "activate" → "aktivieren" (standard DE tech term)
```

## Examples

### Example Input
```
Translate the following UI strings from English to Spanish (Latin America) and French. Keep HTML tags and {{placeholders}} intact.

"Hello, {{name}}! Your <strong>free trial</strong> expires in {{days}} days."
```

### Example Output
```
**ES-419:** ¡Hola, {{name}}! Tu <strong>prueba gratuita</strong> vence en {{days}} días.

**FR:** Bonjour, {{name}} ! Votre <strong>essai gratuit</strong> expire dans {{days}} jours.

Notes:
- HTML tag <strong> preserved in both translations.
- Placeholders {{name}} and {{days}} left untouched.
- Used "vence" (ES-419) for "expires" — standard LatAm Spanish; "caduca" used in ES-ES.
```

## Boundaries

- Do NOT translate proper nouns (brand names, personal names, product names) unless the user explicitly asks or a standard translation exists.
- Do NOT omit or modify placeholders, HTML tags, code blocks, or structural markup — preserve them verbatim.
- Do NOT assume a single "Spanish" or "Chinese" without confirming the target locale (es-ES vs es-419; zh-CN vs zh-TW).
- Always flag idioms or cultural references that don't have a direct equivalent rather than silently substituting a literal translation.
- For legal, medical, or financial documents, recommend human review by a certified translator before official use.
- If the source text is ambiguous, state the assumption made and offer an alternative translation for the other interpretation.
