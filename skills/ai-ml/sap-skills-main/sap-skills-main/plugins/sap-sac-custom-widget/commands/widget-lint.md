---
name: widget-lint
description: Analyzes SAC custom widget code for performance issues, security concerns, and best practice violations
allowed-tools:
  - Read
  - Grep
  - Bash
argument-hint: [file_path]
---

# SAC Custom Widget Linter Command

Analyze SAP Analytics Cloud custom widget code for performance optimization opportunities, security concerns, and best practice compliance.

## Usage

```
/widget-lint [file_path]
/widget-lint widget.js
/widget-lint src/
/widget-lint --fix-suggestions
```

## Lint Categories

### 1. Performance Analysis

**Critical Performance Issues**:
- Large synchronous operations in lifecycle functions
- Missing debounce on resize handlers
- DOM manipulation inside loops
- Unnecessary re-renders
- Memory leaks (uncleaned event listeners, intervals)

**Performance Warnings**:
- Chart library not disposed properly
- No caching of expensive calculations
- Inline styles instead of CSS classes
- Synchronous third-party library loading

**Performance Suggestions**:
- Use requestAnimationFrame for animations
- Implement virtual scrolling for large datasets
- Lazy load third-party libraries
- Cache DOM element references

### 2. Security Analysis

**Critical Security Issues**:
- innerHTML with user-provided content (XSS risk)
- eval() or Function() usage
- document.write() calls
- Unsanitized URL parameters

**Security Warnings**:
- ignoreIntegrity: true in production
- HTTP URLs instead of HTTPS
- Missing Content Security Policy considerations
- Potential injection in dynamic SQL/queries

**Security Suggestions**:
- Use textContent instead of innerHTML
- Validate all external data
- Implement input sanitization
- Use HTTPS for all external resources

### 3. Best Practices Analysis

**Critical Best Practice Issues**:
- Missing onCustomWidgetBeforeUpdate or onCustomWidgetAfterUpdate
- No Shadow DOM (attachShadow not called)
- customElements.define not called
- Class not extending HTMLElement

**Best Practice Warnings**:
- Missing onCustomWidgetResize handler
- Missing onCustomWidgetDestroy cleanup
- No propertiesChanged event dispatch
- Hardcoded colors/fonts (should use SAP theming)

**Best Practice Suggestions**:
- Use SAP theme variables (--sapFontFamily, --sapTextColor)
- Implement proper error boundaries
- Add console.warn for debugging
- Include JSDoc comments for methods

### 4. SAC Integration Analysis

**Integration Issues**:
- Property setters without propertiesChanged dispatch
- Event dispatch with incorrect detail structure
- Method definitions in JSON not implemented in JS
- Data binding access without null checks

**Integration Warnings**:
- Properties defined but no getter/setter
- Events defined but never dispatched
- Methods defined but with wrong signature

## Lint Process

1. **Parse widget files** (JSON and JavaScript)
2. **Run static analysis** on JavaScript
3. **Check for patterns** in each category
4. **Score severity** of each finding
5. **Provide actionable recommendations**

## Output Format

```
## SAC Widget Lint Report

**Files Analyzed**: [list]
**Overall Score**: [X/100]

### Performance Issues (X found)

#### Critical
1. [Issue description]
   **Location**: [file:line]
   **Impact**: [Performance impact description]
   **Fix**: [Code suggestion]

#### Warnings
1. [Issue description]
   **Recommendation**: [How to improve]

### Security Issues (X found)

#### Critical
1. [Issue description]
   **Risk**: [Security risk description]
   **Fix**: [Required fix]

#### Warnings
1. [Issue description]
   **Recommendation**: [Security improvement]

### Best Practices (X found)

#### Violations
1. [Issue description]
   **Standard**: [Best practice reference]
   **Fix**: [Implementation suggestion]

### SAC Integration (X found)

1. [Issue description]
   **Impact**: [How it affects SAC integration]
   **Fix**: [Required change]

### Summary

| Category | Critical | Warnings | Suggestions |
|----------|----------|----------|-------------|
| Performance | X | X | X |
| Security | X | X | X |
| Best Practices | X | X | X |
| SAC Integration | X | X | X |

### Recommendations Priority

1. [Highest priority fix]
2. [Second priority fix]
3. [Third priority fix]
```

## Lint Rules Detail

### Performance Rules

#### P001: Debounce Resize Handler
```javascript
// BAD: Direct resize handling
onCustomWidgetResize() {
  this._render(); // Called too frequently
}

// GOOD: Debounced resize
onCustomWidgetResize() {
  clearTimeout(this._resizeTimeout);
  this._resizeTimeout = setTimeout(() => this._render(), 100);
}
```

#### P002: Cache DOM References
```javascript
// BAD: Query DOM on every render
_render() {
  this._shadowRoot.getElementById("chart").innerHTML = "";
}

// GOOD: Cache reference
constructor() {
  this._chartEl = this._shadowRoot.getElementById("chart");
}
_render() {
  this._chartEl.innerHTML = "";
}
```

#### P003: Dispose Chart Instances
```javascript
// BAD: No cleanup
onCustomWidgetDestroy() { }

// GOOD: Proper disposal
onCustomWidgetDestroy() {
  if (this._chart) {
    this._chart.dispose();
    this._chart = null;
  }
}
```

### Security Rules

#### S001: XSS Prevention
```javascript
// BAD: XSS vulnerability
element.innerHTML = userProvidedValue;

// GOOD: Safe text content
element.textContent = userProvidedValue;
```

#### S002: HTTPS URLs
```json
// BAD: HTTP URL
"url": "http://example.com/widget.js"

// GOOD: HTTPS URL
"url": "https://example.com/widget.js"
```

### Best Practice Rules

#### B001: SAP Theme Variables
```css
/* BAD: Hardcoded values */
color: #333333;
font-family: Arial;

/* GOOD: SAP theme variables */
color: var(--sapTextColor, #333);
font-family: var(--sapFontFamily, Arial);
```

#### B002: Null Data Checks
```javascript
// BAD: Direct access
const data = this.myDataBinding.data;

// GOOD: Null check
const binding = this.dataBindings?.getDataBinding("myDataBinding");
if (!binding || !binding.data) return;
const data = binding.data;
```

## Implementation Instructions

When this command is invoked:

1. Read the specified file(s)
2. For JavaScript files:
   - Parse AST if possible, otherwise use regex patterns
   - Check for performance anti-patterns
   - Check for security issues
   - Verify SAC integration patterns
3. For JSON files:
   - Validate against best practices
   - Check for security configurations
4. Aggregate findings by category and severity
5. Calculate overall score (start at 100, deduct for issues)
6. Present findings in priority order
7. If `--fix-suggestions`, include complete code fixes
