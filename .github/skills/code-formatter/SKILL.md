---
name: code-formatter
description: Applies language-specific formatting (Prettier, Black, gofmt, rustfmt) and enforces consistent linting rules across a codebase. Invoke when asked to format code, fix linting errors, set up Prettier or Black, configure ESLint, enforce consistent code style, or add pre-commit formatting hooks.
---

# Code Formatter

Configures and applies language-specific formatters and linters to establish consistent code style across a codebase — generating configuration files, fixing violations, and setting up pre-commit hooks and CI checks to enforce formatting automatically.

## When to Use

- User asks to "format this code", "fix linting errors", or "set up Prettier"
- A new project needs formatter/linter configuration
- CI is failing due to formatting violations
- The team wants to enforce consistent code style in PRs
- Existing linting config needs to be updated or extended
- User asks to add pre-commit hooks for automatic formatting

## Process

1. **Detect the language(s) and existing tooling**:
   - JavaScript/TypeScript: Prettier, ESLint (with `@typescript-eslint`, `eslint-plugin-react`, etc.)
   - Python: Black (formatter), Ruff (linter + formatter), isort, mypy, flake8
   - Go: `gofmt` (built-in), `goimports`, `golangci-lint`
   - Rust: `rustfmt`, `clippy`
   - Java: google-java-format, Checkstyle, Spotless
   - Ruby: RuboCop, StandardRB
   - Check for existing config files: `.eslintrc.*`, `prettier.config.*`, `pyproject.toml`, `.rubocop.yml`

2. **Generate formatter configuration**:

   **Prettier** (`.prettierrc` or `prettier.config.js`):
   - `printWidth`: 100 (adjust to team preference)
   - `tabWidth`: 2 for JS/TS, 4 for Python conventions
   - `singleQuote`: true/false based on existing codebase
   - `trailingComma`: "all" (ES5+ friendly)
   - `semi`: true/false
   - `endOfLine`: "lf"
   - Add `overrides` for specific file types (JSON, YAML, markdown)

   **ESLint** (`eslint.config.js` or `.eslintrc.json`):
   - Extend from `eslint:recommended`, `@typescript-eslint/recommended`
   - Add framework-specific plugins (React, Vue, import ordering)
   - Configure rules based on existing codebase conventions
   - Add `no-console` (warn in dev, error in prod)
   - Set `no-unused-vars` to error
   - Add `import/order` for consistent import ordering

   **Black + Ruff** (`pyproject.toml`):
   - `line-length = 100`
   - `target-version = ["py311"]`
   - Ruff rules: `E`, `F`, `I` (isort), `N` (naming), `UP` (pyupgrade), `B` (bugbear)
   - Exclude: `migrations/`, `__pycache__/`, `.venv/`

3. **Generate `.prettierignore` / `.eslintignore`**:
   - Exclude: `dist/`, `build/`, `node_modules/`, `coverage/`, auto-generated files, vendored code

4. **Add formatter scripts to `package.json`** or `Makefile`:
   - `format`: run formatter to fix all files
   - `format:check`: check without modifying (for CI)
   - `lint`: run linter, exit non-zero on violations
   - `lint:fix`: run linter with auto-fix

5. **Set up pre-commit hooks** (`.pre-commit-config.yaml` or `lint-staged` + Husky):
   - Run formatter and linter only on staged files (fast)
   - Block commit if violations remain after auto-fix

6. **Set up CI check**:
   - Add a `lint` job to the CI pipeline that runs format check and linting
   - This ensures formatting is enforced on all PRs

7. **Fix existing violations** if asked:
   - Run the formatter on the provided code and show the corrected output
   - Explain non-trivial lint rule violations (not just formatting)

## Output Format

### `.prettierrc`
```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "singleQuote": true,
  "trailingComma": "all",
  "semi": true,
  "endOfLine": "lf",
  "arrowParens": "always",
  "overrides": [
    { "files": "*.json", "options": { "printWidth": 80 } },
    { "files": "*.md", "options": { "proseWrap": "always" } }
  ]
}
```

### `eslint.config.js` (ESLint v9 flat config)
```js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'off',
      'prefer-const': 'error',
    },
  },
  { ignores: ['dist/', 'build/', 'node_modules/'] }
);
```

### `pyproject.toml` (Ruff + Black)
```toml
[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]  # line length handled by Black
exclude = ["migrations/", ".venv/"]
```

## Examples

### Example Input
```javascript
const x=1
const foo = function(a,b,c){
return a+b+c}

var unused = "hello"
```

### Example Output (Prettier + ESLint applied)
```javascript
// After Prettier formatting:
const x = 1;
const foo = function (a, b, c) {
  return a + b + c;
};

// ESLint violations (after formatting):
// Line 5: 'unused' is assigned a value but never used. (@typescript-eslint/no-unused-vars)
// Line 1: Prefer 'const' over 'let'. (prefer-const) ✓ already const
// Line 2: Prefer arrow function expression. (prefer-arrow-callback) — optional rule
```

## Boundaries

- Do NOT apply formatting to auto-generated files (migrations, protobuf output, OpenAPI generated clients).
- Do NOT change linting rules that would cause existing passing CI to fail without flagging the breaking change.
- Do NOT apply `eslint --fix` to logic-changing rules (like `eqeqeq` changing `==` to `===`) without reviewing each case.
- When configuring ESLint, do NOT disable security-relevant rules (`no-eval`, `no-implied-eval`, etc.).
- Do NOT generate formatter configs that conflict with each other (e.g., Prettier and ESLint formatting rules overlapping — use `eslint-config-prettier` to disable conflicting ESLint formatting rules).
- If multiple languages are used in the repo, generate separate formatter configs per language — do not try to handle all with one tool.
