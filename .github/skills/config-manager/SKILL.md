---
name: config-manager
description: Manages environment variables, secrets, and feature flags — generates .env templates, validates required keys, and flags hardcoded secrets. Invoke when asked to manage configuration, audit for hardcoded secrets, generate .env templates, validate environment variables, or set up feature flags.
---

# Config Manager

Audits and improves configuration management — detects hardcoded secrets, generates `.env` templates with documentation, validates all required environment variables on startup, and optionally sets up feature flag patterns for progressive rollout.

## When to Use

- User asks to "manage configuration", "audit for hardcoded secrets", or "set up env vars"
- A code review flagged hardcoded credentials or connection strings
- A new deployment environment needs its configuration documented
- The application crashes on missing config with unhelpful errors
- User wants to implement feature flags for progressive feature rollout
- Secrets have been accidentally committed and need to be cleaned up

## Process

1. **Scan for hardcoded secrets and configuration**:
   - Search for patterns matching:
     - API keys: `sk-`, `pk-`, `AKIA` (AWS), `ghp_`, `glpat-`
     - Connection strings: `postgres://`, `mongodb+srv://`, `redis://` with credentials
     - JWT secrets: `secret: "..."`, `jwtSecret =`
     - Passwords: `password = "..."`, `db_pass =`
     - Tokens: long hex/base64 strings assigned to variables named `*token*`, `*key*`, `*secret*`
   - Flag file:line for each finding with severity (Critical if committed to git history)

2. **Inventory all configuration the application reads**:
   - Search for `process.env.*`, `os.environ[*]`, `os.getenv(*)`, `viper.Get*`, `config.*`
   - Collect all variable names, their usage context, and whether they have defaults
   - Classify: required (no default, app won't function), optional (has default), feature flag (boolean)

3. **Generate `.env.example`** (a template — never the actual `.env`):
   - List every discovered variable
   - Add a descriptive comment for each explaining what it's for, acceptable values, and format
   - Provide safe placeholder values (not real secrets)
   - Group variables by concern (database, auth, external services, features, etc.)
   - Mark required variables clearly with a comment: `# REQUIRED`

4. **Generate a config validation module** that runs at startup:
   - Read all required variables
   - Validate format where applicable (URL format, integer range, enum values)
   - Fail fast on startup with a clear error message listing every missing/invalid variable
   - Never crash mid-request due to missing config

5. **Generate feature flag patterns** if requested:
   - Simple env-based flags: `FEATURE_NEW_DASHBOARD=true`
   - Percentage rollout: `FEATURE_ROLLOUT_PERCENTAGE=20`
   - Per-user targeting: integrate with LaunchDarkly, Unleash, or Flagsmith
   - Provide a `isFeatureEnabled(flag, userId?)` utility function

6. **Provide git remediation guidance** if secrets are found in git history:
   - Advise rotating the exposed secret immediately
   - Provide BFG Repo-Cleaner or `git filter-repo` commands to purge from history
   - Note that force-push is required and all collaborators must re-clone

## Output Format

### Secret Scan Results
```
## Configuration Audit

### 🔴 Hardcoded Secrets Found

| File | Line | Type | Action Required |
|------|------|------|----------------|
| src/db/connection.ts | 12 | PostgreSQL connection string with password | Rotate & move to env var |
| config/auth.js | 34 | JWT secret (hardcoded string) | Rotate & move to env var |

**Immediate action:** These may be in git history. Rotate both secrets NOW, then
remove from source using `git filter-repo`.
```

### `.env.example`
```bash
# =============================================================================
# Database Configuration
# =============================================================================
# REQUIRED — PostgreSQL connection string
# Format: postgresql://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_URL=postgresql://app:changeme@localhost:5432/myapp_dev

# =============================================================================
# Authentication
# =============================================================================
# REQUIRED — JWT signing secret (min 32 chars)
# Generate: openssl rand -hex 32
JWT_SECRET=replace_with_a_secure_random_value_at_least_32_chars

# =============================================================================
# Feature Flags
# =============================================================================
# Optional — Enable new dashboard UI (default: false)
FEATURE_NEW_DASHBOARD=false
```

### Config Validation Module (TypeScript)
```ts
// src/config/index.ts
import { z } from 'zod';

const ConfigSchema = z.object({
  DATABASE_URL: z.string().url('DATABASE_URL must be a valid URL'),
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  FEATURE_NEW_DASHBOARD: z.enum(['true', 'false']).transform(v => v === 'true').default('false'),
});

const result = ConfigSchema.safeParse(process.env);
if (!result.success) {
  console.error('❌ Invalid configuration:\n', result.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = result.data;
```

## Examples

### Example Input
```python
# config.py
DATABASE_URL = "postgresql://admin:SuperSecret123@prod.db.example.com/mydb"
API_KEY = "sk-live-abc123xyz"
DEBUG = True
```

### Example Output
```
🔴 Critical: 2 hardcoded secrets found.

1. DATABASE_URL contains credentials (line 2) — rotate database password immediately
2. API_KEY contains a live API key (line 3) — revoke and regenerate

Recommended refactor:
```python
# config.py
import os

DATABASE_URL = os.environ["DATABASE_URL"]  # required
API_KEY = os.environ["API_KEY"]            # required
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"  # optional, default false
```

Add to .env.example:
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev
API_KEY=your_api_key_here
DEBUG=false
```

## Boundaries

- Do NOT create or populate `.env` files — only `.env.example` with placeholder values.
- Do NOT display discovered secret values in output — mask after the first 4 characters (e.g., `sk-li...`).
- Do NOT attempt to rotate secrets — only advise that rotation is required and provide instructions.
- Do NOT recommend committing secrets to the repository in any form, including "encrypted in the repo".
- If secrets are found in git history, note that deleting the file is insufficient — history must be rewritten.
- Always recommend using a secrets manager (AWS Secrets Manager, Vault, GCP Secret Manager) for production rather than plain environment variables for highly sensitive values.
