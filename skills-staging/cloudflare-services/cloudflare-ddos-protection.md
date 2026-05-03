---
name: Cloudflare DDoS Protection
description: Configure Cloudflare DDoS Protection to automatically detect and mitigate volumetric and application-layer attacks with real-time L3/L4 and L7 protection. Trigger phrases include "DDoS protection", "DDoS mitigation", "stop DDoS attacks", "volumetric attack protection", "layer 7 DDoS", and "application-layer DDoS".
license: MIT
---

# Cloudflare DDoS Protection

Cloudflare DDoS Protection provides automatic, always-on protection against Distributed Denial of Service attacks at all layers of the network stack. It leverages Cloudflare's global network to detect and mitigate attacks in real-time, protecting your applications and infrastructure from volumetric, protocol, and application-layer attacks.

## When to Use

Use Cloudflare DDoS Protection when you need to:

- **Protect web applications** from volumetric and application-layer DDoS attacks
- **Defend infrastructure** against L3/L4 network and transport layer attacks
- **Ensure availability** during large-scale attack campaigns
- **Automatically mitigate** attacks without manual intervention
- **Gain visibility** into attack patterns and traffic anomalies
- **Comply with SLAs** requiring high uptime and availability
- **Scale protection** across multiple domains and IP ranges
- **Reduce operational overhead** of managing DDoS defenses
- **Protect APIs and microservices** from targeted attacks
- **Defend against emerging threats** with continuously updated rule sets

Cloudflare DDoS Protection is essential for any internet-facing application or service that requires high availability and resilience against denial-of-service attacks.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/ddos-protection/
- **Managed Rulesets**: https://developers.cloudflare.com/ddos-protection/managed-rulesets/
- **Network-layer DDoS Attack Protection**: https://developers.cloudflare.com/ddos-protection/managed-rulesets/network/
- **HTTP DDoS Attack Protection**: https://developers.cloudflare.com/ddos-protection/managed-rulesets/http/
- **Advanced TCP Protection**: https://developers.cloudflare.com/ddos-protection/tcp-protection/
- **Best Practices**: https://developers.cloudflare.com/ddos-protection/best-practices/
- **Analytics and Reporting**: https://developers.cloudflare.com/ddos-protection/reference/analytics/
- **Change Log**: https://developers.cloudflare.com/ddos-protection/change-log/

## Quick Start

### Enable DDoS Protection (Dashboard)

1. **Log in to Cloudflare Dashboard**
   ```
   Navigate to: https://dash.cloudflare.com
   Select your account and domain
   ```

2. **Access Security Settings**
   ```
   Go to Security > DDoS
   ```

3. **Configure HTTP DDoS Attack Protection**
   ```
   - View the HTTP DDoS Attack Protection managed ruleset
   - Enable/disable rules as needed
   - Configure sensitivity levels: Low, Medium, High, or Essentially Off
   - Set custom expressions for specific rules
   ```

4. **Configure Network-layer DDoS Attack Protection**
   ```
   - Navigate to Network-layer DDoS Attack Protection
   - Review default protection settings
   - Adjust sensitivity for specific attack vectors
   - Configure Advanced TCP Protection (if available)
   ```

### Configure via API

```bash
# Get account ID and zone ID
ACCOUNT_ID="your_account_id"
ZONE_ID="your_zone_id"
API_TOKEN="your_api_token"

# List HTTP DDoS managed ruleset
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json"

# Update HTTP DDoS ruleset with custom sensitivity
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "efb7b8c949ac4650a09736fc376e9aee",
          "overrides": {
            "sensitivity_level": "high"
          }
        },
        "expression": "true",
        "description": "Execute HTTP DDoS Attack Protection ruleset"
      }
    ]
  }'
```

### Configure Network-layer DDoS Protection

```bash
# Update network-layer DDoS protection
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/rulesets/phases/ddos_l4/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "3b2c7f3d1f3e4c9a8b1e5f6a7c8d9e0f",
          "overrides": {
            "sensitivity_level": "medium"
          }
        },
        "expression": "true",
        "description": "Execute Network-layer DDoS Attack Protection"
      }
    ]
  }'
```

### Terraform Configuration

