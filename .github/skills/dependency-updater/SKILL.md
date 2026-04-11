---
name: dependency-updater
description: Audits package.json, requirements.txt, or go.mod for outdated or vulnerable packages and proposes safe upgrades. Invoke when asked to update dependencies, audit packages, check for vulnerabilities, or upgrade libraries in a project.
---

# Dependency Updater

Audits project dependency manifests for outdated versions and known vulnerabilities, then proposes safe, incremental upgrades with risk assessments and migration notes.

## When to Use

- User asks to "update dependencies", "upgrade packages", or "audit vulnerabilities"
- Dependabot or Renovate alerts are pending review
- Security advisories reference packages in the project
- A new major version of a key dependency has been released
- The project hasn't had a dependency update in >3 months
- CI is failing due to peer dependency conflicts

## Process

1. **Identify the package ecosystem** from manifest files:
   - `package.json` / `package-lock.json` / `yarn.lock` → npm/Yarn (Node.js)
   - `requirements.txt` / `Pipfile` / `pyproject.toml` / `poetry.lock` → pip/Poetry (Python)
   - `go.mod` / `go.sum` → Go modules
   - `Gemfile` / `Gemfile.lock` → Bundler (Ruby)
   - `pom.xml` / `build.gradle` → Maven/Gradle (Java)
   - `Cargo.toml` / `Cargo.lock` → Cargo (Rust)

2. **Inventory current versions** from the lockfile or manifest.

3. **Check for vulnerabilities** using advisory databases:
   - npm: GitHub Advisory Database, npm audit
   - Python: PyPI Advisory Database, pip-audit
   - Go: govulncheck, https://pkg.go.dev/vuln
   - Prioritize CVEs with CVSS score ≥ 7.0 (High/Critical)

4. **Identify outdated packages**:
   - Classify each update as **patch** (1.0.0 → 1.0.1), **minor** (1.0.0 → 1.1.0), or **major** (1.0.0 → 2.0.0)
   - Patch: generally safe, apply immediately
   - Minor: check changelog for deprecations; usually safe
   - Major: review migration guide; potential breaking changes

5. **For each proposed upgrade, provide**:
   - Current version → proposed version
   - Reason (security fix / feature / patch)
   - Risk level (Low / Medium / High)
   - Breaking changes or migration notes if major
   - Links to CHANGELOG or release notes

6. **Group recommendations**:
   - 🔴 **Urgent**: known CVE, CVSS ≥ 7
   - 🟡 **Recommended**: patch/minor updates, no breaking changes
   - 🟢 **Optional**: major upgrades, evaluate when time permits

7. **Generate the updated manifest diff** showing the exact version strings to change.

8. **Note any peer dependency conflicts** that would arise from the proposed changes and suggest resolution order.

## Output Format

```
## Dependency Audit Report

**Manifest:** `package.json`
**Total packages:** 48 direct, 312 transitive
**Vulnerable:** 3 · **Outdated:** 12

---

### 🔴 Urgent — Security Vulnerabilities

| Package | Current | Fix Version | CVE | Severity |
|---------|---------|-------------|-----|----------|
| `lodash` | 4.17.20 | 4.17.21 | CVE-2021-23337 | High (7.2) |
| `axios` | 0.21.1 | 0.21.4 | CVE-2021-3749 | High (7.5) |

**lodash 4.17.21** — Patch: fixes command injection via `_.template`.
No API changes. Safe to apply immediately.

---

### 🟡 Recommended — Patch/Minor Updates

| Package | Current | Latest | Type |
|---------|---------|--------|------|
| `express` | 4.18.1 | 4.18.3 | patch |
| `typescript` | 5.0.4 | 5.4.5 | minor |

---

### Proposed `package.json` Changes
```diff
-  "lodash": "^4.17.20",
+  "lodash": "^4.17.21",
-  "axios": "^0.21.1",
+  "axios": "^0.21.4",
```

### Next Steps
1. Apply urgent security patches first: `npm update lodash axios`
2. Run test suite to confirm no regressions
3. Review TypeScript 5.4 release notes for minor changes before upgrading
```

## Examples

### Example Input
```
requirements.txt:
Django==3.2.0
requests==2.25.1
Pillow==8.1.0
```

### Example Output
```
## Dependency Audit

### 🔴 Urgent
- **Pillow 8.1.0** → **10.3.0** — Multiple CVEs including heap buffer overflow
  (CVE-2021-25287, CVE-2021-34552). Upgrade immediately.

### 🟡 Recommended
- **Django 3.2.0** → **3.2.25** — LTS patch series; security backports included.
- **requests 2.25.1** → **2.31.0** — Minor: fixes several edge cases with redirects.

### Updated requirements.txt
Django==3.2.25
requests==2.31.0
Pillow==10.3.0
```

## Boundaries

- Do NOT apply upgrades automatically without listing them and explaining the risk.
- Do NOT upgrade across major versions without noting breaking changes from the CHANGELOG.
- Do NOT recommend pre-release or RC versions unless the user explicitly requests them.
- Do NOT modify lockfiles directly — propose manifest changes and let the package manager regenerate the lockfile.
- Flag if a vulnerable package is a transitive dependency (not directly in the manifest) and note that a direct dependency must be updated to pull in the fix.
- Do NOT remove dependencies — only flag them as potentially unused; removal requires manual verification.
- If no manifest file is provided, ask the user to share one before proceeding.
