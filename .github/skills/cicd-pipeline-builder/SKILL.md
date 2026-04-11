---
name: cicd-pipeline-builder
description: Generates GitHub Actions, GitLab CI, or CircleCI pipeline configs tailored to the detected language and framework. Invoke when asked to create a CI/CD pipeline, set up automated testing, configure deployment workflows, or build GitHub Actions workflows.
---

# CI/CD Pipeline Builder

Generates complete, production-ready CI/CD pipeline configurations for GitHub Actions, GitLab CI, or CircleCI — tailored to the detected language, framework, and deployment target.

## When to Use

- User asks to "set up CI/CD", "create a GitHub Actions workflow", or "automate deployments"
- A new repository has no pipeline configuration
- Tests are being run manually and need to be automated
- User wants to add deployment stages (staging, production)
- Existing pipeline needs optimization (parallelism, caching, conditional steps)
- User asks to add specific jobs: linting, security scanning, Docker builds, releases

## Process

1. **Identify the target CI/CD platform**:
   - Default to GitHub Actions (`.github/workflows/`) if not specified
   - GitLab CI → `.gitlab-ci.yml`
   - CircleCI → `.circleci/config.yml`

2. **Detect the language, runtime, and framework**:
   - Check for `package.json`, `requirements.txt`, `go.mod`, `Gemfile`, `pom.xml`, `Cargo.toml`
   - Note test runner (Jest, pytest, go test, RSpec, JUnit)
   - Note build tool (npm, Vite, webpack, Maven, Gradle)
   - Check for Docker files, Kubernetes manifests, or cloud config (AWS, GCP, Azure)

3. **Design the pipeline stages**:
   - **CI (on every push/PR)**:
     1. Checkout
     2. Set up language runtime (cache dependencies)
     3. Install dependencies (with cache key based on lockfile hash)
     4. Lint / format check
     5. Run unit tests (with coverage report)
     6. Run integration tests (if applicable)
     7. Security scan (dependency audit)
     8. Build artifact (if applicable)
   - **CD (on merge to main/release tags)**:
     9. Build Docker image (multi-platform if needed)
     10. Push to container registry
     11. Deploy to staging
     12. Run smoke tests
     13. Deploy to production (with manual approval gate for production)

4. **Apply performance best practices**:
   - Cache `node_modules`, pip packages, Go module cache, Maven `.m2`
   - Parallelize independent jobs (lint, test, security scan)
   - Use matrix builds for multi-version testing
   - Fail fast on lint before running expensive tests

5. **Add security hardening**:
   - Pin action versions to full SHA (not mutable tags like `@v3`)
   - Use `GITHUB_TOKEN` with minimal required permissions
   - Store secrets in platform secret store (never hardcode)
   - Use OIDC for cloud provider authentication instead of long-lived keys

6. **Add status badges** and PR summary comments for test results.

7. **Generate the YAML** with inline comments explaining non-obvious choices.

## Output Format

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
      - uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8 # v4.0.2
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: ['18', '20', '22']
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
      - uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8 # v4.0.2
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@e28ff129e5465c2c0dcc6f003fc735cb6ae0c673 # v4.5.0
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Examples

### Example Input
```
Create a GitHub Actions CI pipeline for a Python FastAPI project.
Run tests with pytest. Lint with ruff. Python 3.11 and 3.12.
Deploy to AWS Lambda on push to main using SAM CLI.
```

### Example Output (structure)
```
.github/workflows/ci.yml
  Jobs:
    lint:      runs ruff check . on ubuntu-latest
    test:      matrix: [3.11, 3.12], runs pytest --cov, uploads to Codecov
    security:  runs pip-audit for dependency vulnerabilities
    deploy:    runs on main push only, uses aws-actions/configure-aws-credentials
               with OIDC (no stored keys), runs sam build && sam deploy
               requires "production" environment approval gate
```

## Boundaries

- Do NOT store secrets in workflow YAML — always reference `${{ secrets.SECRET_NAME }}`.
- Do NOT use mutable action tags (`@v3`, `@main`) in final output — pin to commit SHAs with version comment.
- Do NOT generate deployment configs without noting that environment secrets (AWS keys, registry credentials) must be configured in the platform's secret store.
- Do NOT generate pipeline configs for platforms not explicitly supported without noting the limitation.
- If the repository structure is unclear, make reasonable assumptions and note them as comments in the YAML.
- Do NOT add deployment stages unless the user requests them or provides deployment context.
- Generated workflows should be valid YAML — verify indentation and syntax before outputting.