```hcl
# Configure HTTP DDoS protection ruleset
resource "cloudflare_ruleset" "http_ddos_protection" {
  zone_id     = var.zone_id
  name        = "HTTP DDoS Attack Protection"
  description = "Custom HTTP DDoS protection configuration"
  kind        = "zone"
  phase       = "http_request_firewall_managed"

  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "high"
        
        # Override specific rules
        rules {
          id                = "rule_id_here"
          sensitivity_level = "medium"
          action            = "block"
        }
      }
    }
    expression  = "true"
    description = "Execute HTTP DDoS managed ruleset with high sensitivity"
    enabled     = true
  }
}

# Configure network-layer DDoS protection
resource "cloudflare_ruleset" "network_ddos_protection" {
  account_id  = var.account_id
  name        = "Network-layer DDoS Protection"
  description = "Custom L3/L4 DDoS protection"
  kind        = "root"
  phase       = "ddos_l4"

  rules {
    action = "execute"
    action_parameters {
      id = "3b2c7f3d1f3e4c9a8b1e5f6a7c8d9e0f"
      overrides {
        sensitivity_level = "high"
      }
    }
    expression  = "true"
    description = "Network-layer DDoS protection"
    enabled     = true
  }
}

# Configure Advanced TCP Protection
resource "cloudflare_ruleset" "advanced_tcp_protection" {
  zone_id     = var.zone_id
  name        = "Advanced TCP Protection"
  description = "TCP-level attack protection"
  kind        = "zone"
  phase       = "ddos_l4"

  rules {
    action = "execute"
    action_parameters {
      id = "advanced_tcp_protection_ruleset_id"
      overrides {
        sensitivity_level = "high"
      }
    }
    expression  = "ip.src.country in {\"CN\" \"RU\"}"
    description = "Enhanced TCP protection for specific countries"
    enabled     = true
  }
}
```

## Core Features

### 1. HTTP DDoS Attack Protection (L7)

Protects against application-layer attacks targeting HTTP/HTTPS services.

**Key Capabilities:**
- Automatic detection of HTTP floods
- Protection against Slowloris and slow POST attacks
- Bot and scraper mitigation
- Request rate limiting
- Header and method-based attack detection
- Regular expression-based filtering
- Custom rule overrides

**Sensitivity Levels:**
- **Essentially Off**: Minimal protection, only blocks the most obvious attacks
- **Low**: Balanced approach with fewer false positives
- **Medium**: Default setting, recommended for most use cases
- **High**: Aggressive protection, may block some legitimate traffic
- **Custom**: Fine-tune individual rules based on specific needs

**Configuration Example:**
```bash
# Set specific sensitivity for API endpoints
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "efb7b8c949ac4650a09736fc376e9aee",
          "overrides": {
            "rules": [
              {
                "id": "specific_rule_id",
                "sensitivity_level": "high",
                "action": "block"
              }
            ]
          }
        },
        "expression": "http.request.uri.path contains \"/api/\"",
        "description": "High sensitivity for API paths"
      }
    ]
  }'
```

### 2. Network-layer DDoS Attack Protection (L3/L4)

Defends against volumetric and protocol attacks at the network and transport layers.

**Protected Attack Vectors:**
- UDP floods
- SYN floods
- ACK floods
- DNS amplification
- NTP amplification
- SSDP amplification
- GRE floods
- ICMP floods
- IP fragmentation attacks

**Features:**
- Automatic mitigation at the edge
- No user configuration required for basic protection
- Advanced configuration for custom needs
- Support for Magic Transit customers
- Prefix-based protection

**Advanced Configuration:**
```bash
# Configure protection for specific IP prefixes
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/rulesets" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom L4 DDoS Protection",
    "kind": "root",
    "phase": "ddos_l4",
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "network_layer_ruleset_id",
          "overrides": {
            "sensitivity_level": "high"
          }
        },
        "expression": "ip.dst in {203.0.113.0/24}",
        "description": "High sensitivity for critical IP range"
      }
    ]
  }'
```

### 3. Advanced TCP Protection

Sophisticated protection against TCP-based attacks with behavioral analysis.

**Features:**
- SYN flood protection
- Out-of-state TCP packet filtering
- Connection rate limiting
- Geographic-based filtering
- Automatic threshold adjustments

