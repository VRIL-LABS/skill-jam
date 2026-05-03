---
name: auth-integrator
description: Adds authentication and authorization flows — OAuth 2.0, JWT, RBAC, API keys — to an existing application. Invoke when asked to add login, implement authentication, set up OAuth, add JWT tokens, implement role-based access control, or secure API endpoints.
---

# Auth Integrator

Designs and implements authentication (verifying identity) and authorization (controlling access) flows for existing applications — covering OAuth 2.0, JWT sessions, API key authentication, and role-based access control (RBAC).

## When to Use

- User asks to "add authentication", "implement login", or "secure these endpoints"
- An API needs API key or JWT-based authentication
- OAuth 2.0 social login (Google, GitHub, etc.) needs to be integrated
- Role-based permissions need to be enforced on routes or resources
- Existing auth implementation has security gaps
- User asks to implement refresh token rotation or session management

## Process

1. **Clarify the auth requirements**:
   - **Authentication type**: session cookies, JWT (stateless), API keys, OAuth 2.0, SAML, magic links
   - **Identity providers**: local (username/password), Google, GitHub, Microsoft, etc.
   - **Authorization model**: no authz, simple auth check, RBAC (roles), ABAC (attributes)
   - **Client type**: SPA (cookie vs. token tradeoffs), mobile, server-to-server
   - **Framework**: Express, FastAPI, Django, Spring Boot, etc.

2. **Design the authentication flow** based on the chosen type:

   **JWT (Stateless Bearer Tokens)**:
   - POST `/auth/login` → validate credentials → issue `access_token` (short-lived, 15min) + `refresh_token` (long-lived, 7–30d, stored in httpOnly cookie or DB)
   - Protected routes: middleware extracts `Authorization: Bearer <token>`, verifies signature and expiry, attaches `req.user`
   - POST `/auth/refresh` → validate refresh token → issue new access token + rotate refresh token
   - POST `/auth/logout` → invalidate refresh token (add to denylist or delete from DB)

   **OAuth 2.0 / OIDC**:
   - GET `/auth/oauth/google` → redirect to provider authorization URL with `state` and `PKCE`
   - GET `/auth/callback` → exchange `code` for tokens → fetch user profile → upsert user in DB → issue local session/JWT
   - Always verify `state` param to prevent CSRF

   **API Keys**:
   - Generate cryptographically random key (32+ bytes): `crypto.randomBytes(32).toString('hex')`
   - Store only a hashed version (SHA-256) in the database, return the plaintext once
   - Middleware: extract `X-API-Key` header → hash it → look up in DB → attach associated user/scope

3. **Design the authorization model**:
   - **RBAC**: define roles (`admin`, `editor`, `viewer`), assign permissions per role, enforce in middleware
   - **Resource ownership**: check `resource.ownerId === req.user.id` before mutations
   - Implement `requireRole(role)` and `requirePermission(permission)` middleware factories

4. **Implement secure password handling** if using local auth:
   - Hash with `bcrypt` (cost factor 12) or `argon2id`
   - Never store, log, or return plaintext passwords
   - Implement rate limiting on login endpoint (max 5 attempts / 15min per IP)

5. **Generate the implementation files**:
   - Auth router with login, register, refresh, logout endpoints
   - Auth middleware for protecting routes
   - JWT utility (sign, verify, refresh)
   - User model with auth fields
   - Role/permission definitions

6. **Add security headers and configurations**:
   - httpOnly, Secure, SameSite=Strict cookies for refresh tokens
   - Short expiry for access tokens
   - Token rotation on every refresh

## Output Format

```
### Files Generated

- `src/auth/auth.router.ts`    — POST /auth/register, /auth/login, /auth/refresh, /auth/logout
- `src/auth/auth.service.ts`   — validateCredentials, issueTokens, refreshTokens, revokeToken
- `src/auth/auth.middleware.ts`— requireAuth, requireRole(role), requirePermission(perm)
- `src/auth/jwt.util.ts`       — signAccessToken, signRefreshToken, verifyToken
- `src/models/user.model.ts`   — id, email, passwordHash, role, refreshTokens[]
```

### `src/auth/auth.middleware.ts`
```ts
import { Request, Response, NextFunction } from 'express';
import { verifyToken } from './jwt.util';

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid Authorization header' });
  }
  try {
    const payload = verifyToken(authHeader.slice(7));
    req.user = payload;
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

export function requireRole(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}
```

## Examples

### Example Input
```
Add JWT authentication to an Express.js API.
Users should be able to register with email/password.
Admin and user roles. Admins can access /admin/* routes.
```

### Example Output (summary)
```
Implementation:
- POST /auth/register — hash password (bcrypt cost 12), create user (role: 'user'), return JWT
- POST /auth/login   — verify credentials, return access token (15min) + set httpOnly refresh cookie
- POST /auth/refresh — validate cookie refresh token, rotate and return new access token
- POST /auth/logout  — revoke refresh token, clear cookie

Middleware:
- requireAuth — validates Bearer JWT on all protected routes
- requireRole('admin') — applied to all /admin/* routes

Security:
- Passwords hashed with bcrypt (cost 12)
- Access tokens expire in 15 minutes
- Refresh tokens stored in DB, rotated on use, revoked on logout
- Rate limiting: 5 login attempts per IP per 15 minutes
```

## Boundaries

- Do NOT implement authentication without HTTPS — note that TLS must be configured at the infrastructure level.
- Do NOT use `Math.random()` or weak hashing for token generation — always use `crypto.randomBytes()` or equivalent.
- Do NOT use `alg: none` or symmetric JWT secrets shorter than 256 bits.
- Do NOT implement "remember me" by simply extending JWT expiry — use proper refresh token rotation.
- Do NOT store sensitive auth tokens in `localStorage` for web clients — prefer httpOnly cookies.
- If the user requests SAML or enterprise SSO, note that these are complex and recommend using an identity provider library or service (Auth0, Okta, Keycloak) rather than building from scratch.
- Always implement rate limiting on authentication endpoints — note if the framework for this is not detected in the project.
