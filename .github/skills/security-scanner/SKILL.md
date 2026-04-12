---
name: security-scanner
description: Detects common vulnerability patterns (XSS, SQL injection, path traversal, IDOR) in source code and suggests mitigations. Invoke when asked to security review code, find vulnerabilities, check for injection risks, audit authentication, or assess OWASP compliance.
---

# Security Scanner

Performs static analysis of source code to identify common security vulnerabilities including injection flaws, broken authentication, insecure data handling, and OWASP Top 10 issues — with concrete mitigation recommendations.

## When to Use

- User asks for a "security review" or "vulnerability scan"
- Code handles user input, authentication, file uploads, or external data
- A security audit is required before deployment
- User asks about OWASP compliance or CVE mitigation
- New endpoints are added that accept untrusted input
- Code accesses the filesystem, executes commands, or makes outbound requests based on user data

## Process

1. **Triage the attack surface** — identify all points where untrusted input enters the system:
   - HTTP request params, headers, cookies, bodies
   - File uploads
   - Environment variables or config files that might be user-controlled
   - Data fetched from external APIs or databases
   - Inter-process communication (IPC, message queues)

2. **Scan for each vulnerability class** using the following checklist:

   **A01 — Injection**
   - SQL: string concatenation into queries → require parameterized queries / prepared statements
   - Command injection: user input in `exec()`, `system()`, `subprocess.call()` shell=True
   - LDAP/XPath/NoSQL injection: unescaped user input in query objects
   - Template injection: user-controlled strings rendered by template engines

   **A02 — Broken Authentication**
   - Hardcoded credentials, tokens, or API keys in source
   - Weak password hashing (MD5, SHA-1, unsalted) → require bcrypt/argon2
   - JWT: `alg: none` acceptance, weak secrets, missing expiry validation
   - Session tokens not invalidated on logout

   **A03 — XSS (Cross-Site Scripting)**
   - User input rendered into HTML without escaping
   - `innerHTML`, `document.write`, `eval()` with dynamic content
   - `dangerouslySetInnerHTML` in React without sanitization
   - Missing Content-Security-Policy header

   **A04 — Insecure Design / IDOR**
   - Object IDs fetched without ownership verification (e.g., `GET /orders/:id` without checking `order.userId === req.user.id`)
   - Predictable resource identifiers (sequential integers) for sensitive resources

   **A05 — Security Misconfiguration**
   - Verbose error messages exposing stack traces to clients
   - Debug mode enabled in production
   - CORS configured with `*` for authenticated routes
   - Missing security headers (HSTS, X-Frame-Options, X-Content-Type-Options)

   **A06 — Path Traversal / File Inclusion**
   - User-controlled paths used in `fs.readFile()`, `open()`, or includes
   - No canonicalization or allowlist check before file access

   **A07 — Cryptographic Failures**
   - Sensitive data (PII, passwords, tokens) stored or transmitted in plaintext
   - Weak algorithms: DES, RC4, MD5 for security purposes
   - Insufficient entropy in token generation (`Math.random()` for secrets)

   **A08 — Supply Chain / Prototype Pollution**
   - `merge()`, `extend()`, or `_.assign()` with untrusted objects in JavaScript
   - Unverified package installs or missing lockfiles

3. **Rate each finding** by severity:
   - 🔴 Critical: immediate exploitability, data loss/RCE risk
   - 🟠 High: exploitable with moderate effort
   - 🟡 Medium: requires specific conditions or chaining
   - 🟢 Low/Info: defense-in-depth improvements

4. **Provide concrete mitigations** with code snippets for each finding.

5. **Summarize the overall security posture** and list top 3 priority fixes.

## Output Format

```
## Security Scan Report

**Files analyzed:** 8
**Findings:** 🔴 1 Critical · 🟠 2 High · 🟡 3 Medium · 🟢 2 Low

---

### 🔴 Critical — SQL Injection
**File:** `src/db/queries.js:34`
**CWE:** CWE-89

```js
// ❌ Vulnerable
const sql = `SELECT * FROM users WHERE username = '${req.body.username}'`;
```

**Mitigation:**
```js
// ✅ Use parameterized query
const sql = 'SELECT * FROM users WHERE username = ?';
db.query(sql, [req.body.username]);
```

---

### 🟠 High — Missing Authorization Check (IDOR)
**File:** `src/routes/documents.js:67`

`GET /documents/:id` fetches the document by ID without verifying
the authenticated user owns it.

**Mitigation:**
```js
const doc = await Document.findById(req.params.id);
if (!doc || doc.ownerId !== req.user.id) {
  return res.status(404).json({ error: 'Not found' });
}
```
```

## Examples

### Example Input
```python
@app.route('/files')
def get_file():
    filename = request.args.get('name')
    with open(f'/var/app/uploads/{filename}') as f:
        return f.read()
```

### Example Output
```
🔴 Critical — Path Traversal (CWE-22)
An attacker can pass `name=../../etc/passwd` to read arbitrary files.

Mitigation:
```python
import os

UPLOAD_DIR = '/var/app/uploads'

@app.route('/files')
def get_file():
    filename = request.args.get('name', '')
    # Resolve and validate the path stays within UPLOAD_DIR
    safe_path = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
    if not safe_path.startswith(UPLOAD_DIR + os.sep):
        abort(400, 'Invalid filename')
    with open(safe_path) as f:
        return f.read()
```
```

## Boundaries

- Do NOT attempt to exploit vulnerabilities — analysis is static and advisory only.
- Do NOT flag false positives as confirmed vulnerabilities — use hedged language ("may be vulnerable", "appears to lack") when confidence is lower.
- Do NOT scan minified or transpiled output — request source files.
- Do NOT report findings in third-party library internals unless the library itself is known-vulnerable (check CVE databases separately).
- Do NOT recommend security-through-obscurity as a mitigation (renaming endpoints, hiding error codes, etc.).
- If code is incomplete (functions without implementations), note that the scan is partial and may miss issues in missing code.
- Always recommend defense-in-depth — even if one layer is secure, suggest additional controls where appropriate.