**Configuration:**
```hcl
resource "cloudflare_ruleset" "tcp_protection" {
  zone_id = var.zone_id
  name    = "Advanced TCP Protection"
  kind    = "zone"
  phase   = "ddos_l4"

  rules {
    action = "execute"
    action_parameters {
      id = "tcp_protection_ruleset_id"
      overrides {
        sensitivity_level = "high"
        rules {
          id     = "syn_flood_protection"
          action = "block"
        }
      }
    }
    expression  = "tcp.flags.syn and not tcp.flags.ack"
    description = "Block SYN flood attempts"
    enabled     = true
  }
}
```

### 4. Analytics and Reporting

Comprehensive visibility into attack patterns and mitigation actions.

**Available Metrics:**
- Attack volume and duration
- Attack types and vectors
- Mitigated vs. unmitigated traffic
- Top attacked targets
- Geographic distribution of attacks
- Rate limiting actions
- Historical trends

**Query Analytics via API:**
```bash
# Get DDoS attack analytics
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/analytics/ddos" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-urlencode "since=2024-01-01T00:00:00Z" \
  --data-urlencode "until=2024-01-31T23:59:59Z"

# Get network-layer DDoS analytics
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/analytics/network_analytics" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-urlencode "dimensions=datetime,attackType" \
  --data-urlencode "metrics=bytesTotal,packetsTotal"
```

## Common Use Cases

### 1. E-commerce Platform Protection

Protect online stores during high-traffic events and against targeted attacks.

```hcl
# Comprehensive DDoS protection for e-commerce
resource "cloudflare_ruleset" "ecommerce_ddos" {
  zone_id     = var.zone_id
  name        = "E-commerce DDoS Protection"
  description = "Multi-layer protection for online store"
  kind        = "zone"
  phase       = "http_request_firewall_managed"

  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "high"
        
        # Extra protection for checkout
        rules {
          id                = "http_flood_rule_id"
          sensitivity_level = "high"
          action            = "challenge"
        }
      }
    }
    expression  = "http.request.uri.path contains \"/checkout\" or http.request.uri.path contains \"/cart\""
    description = "High sensitivity for checkout and cart"
    enabled     = true
  }

  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "medium"
      }
    }
    expression  = "true"
    description = "Medium sensitivity for all other paths"
    enabled     = true
  }
}
```

### 2. API Service Protection

Shield API endpoints from targeted attacks and abuse.

```bash
# API-specific DDoS configuration
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "efb7b8c949ac4650a09736fc376e9aee",
          "overrides": {
            "sensitivity_level": "high",
            "rules": [
              {
                "id": "http_anomaly_rule",
                "sensitivity_level": "high",
                "action": "block"
              }
            ]
          }
        },
        "expression": "http.request.uri.path matches \"^/api/v[0-9]+/\"",
        "description": "Enhanced protection for API endpoints",
        "enabled": true
      }
    ]
  }'
```

### 3. Gaming Server Protection

Protect game servers from volumetric attacks and ensure low-latency gameplay.

```bash
# Network-layer protection for gaming
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/rulesets/phases/ddos_l4/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      {
        "action": "execute",
        "action_parameters": {
          "id": "network_ddos_ruleset_id",
          "overrides": {
            "sensitivity_level": "high",
            "rules": [
              {
                "id": "udp_flood_rule",
                "sensitivity_level": "high",
                "action": "block"
              }
            ]
          }
        },
        "expression": "ip.dst in {203.0.113.100/32} and ip.proto == \"udp\"",
        "description": "High sensitivity UDP protection for game servers",
        "enabled": true
      }
    ]
  }'
```

### 4. Content Delivery Protection

Secure CDN resources and media delivery from abuse.

```hcl
resource "cloudflare_ruleset" "cdn_ddos_protection" {
  zone_id = var.zone_id
  name    = "CDN DDoS Protection"
  kind    = "zone"
  phase   = "http_request_firewall_managed"

  # Strict protection for video streaming
  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "high"
      }
    }
    expression  = "http.request.uri.path matches \"\\.(mp4|m3u8|ts)$\""
    description = "High protection for streaming content"
    enabled     = true
  }

  # Moderate protection for static assets
  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "medium"
      }
    }
    expression  = "http.request.uri.path matches \"\\.(jpg|png|css|js)$\""
    description = "Medium protection for static assets"
    enabled     = true
  }
}
```

