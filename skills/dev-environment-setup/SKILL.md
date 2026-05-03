---
name: dev-environment-setup
description: Bootstraps development environments with .env templates, Makefile targets, editor configs, and local dependency instructions. Invoke when setting up a new project, onboarding to a repository, configuring local dev tooling, or creating developer documentation for getting started.
---

# Dev Environment Setup

Bootstraps a consistent, well-documented local development environment by generating `.env` templates, `Makefile` targets, editor configuration files, pre-commit hooks, and getting-started documentation tailored to the detected project stack.

## When to Use

- A new repository needs a developer onboarding setup
- Existing repo has no `.env.example`, `Makefile`, or setup scripts
- New team members struggle to run the project locally
- User asks for a "developer setup", "local environment config", or "onboarding guide"
- Project uses multiple services and needs a coordinated local startup sequence
- Editor configs need to be standardized across the team

## Process

1. **Detect the project stack**:
   - Language runtime(s) and version managers (nvm, pyenv, rbenv, asdf, rtx/mise)
   - Package manager (npm, yarn, pnpm, pip, poetry, cargo, go mod)
   - Database(s) needed locally (PostgreSQL, MySQL, SQLite, Redis, MongoDB)
   - Other services (message queues, object storage, search engines)
   - Existing tooling: Docker, docker-compose, devcontainers

2. **Generate `.env.example`** (never `.env`):
   - List all environment variables the application reads
   - Include descriptions as comments for each variable
   - Provide safe example/placeholder values (not real secrets)
   - Group related variables with section comments
   - Flag required vs. optional variables

3. **Generate a `Makefile`** with common developer targets:
   - `make setup` — full first-time setup (install deps, create .env, run migrations)
   - `make dev` — start the development server with hot reload
   - `make test` — run test suite
   - `make lint` — run linter and formatter checks
   - `make build` — production build
   - `make clean` — remove generated artifacts
   - `make db-migrate` / `make db-reset` — database operations
   - `make help` — auto-generated help text from target comments

4. **Generate editor configuration files**:
   - `.editorconfig` — indent style, line endings, trailing whitespace, charset
   - `.vscode/settings.json` — format on save, default formatter, file associations
   - `.vscode/extensions.json` — recommended extensions for the stack
   - `.vscode/launch.json` — debugger configuration

5. **Generate `.tool-versions`** (asdf) or `.nvmrc` / `.python-version` for runtime pinning.

6. **Generate `.pre-commit-config.yaml`** if pre-commit is appropriate:
   - Language-specific linters and formatters
   - Commit message validation
   - Secret scanning (detect-secrets, gitleaks)

7. **Write or update `CONTRIBUTING.md`** with:
   - Prerequisites (runtime versions, tools to install)
   - Step-by-step first-time setup
   - How to run tests
   - How to contribute (branch naming, PR process)
   - Troubleshooting section for common setup issues

## Output Format

### `.env.example`
```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# Database — use docker-compose to start locally: make db-up
DATABASE_URL=postgresql://app:password@localhost:5432/myapp_dev

# Redis — required for session storage and job queues
REDIS_URL=redis://localhost:6379

# Authentication — generate with: openssl rand -hex 32
JWT_SECRET=replace_with_random_secret_do_not_use_in_production
JWT_EXPIRES_IN=7d

# External Services (optional in dev — feature flags will disable if unset)
SENDGRID_API_KEY=
STRIPE_SECRET_KEY=
```

### `Makefile`
```makefile
.PHONY: help setup dev test lint build clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## First-time project setup
	@cp -n .env.example .env || true
	npm ci
	npm run db:migrate

dev: ## Start development server with hot reload
	npm run dev

test: ## Run test suite
	npm test

lint: ## Lint and format check
	npm run lint
```

## Examples

### Example Input
```
Python FastAPI project. Uses PostgreSQL and Redis.
Team uses VS Code. Need a clean setup for new contributors.
```

### Example Output (files generated)
```
.env.example              — DATABASE_URL, REDIS_URL, SECRET_KEY, DEBUG, PORT
Makefile                  — setup, dev, test, lint, build, db-migrate, db-reset, help
.editorconfig             — 4-space Python indent, LF line endings, UTF-8
.vscode/settings.json     — Python interpreter, Black formatter, autoformat on save
.vscode/extensions.json   — ms-python.python, ms-python.black-formatter, mtxr.sqltools
.vscode/launch.json       — uvicorn debug config on port 8000
.python-version           — 3.12.3
.pre-commit-config.yaml   — ruff, black, mypy, detect-secrets
CONTRIBUTING.md           — pyenv setup, poetry install, make setup instructions
```

## Boundaries

- Do NOT create or populate `.env` files — only `.env.example` with placeholder values.
- Do NOT hardcode real API keys, passwords, or connection strings in any generated file.
- Do NOT generate setup scripts that require root/sudo without clearly flagging the requirement.
- Do NOT assume Docker is available if not detected — provide both Docker and non-Docker setup paths.
- Keep `Makefile` targets portable (POSIX sh, avoid Bash-only features unless the team uses Linux/macOS exclusively).
- If the project already has `.env.example` or a `Makefile`, propose additions/modifications rather than overwriting.
- Do NOT generate IDE configs for editors not used by the team unless asked.
