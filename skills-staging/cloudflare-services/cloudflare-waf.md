---
name: Cloudflare WAF
description: >
  Manages Cloudflare Web Application Firewall (WAF) for protection against OWASP Top 10 vulnerabilities, custom and managed rulesets, rate limiting, bot mitigation, and advanced threat detection.
  Invoke when asked to configure WAF, block attacks, create custom rules, implement rate limiting, protect against OWASP threats, mitigate bots, filter malicious traffic, or secure web applications with Cloudflare.
license: MIT
---

# Cloudflare WAF (Web Application Firewall)

Cloudflare's Web Application Firewall (WAF) protects web applications from common exploits and vulnerabilities including the OWASP Top 10. It provides managed rulesets, custom rule creation, rate limiting, bot protection, and real-time threat intelligence to defend against SQL injection, XSS, DDoS, and other web attacks.

## When to Use

Use Cloudflare WAF when you need:

- **OWASP Top 10 Protection**: Defense against common web vulnerabilities
- **Managed Rulesets**: Pre-configured rules for known attack patterns
- **Custom Rules**: Create specific security rules for your application
- **Rate Limiting**: Protect against brute force and DDoS attacks
- **Bot Mitigation**: Block malicious bots while allowing legitimate traffic
- **Geo-Blocking**: Block or allow traffic from specific countries
- **IP Reputation**: Automatic blocking of known malicious IPs
- **Zero-Day Protection**: Quick deployment of rules for new threats
- **API Protection**: Secure REST and GraphQL APIs

**Don't use** WAF as a replacement for secure coding practices, input validation in your application, or proper authentication mechanisms. WAF is a defense layer, not a substitute for application security.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/waf/
- **Managed Rules**: https://developers.cloudflare.com/waf/managed-rules/
- **Custom Rules**: https://developers.cloudflare.com/waf/custom-rules/
- **Rate Limiting**: https://developers.cloudflare.com/waf/rate-limiting-rules/
- **WAF Analytics**: https://developers.cloudflare.com/waf/analytics/
- **Firewall Rules (Legacy)**: https://developers.cloudflare.com/firewall/
- **API Reference**: https://developers.cloudflare.com/api/operations/waf-managed-rulesets-list-managed-rulesets
- **OWASP Core Ruleset**: https://developers.cloudflare.com/waf/managed-rules/reference/owasp-core-ruleset/
- **Best Practices**: https://developers.cloudflare.com/waf/best-practices/
- **Change Log**: https://developers.cloudflare.com/waf/change-log/

## Quick Start

### Step 1: Enable WAF Managed Rules

**Via Dashboard:**
1. Log in to Cloudflare Dashboard
2. Select your domain
3. Go to **Security** → **WAF**
4. Click **Deploy a managed ruleset**
5. Select **Cloudflare Managed Ruleset**
6. Click **Deploy**

**Via API:**
```bash
# Deploy Cloudflare Managed Ruleset
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "efb7b8c949ac4650a09736fc376e9aee"
        },
        "expression": "true",
        "description": "Execute Cloudflare Managed Ruleset"
      }
    ]
  }'
```

### Step 2: Create a Custom WAF Rule

```bash
# Block requests with SQL injection patterns
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "(http.request.uri.query contains \"union select\") or (http.request.uri.query contains \"<script>\")",
    "description": "Block SQL injection and XSS attempts",
    "enabled": true
  }'
```

### Step 3: Configure Rate Limiting

```bash
# Rate limit: Max 100 requests per minute per IP
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_ratelimit/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "true",
    "description": "Rate limit all requests",
    "action_parameters": {
      "response": {
        "status_code": 429,
        "content": "Too many requests",
        "content_type": "text/plain"
      }
    },
    "ratelimit": {
      "characteristics": ["ip.src"],
      "period": 60,
      "requests_per_period": 100,
      "mitigation_timeout": 600
    }
  }'
```

### Step 4: Enable Security Level