## Integration

### 1. Integration with WAF

Combine DDoS protection with Web Application Firewall for comprehensive security.

```hcl
# WAF + DDoS combined ruleset
resource "cloudflare_ruleset" "combined_protection" {
  zone_id = var.zone_id
  name    = "WAF and DDoS Protection"
  kind    = "zone"
  phase   = "http_request_firewall_managed"

  # DDoS protection rule
  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "high"
      }
    }
    expression  = "true"
    description = "HTTP DDoS protection"
    enabled     = true
  }

  # WAF managed ruleset
  rules {
    action = "execute"
    action_parameters {
      id = "owasp_core_ruleset_id"
    }
    expression  = "true"
    description = "OWASP Core Ruleset"
    enabled     = true
  }
}
```

### 2. Integration with Rate Limiting

Layer DDoS protection with custom rate limiting rules.

```bash
# Create rate limiting rule for API
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rate_limits" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "match": {
      "request": {
        "url": "*.example.com/api/*"
      }
    },
    "threshold": 100,
    "period": 60,
    "action": {
      "mode": "challenge",
      "timeout": 86400
    },
    "description": "API rate limit - 100 requests per minute"
  }'
```

### 3. Integration with Load Balancing

Protect load-balanced endpoints from DDoS attacks.

```hcl
resource "cloudflare_load_balancer" "protected_lb" {
  zone_id          = var.zone_id
  name             = "protected-lb.example.com"
  default_pool_ids = [cloudflare_load_balancer_pool.main.id]
  
  # Enable DDoS protection
  session_affinity = "cookie"
  steering_policy  = "dynamic_latency"
  
  # Configure health checks
  proxied = true  # Required for DDoS protection
}

# DDoS protection for load balancer
resource "cloudflare_ruleset" "lb_ddos_protection" {
  zone_id = var.zone_id
  name    = "Load Balancer DDoS Protection"
  kind    = "zone"
  phase   = "http_request_firewall_managed"

  rules {
    action = "execute"
    action_parameters {
      id = "efb7b8c949ac4650a09736fc376e9aee"
      overrides {
        sensitivity_level = "high"
      }
    }
    expression  = "http.host eq \"protected-lb.example.com\""
    description = "DDoS protection for load balancer"
    enabled     = true
  }
}
```

### 4. Integration with Analytics and Monitoring

Export DDoS metrics to external monitoring systems.

```python
import requests
import json
from datetime import datetime, timedelta

class CloudflareDDoSMonitor:
    def __init__(self, api_token, zone_id, account_id):
        self.api_token = api_token
        self.zone_id = zone_id
        self.account_id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"
        
    def get_http_ddos_analytics(self, hours=24):
        """Fetch HTTP DDoS attack analytics"""
        until = datetime.utcnow()
        since = until - timedelta(hours=hours)
        
        url = f"{self.base_url}/zones/{self.zone_id}/analytics/ddos"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        params = {
            "since": since.isoformat() + "Z",
            "until": until.isoformat() + "Z"
        }
        
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def get_network_ddos_analytics(self, hours=24):
        """Fetch network-layer DDoS analytics"""
        until = datetime.utcnow()
        since = until - timedelta(hours=hours)
        
        url = f"{self.base_url}/accounts/{self.account_id}/analytics/network_analytics"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        params = {
            "since": since.isoformat() + "Z",
            "until": until.isoformat() + "Z",
            "dimensions": "datetime,attackType",
            "metrics": "bytesTotal,packetsTotal"
        }
        
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def check_active_attacks(self):
        """Check for active DDoS attacks"""
        data = self.get_http_ddos_analytics(hours=1)
        
        if data.get("success") and data.get("result"):
            attacks = data["result"].get("attacks", [])
            return len(attacks) > 0, attacks
        
        return False, []

# Usage
monitor = CloudflareDDoSMonitor(
    api_token="your_token",
    zone_id="your_zone_id",
    account_id="your_account_id"
)

active, attacks = monitor.check_active_attacks()
if active:
    print(f"Active attacks detected: {len(attacks)}")
    for attack in attacks:
        print(f"  - Type: {attack.get('type')}, Volume: {attack.get('volume')}")
```

## Best Practices

### 1. Sensitivity Configuration

