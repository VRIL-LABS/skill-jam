---
name: Cloudflare SSL/TLS
description: >
  Manages Cloudflare SSL/TLS certificates, encryption modes (Flexible, Full, Full Strict), Always Use HTTPS, HSTS, certificate management, and edge SSL termination.
  Invoke when asked to configure SSL/TLS, enable HTTPS, set encryption mode, implement HSTS, manage certificates, configure SSL settings, enable Always Use HTTPS, or secure connections with Cloudflare.
license: MIT
---

# Cloudflare SSL/TLS

Cloudflare provides free SSL/TLS certificates and edge encryption for all domains, eliminating the need to purchase or manually renew certificates. The service supports multiple encryption modes, automatic HTTPS rewrites, HSTS, client certificates, and advanced SSL configurations for enterprise security requirements.

## When to Use

Use Cloudflare SSL/TLS when you need:

- **Free SSL Certificates**: Automatic issuance and renewal of SSL/TLS certificates
- **Edge Encryption**: Terminate SSL at Cloudflare's edge for performance
- **Flexible Encryption Modes**: Choose between Flexible, Full, and Full (Strict)
- **Always Use HTTPS**: Automatic HTTP to HTTPS redirects
- **HSTS**: HTTP Strict Transport Security enforcement
- **Modern TLS**: Support for TLS 1.2, TLS 1.3, and cipher suite control
- **Client Certificates**: Mutual TLS (mTLS) for API protection
- **Custom Certificates**: Upload and manage your own certificates
- **Certificate Pinning**: Advanced certificate validation

**Don't use** if you need end-to-end encryption without Cloudflare termination (use Full Strict mode instead), or if you have specific compliance requirements that prohibit third-party SSL termination.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/ssl/
- **Encryption Modes**: https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/
- **Edge Certificates**: https://developers.cloudflare.com/ssl/edge-certificates/
- **Origin Certificates**: https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/
- **Client Certificates**: https://developers.cloudflare.com/ssl/client-certificates/
- **Always Use HTTPS**: https://developers.cloudflare.com/ssl/edge-certificates/encrypt-visitor-traffic/
- **HSTS**: https://developers.cloudflare.com/ssl/edge-certificates/http-strict-transport-security/
- **TLS 1.3**: https://developers.cloudflare.com/ssl/edge-certificates/tls-13/
- **API Reference**: https://developers.cloudflare.com/api/operations/zone-settings-get-ssl-setting
- **Troubleshooting**: https://developers.cloudflare.com/ssl/troubleshooting/

## Quick Start

### Step 1: Enable Universal SSL (Automatic)

Universal SSL is automatically enabled when you add a domain to Cloudflare:

```bash
# Check SSL status
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/universal/settings" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"

# Certificate is automatically issued within 15 minutes
```

### Step 2: Choose SSL/TLS Encryption Mode

```bash
# Set encryption mode via API
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "full"
  }'

# Modes: "off", "flexible", "full", "full_strict"
```

**Via Dashboard:**
1. Log in to Cloudflare Dashboard
2. Select your domain
3. Go to **SSL/TLS** → **Overview**
4. Select encryption mode:
   - **Off**: No encryption (not recommended)
   - **Flexible**: Cloudflare ↔ Visitor encrypted, Cloudflare ↔ Origin unencrypted
   - **Full**: Cloudflare ↔ Visitor encrypted, Cloudflare ↔ Origin encrypted (self-signed OK)
   - **Full (Strict)**: Cloudflare ↔ Visitor encrypted, Cloudflare ↔ Origin encrypted (valid certificate required)

### Step 3: Enable Always Use HTTPS

```bash
# Enable via API
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/always_use_https" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "on"
  }'
```

### Step 4: Configure HSTS (Optional but Recommended)

```bash
# Enable HSTS
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_header" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": {
      "strict_transport_security": {
        "enabled": true,
        "max_age": 31536000,
        "include_subdomains": true,
        "preload": true,
        "nosniff": true
      }
    }
  }'
```