```bash
# Set security level to "High"
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "high"
  }'

# Options: "off", "essentially_off", "low", "medium", "high", "under_attack"
```

### Step 5: Monitor WAF Events

```bash
# Get WAF analytics
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/events?per_page=50" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"

# Filter by action
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/events?action=block" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

## Core Features

### 1. Managed Rulesets

Deploy pre-configured security rules:

```bash
# Cloudflare Managed Ruleset (all customers)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "efb7b8c949ac4650a09736fc376e9aee",
          "overrides": {
            "enabled": true,
            "action": "block"
          }
        },
        "expression": "true"
      }
    ]
  }'

# OWASP Core Ruleset (Pro and above)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "4814384a9e5d4991b9815dcfc25d2f1f",
          "overrides": {
            "enabled": true,
            "sensitivity_level": "medium"
          }
        },
        "expression": "true"
      }
    ]
  }'

# Cloudflare Exposed Credentials Check (Enterprise)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "c2e184081120413c86c3ab7e14069605"
        },
        "expression": "http.request.method == \"POST\""
      }
    ]
  }'
```

### 2. Custom WAF Rules

Create application-specific security rules:

```bash
# Block specific user agents
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "(http.user_agent contains \"curl\") or (http.user_agent contains \"wget\")",
    "description": "Block command-line tools"
  }'

# Challenge requests from specific countries
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "managed_challenge",
    "expression": "ip.geoip.country in {\"CN\" \"RU\" \"KP\"}",
    "description": "Challenge traffic from high-risk countries"
  }'

# Protect admin panel
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "(http.request.uri.path contains \"/admin\") and (ip.src ne 203.0.113.1)",
    "description": "Restrict admin access to office IP"
  }'

# Block requests with suspicious patterns
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "(http.request.uri.query contains \"../\") or (http.request.uri.query contains \"/etc/passwd\") or (http.request.uri.query contains \"cmd.exe\")",
    "description": "Block path traversal attempts"
  }'

# Skip WAF for trusted IPs
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "skip",
    "action_parameters": {
      "ruleset": "current"
    },
    "expression": "ip.src in {203.0.113.0/24}",
    "description": "Skip WAF for office network"
  }'
```

### 3. Rate Limiting Rules

Protect against abuse and DDoS:

```bash
# Rate limit login endpoint
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_ratelimit/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "http.request.uri.path eq \"/login\"",
    "description": "Login rate limit",
    "action_parameters": {
      "response": {
        "status_code": 429,
        "content": "{\"error\": \"Too many login attempts. Try again later.\"}",
        "content_type": "application/json"
      }
    },
    "ratelimit": {
      "characteristics": ["ip.src"],
      "period": 60,
      "requests_per_period": 5,
      "mitigation_timeout": 600
    }
  }'

# API rate limit per API key
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_ratelimit/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "http.request.uri.path contains \"/api/\"",
    "description": "API rate limit per key",
    "ratelimit": {
      "characteristics": ["http.request.headers[\"x-api-key\"]"],
      "period": 60,
      "requests_per_period": 100,
      "mitigation_timeout": 300
    }
  }'

# Rate limit by country
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_ratelimit/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "managed_challenge",
    "expression": "ip.geoip.country eq \"CN\"",
    "description": "Challenge high-volume traffic from CN",
    "ratelimit": {
      "characteristics": ["ip.src"],
      "period": 10,
      "requests_per_period": 10,
      "mitigation_timeout": 60
    }
  }'

# Complex rate limit (IP + ASN)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_ratelimit/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "true",
    "description": "Multi-characteristic rate limit",
    "ratelimit": {
      "characteristics": ["ip.src", "ip.geoip.asnum"],
      "period": 60,
      "requests_per_period": 200,
      "mitigation_timeout": 300,
      "counting_expression": "http.request.uri.path eq \"/search\""
    }
  }'
```

### 4. Bot Protection

Detect and mitigate automated traffic:

```bash
# Block definitively automated traffic
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "cf.bot_management.score lt 30",
    "description": "Block bots with low score"
  }'