- **Start with Medium**: Use medium sensitivity as baseline
- **Monitor False Positives**: Track legitimate traffic being blocked
- **Gradual Increases**: Increment sensitivity gradually based on attack patterns
- **Path-Specific Settings**: Use different sensitivities for different endpoints
- **Test Before Production**: Validate settings in staging environment

### 2. Rule Override Strategy

- **Minimal Overrides**: Only override rules when necessary
- **Document Changes**: Maintain clear documentation of all overrides
- **Regular Review**: Periodically review custom configurations
- **Version Control**: Track ruleset changes using Terraform or API logs

### 3. Monitoring and Alerting

- **Enable Notifications**: Configure alerts for DDoS events
- **Review Analytics**: Regularly check DDoS analytics dashboard
- **Trend Analysis**: Monitor attack patterns over time
- **Incident Response**: Develop playbooks for attack scenarios

### 4. Performance Optimization

- **Minimize Latency**: Balance protection with performance impact
- **Cache Aggressively**: Use caching to reduce origin load
- **Geographic Routing**: Route traffic through optimal data centers
- **Connection Pooling**: Maintain persistent connections where possible

### 5. Security Layering

- **Defense in Depth**: Combine DDoS with WAF, rate limiting, and bot management
- **Origin Protection**: Use Cloudflare Tunnel or restrict origin IPs
- **Certificate Validation**: Enforce TLS and validate certificates
- **Access Controls**: Implement IP allowlists/blocklists where appropriate

## Troubleshooting

### Issue: Legitimate Traffic Being Blocked

**Symptoms:**
- Increased customer complaints
- Higher error rates in analytics
- Specific user groups affected

**Solutions:**
```bash
# 1. Check recent DDoS events
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/analytics/ddos" \
  -H "Authorization: Bearer ${API_TOKEN}"

# 2. Lower sensitivity for affected paths
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [{
      "action": "execute",
      "action_parameters": {
        "id": "efb7b8c949ac4650a09736fc376e9aee",
        "overrides": {
          "sensitivity_level": "low"
        }
      },
      "expression": "http.request.uri.path contains \"/affected-path\"",
      "description": "Reduced sensitivity for legitimate traffic"
    }]
  }'

# 3. Add IP allowlist
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/firewall/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "expression": "ip.src in {203.0.113.0/24}"
    },
    "action": "allow",
    "description": "Allow trusted IP range"
  }'
```

### Issue: Attack Not Being Mitigated

**Symptoms:**
- Origin servers under load
- High bandwidth consumption
- Service degradation

**Solutions:**
```bash
# 1. Increase sensitivity
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [{
      "action": "execute",
      "action_parameters": {
        "id": "efb7b8c949ac4650a09736fc376e9aee",
        "overrides": {
          "sensitivity_level": "high"
        }
      },
      "expression": "true"
    }]
  }'

# 2. Enable Advanced TCP Protection
# Contact Cloudflare support to enable this feature

# 3. Implement additional rate limiting
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rate_limits" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "threshold": 50,
    "period": 60,
    "action": {"mode": "block"},
    "description": "Emergency rate limit"
  }'
```

### Issue: Configuration Not Taking Effect

**Symptoms:**
- API changes not reflected
- Dashboard shows old settings
- Unexpected behavior

**Solutions:**
```bash
# 1. Verify ruleset deployment
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/http_request_firewall_managed/entrypoint" \
  -H "Authorization: Bearer ${API_TOKEN}"

# 2. Check for conflicting rules
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets" \
  -H "Authorization: Bearer ${API_TOKEN}"

# 3. Clear cache and redeploy
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything": true}'
```

## See Also

- **[Cloudflare WAF](cloudflare-waf.md)** - Web Application Firewall for application security
- **[Cloudflare Zero Trust](cloudflare-zero-trust.md)** - Identity-aware access control
- **[Cloudflare Rate Limiting](cloudflare-rate-limiting.md)** - Request rate limiting and throttling
- **[Cloudflare Bot Management](cloudflare-bot-management.md)** - Bot detection and mitigation
- **[Cloudflare Load Balancing](cloudflare-load-balancing.md)** - Global load balancing and failover
- **[Cloudflare Analytics](cloudflare-analytics.md)** - Traffic analytics and insights