### Step 5: Verify SSL Configuration

```bash
# Check SSL certificate
curl -vI https://example.com 2>&1 | grep -A 10 "SSL certificate"

# Test SSL Labs
open https://www.ssllabs.com/ssltest/analyze.html?d=example.com

# Verify TLS version
openssl s_client -connect example.com:443 -tls1_3

# Check certificate expiry
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

## Core Features

### 1. SSL/TLS Encryption Modes

#### Flexible SSL
```bash
# Use when origin doesn't support SSL
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "flexible"}'

# Architecture:
# Visitor → [HTTPS] → Cloudflare → [HTTP] → Origin
# ⚠️ Warning: Origin connection is unencrypted
```

#### Full SSL
```bash
# Use when origin has SSL (even self-signed)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "full"}'

# Architecture:
# Visitor → [HTTPS] → Cloudflare → [HTTPS] → Origin
# ✓ End-to-end encryption (accepts self-signed)
```

#### Full (Strict) SSL
```bash
# Use when origin has valid SSL certificate
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "strict"}'

# Architecture:
# Visitor → [HTTPS] → Cloudflare → [HTTPS (validated)] → Origin
# ✓ End-to-end encryption with certificate validation
# Recommended for production
```

### 2. Origin CA Certificates

Generate free certificates for your origin server:

```bash
# Create Origin CA certificate via API
curl -X POST "https://api.cloudflare.com/client/v4/certificates" \
  -H "X-Auth-User-Service-Key: YOUR_ORIGIN_CA_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "hostnames": ["example.com", "*.example.com"],
    "requested_validity": 5475,
    "request_type": "origin-rsa",
    "csr": ""
  }'

# Response includes certificate and private key
# {
#   "result": {
#     "id": "cert_id",
#     "certificate": "-----BEGIN CERTIFICATE-----\n...",
#     "private_key": "-----BEGIN PRIVATE KEY-----\n...",
#     "expires_on": "2039-01-01T00:00:00Z"
#   }
# }
```

**Install on Origin Server (Nginx):**
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/ssl/cloudflare/origin.pem;
    ssl_certificate_key /etc/ssl/cloudflare/origin.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:8080;
    }
}
```

### 3. Edge Certificates

Manage SSL certificates at Cloudflare's edge:

```bash
# List edge certificates
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/certificate_packs" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Order advanced certificate (Advanced Certificate Manager)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/certificate_packs/order" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "advanced",
    "hosts": ["example.com", "*.example.com"],
    "validation_method": "txt",
    "validity_days": 90,
    "certificate_authority": "lets_encrypt"
  }'

# Upload custom certificate
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/custom_certificates" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "certificate": "-----BEGIN CERTIFICATE-----\n...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n..."
  }'
```

### 4. Always Use HTTPS

Automatically redirect HTTP to HTTPS:

```bash
# Enable globally
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/always_use_https" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

# Or use Page Rules for specific paths
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [
      {
        "target": "url",
        "constraint": {
          "operator": "matches",
          "value": "http://example.com/*"
        }
      }
    ],
    "actions": [
      {
        "id": "always_use_https",
        "value": true
      }
    ],
    "status": "active"
  }'
```

### 5. HTTP Strict Transport Security (HSTS)

Force browsers to use HTTPS:

```bash
# Enable HSTS with preload
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_header" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": {
      "strict_transport_security": {
        "enabled": true,
        "max_age": 31536000,
        "include_subdomains": true,
        "preload": true,
        "nosniff": true
      }
    }
  }'

# This sets the header:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Submit to HSTS Preload List:**
1. Enable HSTS with `preload: true`
2. Set `max_age` to at least 31536000 (1 year)
3. Include subdomains
4. Submit at https://hstspreload.org/

### 6. Minimum TLS Version

Control which TLS versions are allowed:

```bash
# Set minimum TLS version to 1.2
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/min_tls_version" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "1.2"
  }'