# Challenge likely bots
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "managed_challenge",
    "expression": "cf.bot_management.score lt 50 and not cf.bot_management.verified_bot",
    "description": "Challenge suspicious traffic"
  }'

# Allow verified bots (Google, Bing, etc.)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "skip",
    "action_parameters": {
      "ruleset": "current"
    },
    "expression": "cf.bot_management.verified_bot",
    "description": "Allow verified search engines"
  }'

# Block bots on specific endpoints
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "js_challenge",
    "expression": "(http.request.uri.path contains \"/api/\") and (cf.bot_management.score lt 50)",
    "description": "JS Challenge bots on API"
  }'
```

### 5. IP Lists

Manage IP allowlists and blocklists:

```bash
# Create IP list
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/rules/lists" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "office_ips",
    "description": "Office IP addresses",
    "kind": "ip"
  }'

# Add IPs to list
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/rules/lists/{list_id}/items" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '[
    {"ip": "203.0.113.1", "comment": "Office"},
    {"ip": "203.0.113.0/24", "comment": "Office network"},
    {"ip": "2001:db8::/32", "comment": "Office IPv6"}
  ]'

# Use IP list in WAF rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "skip",
    "action_parameters": {
      "ruleset": "current"
    },
    "expression": "ip.src in $office_ips",
    "description": "Skip WAF for office IPs"
  }'
```

## Common Use Cases

### Comprehensive Security Configuration

```bash
#!/bin/bash
ZONE_ID="your_zone_id"
API_TOKEN="your_api_token"

# 1. Deploy managed rulesets
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "efb7b8c949ac4650a09736fc376e9aee"
        },
        "expression": "true",
        "description": "Cloudflare Managed Ruleset"
      }
    ]
  }'

# 2. Set security level to High
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/security_level" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "high"}'

# 3. Enable Browser Integrity Check
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/browser_check" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

# 4. Enable Challenge Passage
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/challenge_ttl" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": 1800}'

echo "WAF configuration complete!"
```

### Protect Login Endpoint

```bash
# Create comprehensive login protection
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "(http.request.uri.path eq \"/login\" or http.request.uri.path eq \"/api/auth\") and (http.request.method eq \"POST\") and (http.request.body.form[\"username\"][0] contains \"admin\" or http.request.body.form[\"password\"][0] contains \"password\")",
    "description": "Block common credential stuffing"
  }'

# Add rate limiting
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_ratelimit/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "http.request.uri.path eq \"/login\" and http.request.method eq \"POST\"",
    "description": "Login rate limit",
    "ratelimit": {
      "characteristics": ["ip.src"],
      "period": 300,
      "requests_per_period": 5,
      "mitigation_timeout": 3600
    }
  }'
```

### API Protection

```javascript
// Worker with WAF integration for API
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Check if request is to API
    if (!url.pathname.startsWith('/api/')) {
      return fetch(request);
    }

    // Validate API key
    const apiKey = request.headers.get('X-API-Key');
    if (!apiKey) {
      return new Response('API key required', {
        status: 401,
        headers: { 'Content-Type': 'text/plain' },
      });
    }

    // Check bot score
    const botScore = request.cf?.botManagement?.score || 0;
    if (botScore < 30) {
      return new Response('Bot detected', {
        status: 403,
        headers: { 'Content-Type': 'text/plain' },
      });
    }

    // Rate limiting (check headers from WAF)
    const rateLimit = request.headers.get('CF-Ray');
    
    // Validate request body for API calls
    if (request.method === 'POST' || request.method === 'PUT') {
      const contentType = request.headers.get('Content-Type');
      if (!contentType?.includes('application/json')) {
        return new Response('Invalid content type', {
          status: 400,
          headers: { 'Content-Type': 'text/plain' },
        });
      }

      // Check body size
      const contentLength = parseInt(request.headers.get('Content-Length') || '0');
      if (contentLength > 1000000) { // 1MB
        return new Response('Request too large', {
          status: 413,
          headers: { 'Content-Type': 'text/plain' },
        });
      }
    }

    // Forward to origin
    return fetch(request);
  }
};
```

### Under Attack Mode

```bash
# Enable "Under Attack" mode during DDoS
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "under_attack"
  }'

