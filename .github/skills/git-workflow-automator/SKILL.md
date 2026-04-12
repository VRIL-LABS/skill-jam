---
name: git-workflow-automator
description: Automates branching strategies, commit message conventions, changelog generation, and semantic versioning tags. Invoke when asked to set up a git workflow, configure commit conventions, generate a changelog, create a release, implement semantic versioning, or automate the release process.
---

# Git Workflow Automator

Establishes and automates git workflows — branching strategies, commit message conventions (Conventional Commits), automated changelog generation, semantic versioning, and release tagging — using GitHub Actions, standard tooling, and configuration files.

## When to Use

- User asks to "set up a git workflow", "configure commit conventions", or "automate releases"
- The team has inconsistent commit messages and changelogs are manual
- User wants to implement semantic versioning and automated version bumps
- User asks about Gitflow, trunk-based development, or GitHub Flow
- A CHANGELOG needs to be generated from git history
- User wants automated release notes on every tag push

## Process

1. **Choose the branching strategy** based on team/project needs:
   - **GitHub Flow** (recommended for most teams): `main` is always deployable; feature branches short-lived; deploy from PR merge. Simple, fast, CD-friendly.
   - **Gitflow**: `main` + `develop` + `feature/*` + `release/*` + `hotfix/*`. More structured, for scheduled releases or parallel maintenance.
   - **Trunk-Based Development**: all work on `main` (or very short-lived branches); feature flags for incomplete features. Best for high-velocity CI/CD.

2. **Set up Conventional Commits**:
   - Standard format: `<type>(<scope>): <description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
   - Breaking changes: append `!` after type or add `BREAKING CHANGE:` footer
   - Generate `commitlint.config.js` to enforce this in CI and via Husky hooks
   - Generate `.czrc` or `commitizen` config for interactive commit prompts

3. **Set up semantic versioning automation**:
   - **semantic-release**: fully automated versioning and publishing based on commit types
     - `fix:` → patch bump (1.0.0 → 1.0.1)
     - `feat:` → minor bump (1.0.0 → 1.1.0)
     - `feat!:` / `BREAKING CHANGE:` → major bump (1.0.0 → 2.0.0)
   - Alternatives: `release-please` (Google), `standard-version`, `changesets` (monorepos)
   - Generate the appropriate configuration file

4. **Generate CHANGELOG automation**:
   - `conventional-changelog` or `git-cliff` for CHANGELOG.md generation
   - Group entries by type (Features, Bug Fixes, Breaking Changes, etc.)
   - Link commit hashes to GitHub commit URLs

5. **Set up branch protection rules** (document, as these are configured in GitHub UI):
   - Require PR reviews before merging to `main`
   - Require status checks (CI) to pass
   - Require up-to-date branches
   - Disallow force-push to `main`
   - Require signed commits (optional)

6. **Generate GitHub Actions workflow** for release automation:
   - Trigger on push to `main` (or on tag push)
   - Run tests, then semantic-release (or release-please)
   - Create GitHub Release with generated release notes
   - Publish package to npm/PyPI if applicable

7. **Generate PR template** (`.github/pull_request_template.md`):
   - Summary of changes
   - Type of change checkboxes
   - Testing instructions
   - Checklist (tests pass, docs updated, CHANGELOG updated if manual)

## Output Format

### `commitlint.config.js`
```js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-max-length': [2, 'always', 100],
  },
};
```

### `.release-it.json` (release-it config)
```json
{
  "$schema": "https://unpkg.com/release-it/schema/release-it.json",
  "git": {
    "commitMessage": "chore: release v${version}",
    "tagName": "v${version}",
    "requireBranch": "main"
  },
  "github": {
    "release": true,
    "releaseName": "v${version}"
  },
  "plugins": {
    "@release-it/conventional-changelog": {
      "preset": "conventionalcommits",
      "infile": "CHANGELOG.md"
    }
  }
}
```

### `.github/workflows/release.yml`
```yaml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
        with:
          fetch-depth: 0  # full history needed for changelog generation

      - uses: google-github-actions/release-please-action@cc61a07e2da466bebbc19b3a7dd01d6aecb20d1e # v4.1.3
        with:
          release-type: node
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Examples

### Example Input
```
Set up conventional commits and automated releases for a Python library.
We use GitHub. Releases should publish to PyPI automatically.
```

### Example Output (files generated)
```
commitlint.config.js    — enforces conventional commit format
.husky/commit-msg       — runs commitlint on each commit locally
.github/workflows/release.yml
  — triggers release-please on push to main
  — on release PR merge: bumps pyproject.toml version, generates CHANGELOG.md
  — publishes to PyPI using trusted publisher (OIDC, no stored API key)
CHANGELOG.md            — initialized with current version
.github/pull_request_template.md — PR template with type checklist
```

**Sample commit convention for the team:**
```
feat(auth): add OAuth 2.0 login via Google
fix(api): handle empty pagination cursor correctly
docs: update README with new auth flow
feat!: remove deprecated v1 endpoints

BREAKING CHANGE: /api/v1/* routes have been removed. Migrate to /api/v2/*.
```

## Boundaries

- Do NOT force-push to protected branches or modify git history in production branches.
- Do NOT recommend Gitflow for teams practicing continuous deployment — the overhead outweighs the benefits.
- When setting up semantic-release or release-please, note that the `GITHUB_TOKEN` needs write permissions to create releases and push version bumps.
- Do NOT automatically squash all commits — preserve merge commits and the commit history structure the team prefers.
- Do NOT generate a CHANGELOG from scratch without reading the actual git log — generated content must reflect real commits.
- If `main` has no Conventional Commits history, note that automated changelog generation will only cover commits made after the convention is adopted.