# Options: "1.0", "1.1", "1.2", "1.3"
# Recommended: "1.2" or "1.3"
```

### 7. TLS 1.3

Enable the latest TLS version:

```bash
# Enable TLS 1.3
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/tls_1_3" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "value": "on"
  }'

# TLS 1.3 benefits:
# - Faster handshakes
# - Improved security
# - 0-RTT resumption
```

## Common Use Cases

### Complete SSL Setup for Production

```bash
#!/bin/bash
ZONE_ID="your_zone_id"
API_TOKEN="your_api_token"

# 1. Set Full (Strict) mode
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/ssl" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "strict"}'

# 2. Enable Always Use HTTPS
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/always_use_https" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

# 3. Enable Automatic HTTPS Rewrites
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/automatic_https_rewrites" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

# 4. Enable HSTS
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/security_header" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "value": {
      "strict_transport_security": {
        "enabled": true,
        "max_age": 31536000,
        "include_subdomains": true,
        "preload": true,
        "nosniff": true
      }
    }
  }'

# 5. Set minimum TLS to 1.2
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/min_tls_version" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "1.2"}'

# 6. Enable TLS 1.3
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/tls_1_3" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

# 7. Enable Opportunistic Encryption
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/opportunistic_encryption" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

echo "SSL/TLS configuration complete!"
```

### Client Certificate Authentication (mTLS)

```bash
# Create client certificate
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/client_certificates" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "csr": "-----BEGIN CERTIFICATE REQUEST-----\n...",
    "validity_days": 365
  }'

# Create mTLS rule (requires Workers or Access)
# Using Cloudflare Access:
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/access/apps" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "API with mTLS",
    "domain": "api.example.com",
    "type": "self_hosted",
    "session_duration": "24h",
    "policies": [{
      "name": "Require Client Certificate",
      "decision": "non_identity",
      "include": [{
        "certificate": {}
      }]
    }]
  }'