# This shows interstitial challenge to all visitors
# After attack subsides, return to normal:

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "medium"
  }'
```

### Geo-Blocking with Exceptions

```bash
# Block all countries except allowed list
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "not ip.geoip.country in {\"US\" \"CA\" \"GB\" \"DE\" \"FR\"}",
    "description": "Allow only specific countries"
  }'

# Exception for specific paths
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "skip",
    "action_parameters": {
      "ruleset": "current"
    },
    "expression": "http.request.uri.path eq \"/api/webhook\"",
    "description": "Allow webhooks from any country"
  }'
```

## Integration

### Terraform Configuration

```hcl
# Managed ruleset
resource "cloudflare_ruleset" "waf_managed" {
  zone_id     = var.zone_id
  name        = "WAF Managed Rules"
  description = "Managed WAF ruleset"
  kind        = "zone"
  phase       = "http_request_firewall_managed"

  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
    }
    expression  = "true"
    description = "Execute Cloudflare Managed Ruleset"
    enabled     = true
  }
}

# Custom WAF rules
resource "cloudflare_ruleset" "waf_custom" {
  zone_id     = var.zone_id
  name        = "Custom WAF Rules"
  description = "Application-specific WAF rules"
  kind        = "zone"
  phase       = "http_request_firewall_custom"

  rules {
    action      = "block"
    expression  = "(http.request.uri.query contains \"union select\")"
    description = "Block SQL injection"
    enabled     = true
  }

  rules {
    action      = "managed_challenge"
    expression  = "cf.bot_management.score lt 30"
    description = "Challenge bots"
    enabled     = true
  }
}

# Rate limiting
resource "cloudflare_ruleset" "rate_limit" {
  zone_id     = var.zone_id
  name        = "Rate Limiting"
  description = "Rate limiting rules"
  kind        = "zone"
  phase       = "http_ratelimit"

  rules {
    action      = "block"
    expression  = "http.request.uri.path eq \"/login\""
    description = "Login rate limit"
    enabled     = true

    action_parameters {
      response {
        status_code  = 429
        content      = "Too many requests"
        content_type = "text/plain"
      }
    }

    ratelimit {
      characteristics      = ["ip.src"]
      period               = 60
      requests_per_period  = 5
      mitigation_timeout   = 600
    }
  }
}

# IP list
resource "cloudflare_list" "trusted_ips" {
  account_id  = var.account_id
  name        = "trusted_ips"
  description = "Trusted IP addresses"
  kind        = "ip"

  item {
    value {
      ip = "203.0.113.1"
    }
    comment = "Office IP"
  }
}
```

### Python Integration

```python
import requests

class CloudflareWAF:
    def __init__(self, zone_id, api_token):
        self.zone_id = zone_id
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def create_custom_rule(self, expression, action, description):
        """Create a custom WAF rule"""
        url = f"{self.base_url}/zones/{self.zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules"
        data = {
            "action": action,
            "expression": expression,
            "description": description,
            "enabled": True
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def set_security_level(self, level):
        """Set zone security level"""
        url = f"{self.base_url}/zones/{self.zone_id}/settings/security_level"
        data = {"value": level}
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()
    
    def get_firewall_events(self, limit=50, action=None):
        """Get WAF events"""
        url = f"{self.base_url}/zones/{self.zone_id}/firewall/events"
        params = {"per_page": limit}
        if action:
            params["action"] = action
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def block_ip(self, ip, comment):
        """Add IP to block list"""
        # Create IP list if not exists, then add IP
        # Implementation depends on your IP list structure
        pass

# Usage
waf = CloudflareWAF(zone_id="your_zone", api_token="your_token")

# Block SQL injection
waf.create_custom_rule(
    expression='(http.request.uri.query contains "union select")',
    action="block",
    description="Block SQL injection"
)

# Enable Under Attack mode
waf.set_security_level("under_attack")

# Get recent blocks
events = waf.get_firewall_events(limit=100, action="block")
```

## Best Practices

### 1. Start with Monitor Mode

```bash
# Test rules in log-only mode first
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "log",
    "expression": "(http.request.uri.query contains \"test\")",
    "description": "Test rule - monitoring only"
  }'

