---
name: docker-composer
description: Creates and validates Dockerfile and docker-compose.yml files optimized for the detected stack, including multi-stage builds. Invoke when asked to dockerize an application, create a Dockerfile, set up docker-compose, containerize a service, or optimize an existing Docker setup.
---

# Docker Composer

Creates optimized, production-ready Dockerfiles and docker-compose configurations for detected application stacks, including multi-stage builds for minimal image sizes, proper layer caching, health checks, and security hardening.

## When to Use

- User asks to "dockerize this app", "create a Dockerfile", or "set up docker-compose"
- An existing Dockerfile is inefficient (large image, slow builds, running as root)
- A multi-service application needs a docker-compose setup for local development
- User wants to add a Docker setup for CI or deployment
- User asks for multi-stage builds to separate build and runtime environments
- Container image size or build time needs to be reduced

## Process

1. **Detect the application stack**:
   - Check for `package.json` (Node.js), `requirements.txt`/`pyproject.toml` (Python), `go.mod` (Go), `pom.xml`/`build.gradle` (Java), `Gemfile` (Ruby), `Cargo.toml` (Rust)
   - Note the framework (Express, FastAPI, Spring Boot, etc.)
   - Identify if it's a static site, API server, worker process, or full-stack app

2. **Choose the right base image**:
   - Prefer official slim/alpine variants: `node:20-slim`, `python:3.12-slim`, `golang:1.22-alpine`
   - For final runtime stages, use distroless where possible (`gcr.io/distroless/nodejs20-debian12`)
   - Pin to a specific digest or version tag — never use `latest`
   - Note the trade-offs (alpine uses musl vs. glibc which can affect native modules)

3. **Design the multi-stage build**:
   - **Stage 1 (deps/builder)**: install all dependencies, run build tools
   - **Stage 2 (runtime)**: copy only the compiled artifacts and runtime dependencies
   - This keeps the final image free of build tools, source code, and dev dependencies

4. **Apply layer caching optimization**:
   - Copy dependency manifests (`package.json`, `requirements.txt`) BEFORE source code
   - Run dependency install BEFORE copying application source
   - This ensures the expensive install step is cached unless dependencies change

5. **Security hardening**:
   - Create and use a non-root user (UID 1000): `RUN adduser --system appuser && USER appuser`
   - Set `WORKDIR` explicitly
   - Use `COPY --chown=appuser:appuser` to set ownership
   - Avoid `sudo`, `apt-get upgrade`, or installing unnecessary packages
   - Set `--no-cache` for `apk add` / `--no-install-recommends` for `apt-get`
   - Expose only necessary ports

6. **Add health check**: `HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:${PORT}/health || exit 1`

7. **For docker-compose**:
   - Define services, networks, and named volumes
   - Map ports and environment variables
   - Set `depends_on` with `condition: service_healthy` for database readiness
   - Include development overrides (`docker-compose.override.yml`) for hot reload

8. **Generate a `.dockerignore`** to exclude `node_modules`, `.git`, test files, and local config.

## Output Format

```dockerfile
# Dockerfile
# ── Stage 1: Dependencies ──────────────────────────────────────────────────────
FROM node:20-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# ── Stage 2: Builder ──────────────────────────────────────────────────────────
FROM node:20-slim AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# ── Stage 3: Runtime ──────────────────────────────────────────────────────────
FROM node:20-slim AS runtime
ENV NODE_ENV=production PORT=3000
WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --chown=appuser:appgroup package.json ./

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

## Examples

### Example Input
```
Dockerize a FastAPI Python app. It needs PostgreSQL and Redis.
Dev setup with hot reload. Production build should be minimal.
```

### Example Output (summary)
```
Files generated:
  Dockerfile           — multi-stage: python:3.12-slim builder → distroless runtime
  docker-compose.yml   — services: app, postgres:16, redis:7-alpine
                          volumes: postgres_data, redis_data
                          networks: backend (internal), frontend (exposed)
  docker-compose.override.yml — mounts ./src as volume, runs uvicorn --reload
  .dockerignore        — excludes __pycache__, .venv, .git, tests/, *.pyc

docker-compose.yml services:
  app:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      postgres: { condition: service_healthy }
      redis: { condition: service_healthy }
  postgres:
    image: postgres:16-alpine
    healthcheck: pg_isready
    volumes: [postgres_data:/var/lib/postgresql/data]
  redis:
    image: redis:7-alpine
    healthcheck: redis-cli ping
```

## Boundaries

- Do NOT include secrets, passwords, or API keys in Dockerfiles or docker-compose.yml — always use environment variables and `.env` files (which should be in `.gitignore`).
- Do NOT use `latest` tag for base images in production Dockerfiles — always pin versions.
- Do NOT run container processes as `root` unless absolutely necessary (and flag it clearly if required).
- Do NOT use `ADD` with remote URLs — use `COPY` for local files and `curl`/`wget` in a `RUN` step.
- Warn if the application has native module dependencies that may be incompatible with Alpine's musl libc.
- Do NOT generate Kubernetes manifests from this skill — recommend the `api-scaffolder` or dedicated K8s tooling.
- Always generate a `.dockerignore` alongside the Dockerfile.