```

**Using Workers for mTLS:**
```javascript
export default {
  async fetch(request, env) {
    // Check client certificate
    const clientCert = request.cf?.tlsClientAuth;
    
    if (!clientCert || !clientCert.certVerified) {
      return new Response('Client certificate required', {
        status: 403,
        headers: {
          'Content-Type': 'text/plain',
        },
      });
    }

    // Extract certificate details
    const certDetails = {
      issuer: clientCert.certIssuerDN,
      subject: clientCert.certSubjectDN,
      serial: clientCert.certSerial,
      notBefore: clientCert.certNotBefore,
      notAfter: clientCert.certNotAfter,
    };

    // Validate certificate attributes
    if (!clientCert.certSubjectDN.includes('CN=api-client')) {
      return new Response('Invalid certificate', { status: 403 });
    }

    // Process authenticated request
    return new Response(JSON.stringify({
      message: 'Authenticated',
      client: certDetails,
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
```

### Custom SSL Certificate Upload

```bash
# Upload custom certificate (Business/Enterprise)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/custom_certificates" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "certificate": "-----BEGIN CERTIFICATE-----\nMIID...\n-----END CERTIFICATE-----",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----",
    "bundle_method": "ubiquitous"
  }'

# Update existing custom certificate
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/custom_certificates/{cert_id}" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "certificate": "-----BEGIN CERTIFICATE-----\n...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n..."
  }'

# Delete custom certificate
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/{zone_id}/custom_certificates/{cert_id}" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### SSL for Staging Environments

```bash
# Use Flexible SSL for development (no origin SSL needed)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{staging_zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "flexible"}'

# Or use Origin CA certificate
curl -X POST "https://api.cloudflare.com/client/v4/certificates" \
  -H "X-Auth-User-Service-Key: YOUR_ORIGIN_CA_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "hostnames": ["staging.example.com"],
    "requested_validity": 365,
    "request_type": "origin-rsa"
  }'
```

### Automatic HTTPS Rewrites

Fix mixed content issues:

```bash
# Enable Automatic HTTPS Rewrites
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/automatic_https_rewrites" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

# Rewrites HTTP resources to HTTPS:
# <img src="http://example.com/image.jpg">
# becomes
# <img src="https://example.com/image.jpg">
```

## Integration

### Nginx Origin Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    # Cloudflare Origin CA certificate
    ssl_certificate /etc/ssl/cloudflare/cert.pem;
    ssl_certificate_key /etc/ssl/cloudflare/key.pem;

    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;

    # SSL session optimization
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Only allow Cloudflare IPs (optional)
    include /etc/nginx/cloudflare-ips.conf;
    deny all;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Cloudflare IP whitelist:**
```bash
# /etc/nginx/cloudflare-ips.conf
# Download from https://www.cloudflare.com/ips/
# IPv4
allow 173.245.48.0/20;
allow 103.21.244.0/22;
allow 103.22.200.0/22;
# ... (update periodically)

# IPv6
allow 2400:cb00::/32;
allow 2606:4700::/32;
# ... (update periodically)
```

### Apache Origin Configuration

```apache
<VirtualHost *:443>
    ServerName example.com

    # Cloudflare Origin CA certificate
    SSLEngine on
    SSLCertificateFile /etc/ssl/cloudflare/cert.pem
    SSLCertificateKeyFile /etc/ssl/cloudflare/key.pem

    # Modern SSL configuration
    SSLProtocol -all +TLSv1.2 +TLSv1.3
    SSLCipherSuite ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder on

    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

    # Restrict to Cloudflare IPs
    <RequireAll>
        Require ip 173.245.48.0/20
        Require ip 103.21.244.0/22
        # ... add all Cloudflare ranges
    </RequireAll>

    DocumentRoot /var/www/html
</VirtualHost>
```

### Terraform Configuration

```hcl
resource "cloudflare_zone_settings_override" "example" {
  zone_id = var.zone_id

  settings {
    ssl = "strict"
    always_use_https = "on"
    automatic_https_rewrites = "on"
    min_tls_version = "1.2"
    tls_1_3 = "on"
    opportunistic_encryption = "on"
  }
}

# Enable HSTS
resource "cloudflare_zone_settings_override" "hsts" {
  zone_id = var.zone_id

  settings {
    security_header {
      enabled = true
      max_age = 31536000
      include_subdomains = true
      preload = true
      nosniff = true
    }
  }
}

# Order Advanced Certificate
resource "cloudflare_certificate_pack" "advanced" {
  zone_id = var.zone_id
  type    = "advanced"
  hosts   = ["example.com", "*.example.com"]
  
  validation_method = "txt"
  validity_days     = 90
  certificate_authority = "lets_encrypt"
}
```

### Node.js / Express

```javascript
const express = require('express');
const helmet = require('helmet');

const app = express();

// Trust Cloudflare proxy
app.set('trust proxy', true);

// Security headers with Helmet
app.use(helmet({
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      upgradeInsecureRequests: [],
    },
  },
}));

// Force HTTPS (redundant if using Cloudflare Always Use HTTPS)
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    res.redirect(`https://${req.header('host')}${req.url}`);
  } else {
    next();
  }
});

app.listen(3000);
```

## Best Practices

### 1. Use Full (Strict) Mode in Production

```bash
# Always use Full (Strict) for maximum security
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "strict"}'

# Ensure origin has valid certificate
# Use Let's Encrypt, commercial CA, or Cloudflare Origin CA
```

### 2. Enable HSTS Gradually

```bash
# Start with short max-age (e.g., 1 week)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_header" \
  --data '{
    "value": {
      "strict_transport_security": {
        "enabled": true,
        "max_age": 604800,
        "include_subdomains": false,
        "preload": false
      }
    }
  }'

# After testing, increase to 1 year and add preload
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_header" \
  --data '{
    "value": {
      "strict_transport_security": {
        "enabled": true,
        "max_age": 31536000,
        "include_subdomains": true,
        "preload": true
      }
    }
  }'