# Review logs, then change action to "block"
```

### 2. Use Skip Actions Wisely

```bash
# Skip WAF for trusted sources first
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "skip",
    "action_parameters": {
      "ruleset": "current"
    },
    "expression": "ip.src in $trusted_ips",
    "description": "Skip all rules for trusted IPs",
    "position": {
      "index": 1
    }
  }'
```

### 3. Layer Your Security

```text
Order of execution:
1. IP allowlist (skip rules)
2. IP blocklist (block bad actors)
3. Geo-blocking (restrict countries)
4. Rate limiting (prevent abuse)
5. Bot detection (challenge suspicious)
6. Custom rules (app-specific)
7. Managed rulesets (OWASP, etc.)
```

### 4. Monitor and Tune

```python
# Regular monitoring script
def analyze_waf_events(zone_id, api_token):
    """Analyze WAF events for tuning"""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/events"
    response = requests.get(url, headers=headers, params={"per_page": 1000})
    events = response.json()["result"]
    
    # Count by action
    action_counts = {}
    for event in events:
        action = event["action"]
        action_counts[action] = action_counts.get(action, 0) + 1
    
    # Find false positives (legitimate traffic blocked)
    for event in events:
        if event["action"] == "block":
            # Check if it might be legitimate
            print(f"Blocked: {event['clientIP']} - {event['userAgent']} - Rule: {event['ruleId']}")
    
    return action_counts

# Run regularly and adjust rules
```

### 5. Document Your Rules

```bash
# Always include descriptive comments
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "action": "block",
    "expression": "ip.src eq 192.0.2.1",
    "description": "Block malicious IP - Ticket #12345 - Added 2024-01-15"
  }'
```

## Troubleshooting

### False Positives

```bash
# Identify blocked requests
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/events?action=block" \
  -H "Authorization: Bearer YOUR_API_TOKEN" | jq '.result[] | {ip: .clientIP, path: .clientRequestPath, rule: .ruleId}'

# Disable specific rule causing false positive
# Or add exception:
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  --data '{
    "action": "skip",
    "action_parameters": {"rules": {"ef3b8c949ac4650a09736fc376e9123"}},
    "expression": "http.request.uri.path eq \"/false-positive-path\""
  }'
```

### Rate Limiting Too Strict

```bash
# Increase threshold
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "ratelimit": {
      "requests_per_period": 200,
      "period": 60
    }
  }'
```

### WAF Not Blocking Attacks

```bash
# Check rule order (skip rules first)
# Verify expression syntax
# Test rule expression:
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint/rules" \
  --data '{
    "action": "log",
    "expression": "YOUR_EXPRESSION_HERE"
  }'

# Review logs to see if rule is matching
```

## See Also

- **Cloudflare Access**: https://developers.cloudflare.com/cloudflare-one/applications/
- **DDoS Protection**: https://developers.cloudflare.com/ddos-protection/
- **Bot Management**: https://developers.cloudflare.com/bots/
- **Page Shield**: https://developers.cloudflare.com/page-shield/
- **API Shield**: https://developers.cloudflare.com/api-shield/
- **Firewall Rules**: https://developers.cloudflare.com/firewall/
- **Security Analytics**: https://developers.cloudflare.com/analytics/security-analytics/
- **Ruleset Engine**: https://developers.cloudflare.com/ruleset-engine/
