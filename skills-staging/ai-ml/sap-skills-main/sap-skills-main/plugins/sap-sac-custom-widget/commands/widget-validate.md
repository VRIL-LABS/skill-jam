---
name: widget-validate
description: Validates SAC custom widget JSON metadata and JavaScript structure for correctness and best practices
allowed-tools:
  - Read
  - Grep
argument-hint: [file_path]
---

# SAC Custom Widget Validation Command

Validate SAP Analytics Cloud custom widget files (widget.json and widget.js) for schema compliance, required fields, and best practices.

## Usage

```
/widget-validate [file_path]
/widget-validate widget.json
/widget-validate src/widget.js
/widget-validate --all
```

## Validation Categories

### 1. widget.json Schema Validation

**Required Root Fields**:
- `id` - Unique identifier (reverse domain notation: com.company.widget)
- `version` - Semantic version (1.0.0)
- `name` - Display name
- `vendor` - Company/author name
- `webcomponents` - Array of component definitions

**Required webcomponents Fields**:
- `kind` - Component type (main, styling, builder)
- `tag` - HTML custom element tag (lowercase with hyphens)
- `url` - JavaScript file URL

**Optional but Recommended**:
- `description` - Widget description
- `license` - License type
- `icon` - Widget icon path
- `integrity` - SHA256 hash for production
- `properties` - Property definitions
- `methods` - Script-callable methods
- `events` - Custom events
- `dataBindings` - Data binding configuration

### 2. widget.js Structure Validation

**Required Elements**:
- Web Component class extending HTMLElement
- `customElements.define()` call matching tag in JSON
- `attachShadow({ mode: "open" })` for Shadow DOM

**Required Lifecycle Functions**:
- `onCustomWidgetBeforeUpdate(changedProperties)`
- `onCustomWidgetAfterUpdate(changedProperties)`

**Recommended Lifecycle Functions**:
- `onCustomWidgetResize()`
- `onCustomWidgetDestroy()`

**Property Patterns**:
- Getter/setter for each defined property
- `propertiesChanged` event dispatch on set

### 3. Data Binding Validation

If `dataBindings` is defined:
- Each binding must have `feeds` array
- Feeds must have `id`, `description`, `type`
- Valid feed types: `dimension`, `mainStructureMember`, `measure`

### 4. Security Validation

**Production Readiness**:
- `ignoreIntegrity` should be `false` for production
- `integrity` hash should be present and valid
- URLs should use HTTPS

**Warning-Level**:
- `ignoreIntegrity: true` (development only)
- HTTP URLs (not recommended)
- Missing CORS considerations in comments

## Validation Process

1. **Identify file type** (JSON or JavaScript)
2. **Parse and validate structure**
3. **Check required fields and patterns**
4. **Cross-validate JSON and JS** (if both present)
5. **Report findings with severity levels**

## Output Format

```
## SAC Widget Validation Report

**File**: [filename]
**Type**: [widget.json / widget.js]
**Status**: [PASS / FAIL / WARNINGS]

### Critical Issues (X found)
1. [Line X]: [Issue description]
   **Current**: `[problematic code]`
   **Required**: `[correct pattern]`

### Warnings (X found)
1. [Line X]: [Issue description]
   **Recommendation**: [How to fix]

### Suggestions (X found)
1. [Issue description]
   **Best Practice**: [Recommendation]

### Summary
- Critical: X (must fix)
- Warnings: X (should fix)
- Suggestions: X (consider)

### Cross-Validation
[Results of JSON ↔ JS consistency check if applicable]
```

## Examples

### Validate widget.json
```
/widget-validate widget.json
```

### Validate widget.js
```
/widget-validate widget.js
```

### Validate All Widget Files
```
/widget-validate --all
```

## Validation Rules Detail

### Tag Naming Convention
```json
// GOOD: lowercase with hyphens
"tag": "my-custom-widget"

// BAD: uppercase or underscores
"tag": "MyCustomWidget"
"tag": "my_custom_widget"
```

### Property Type Validation
```json
// Valid types
"type": "string"
"type": "integer"
"type": "number"
"type": "boolean"
"type": "array"
"type": "object"
"type": "Color"     // SAC special type
"type": "Selection" // SAC special type
```

### Lifecycle Function Check
```javascript
// REQUIRED - will fail validation if missing
onCustomWidgetBeforeUpdate(changedProperties) { }
onCustomWidgetAfterUpdate(changedProperties) { }

// RECOMMENDED - warning if missing
onCustomWidgetResize() { }
onCustomWidgetDestroy() { }
```

### customElements.define Match
```javascript
// Tag in widget.json
"tag": "my-widget"

// Must match in widget.js
customElements.define("my-widget", MyWidget);
```

## Implementation Instructions

When this command is invoked:

1. Parse the file path argument
2. If `--all`, find all widget.json and widget.js files in the project
3. For each file:
   - Read file contents
   - Determine file type (JSON or JavaScript)
   - Apply appropriate validation rules
   - Record issues with line numbers where possible
4. If both widget.json and widget.js found in same directory:
   - Cross-validate tag names
   - Verify property definitions match getters/setters
   - Check event definitions match dispatches
5. Present findings in the format above
6. Provide summary with counts by severity