```

### 3. Monitor Certificate Expiration

```python
import requests
from datetime import datetime, timedelta

def check_certificate_expiry(zone_id, api_token):
    """Monitor SSL certificate expiration"""
    
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/certificate_packs'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    certs = response.json()['result']
    
    for cert in certs:
        expiry = datetime.fromisoformat(cert['expires_on'].replace('Z', '+00:00'))
        days_until_expiry = (expiry - datetime.now(expiry.tzinfo)).days
        
        if days_until_expiry < 30:
            print(f"⚠️  Certificate {cert['id']} expires in {days_until_expiry} days")
        else:
            print(f"✓ Certificate {cert['id']} valid for {days_until_expiry} days")

# Universal SSL certificates auto-renew
# Custom certificates require manual renewal
```

### 4. Test SSL Configuration

```bash
# Use SSL Labs
curl -s "https://api.ssllabs.com/api/v3/analyze?host=example.com" | jq .

# Test with OpenSSL
openssl s_client -connect example.com:443 -servername example.com < /dev/null

# Check cipher suites
nmap --script ssl-enum-ciphers -p 443 example.com

# Verify HSTS
curl -I https://example.com | grep -i strict-transport-security
```

### 5. Handle Certificate Validation Errors

```javascript
// Worker to handle SSL errors gracefully
export default {
  async fetch(request, env) {
    try {
      const response = await fetch(request);
      return response;
    } catch (err) {
      if (err.message.includes('SSL')) {
        console.error('SSL error:', err);
        
        return new Response('SSL/TLS configuration error. Please contact support.', {
          status: 502,
          headers: {
            'Content-Type': 'text/plain',
          },
        });
      }
      throw err;
    }
  }
};
```

## Troubleshooting

### SSL Certificate Not Provisioning

```bash
# Check Universal SSL status
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/universal/settings" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Common issues:
# 1. CAA records blocking issuance
dig example.com CAA

# If CAA exists, ensure it allows Cloudflare:
# example.com. 300 IN CAA 0 issue "pki.goog; letsencrypt.org; digicert.com"

# 2. DNS not resolving
dig example.com

# 3. Wait 15-24 hours for initial issuance
```

### SSL Errors (ERR_SSL_VERSION_OR_CIPHER_MISMATCH)

```bash
# Check minimum TLS version
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/min_tls_version" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Lower to 1.0 temporarily to test
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/min_tls_version" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  --data '{"value": "1.0"}'

# Test with different TLS versions
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3
```

### Origin SSL Certificate Errors

```bash
# Error: "SSL Handshake Failed" or "526"

# 1. Verify origin certificate is valid
openssl s_client -connect origin-server-ip:443 -servername example.com

# 2. Check if using self-signed cert with Full (Strict)
# Solution: Use Full mode or install valid certificate

# 3. Verify SSL mode matches origin setup
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### Mixed Content Warnings

```bash
# Enable Automatic HTTPS Rewrites
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/automatic_https_rewrites" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  --data '{"value": "on"}'

# Or use Content Security Policy
# Content-Security-Policy: upgrade-insecure-requests
```

### Too Many Redirects

```bash
# Usually caused by:
# 1. Origin also redirecting to HTTPS
# 2. Flexible SSL with origin forcing HTTPS

# Solution: Use Full or Full (Strict) mode
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl" \
  --data '{"value": "full"}'

# Or configure origin to trust X-Forwarded-Proto header
```

## See Also

- **Cloudflare Access**: https://developers.cloudflare.com/cloudflare-one/applications/
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **API Shield**: https://developers.cloudflare.com/api-shield/
- **Bot Management**: https://developers.cloudflare.com/bots/
- **Certificate Transparency**: https://developers.cloudflare.com/ssl/edge-certificates/certificate-transparency-monitoring/
- **Authenticated Origin Pulls**: https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/
- **Cipher Suites**: https://developers.cloudflare.com/ssl/reference/cipher-suites/
- **Let's Encrypt**: https://letsencrypt.org/
