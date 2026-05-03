---
name: Cloudflare DNS
description: >
  Manages Cloudflare DNS for authoritative DNS hosting, fast resolution, DNSSEC support, global redundancy, programmatic DNS management via API, and advanced DNS features.
  Invoke when asked to configure DNS records, set up domain nameservers, enable DNSSEC, manage DNS via API, implement DNS failover, configure DNS analytics, or optimize DNS resolution with Cloudflare.
license: MIT
---

# Cloudflare DNS

Cloudflare DNS is one of the world's fastest authoritative DNS services, offering free DNS hosting with a globally distributed anycast network. It provides sub-second DNS propagation, DNSSEC support, advanced analytics, and comprehensive API access for programmatic DNS management.

## When to Use

Use Cloudflare DNS when you need:

- **Fast DNS Resolution**: Sub-20ms query response times globally
- **Free Authoritative DNS**: No-cost DNS hosting for unlimited domains
- **DNSSEC Support**: Cryptographic authentication of DNS records
- **Global Redundancy**: Distributed across 300+ data centers
- **API Management**: Programmatic DNS record creation and updates
- **Analytics**: DNS query insights and traffic patterns
- **Advanced Features**: CNAME flattening, wildcard records, proxied DNS
- **DDoS Protection**: Built-in protection for DNS infrastructure
- **Secondary DNS**: Use as primary or secondary nameserver

**Don't use** if you need dynamic DNS updates from devices (use specialized DDNS services), complex DNS routing policies beyond what Cloudflare offers, or if you're locked into another DNS provider's proprietary features.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/dns/
- **DNS Records**: https://developers.cloudflare.com/dns/manage-dns-records/
- **DNSSEC**: https://developers.cloudflare.com/dns/dnssec/
- **API Reference**: https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
- **DNS Analytics**: https://developers.cloudflare.com/dns/dns-analytics/
- **CNAME Flattening**: https://developers.cloudflare.com/dns/cname-flattening/
- **Secondary DNS**: https://developers.cloudflare.com/dns/zone-setups/zone-transfers/
- **DNS Firewall**: https://developers.cloudflare.com/dns/dns-firewall/
- **Best Practices**: https://developers.cloudflare.com/dns/best-practices/
- **Troubleshooting**: https://developers.cloudflare.com/dns/troubleshooting/

## Quick Start

### Step 1: Add Domain to Cloudflare

```bash
# Via API
curl -X POST "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "example.com",
    "type": "full"
  }'

# Response includes zone_id and nameservers
# {
#   "result": {
#     "id": "zone_id_here",
#     "name": "example.com",
#     "name_servers": [
#       "eva.ns.cloudflare.com",
#       "hans.ns.cloudflare.com"
#     ]
#   }
# }
```

### Step 2: Update Nameservers at Registrar

Update your domain registrar to use Cloudflare's nameservers:
- `eva.ns.cloudflare.com`
- `hans.ns.cloudflare.com`

(Exact nameservers provided when adding domain)

### Step 3: Create DNS Records

```bash
# Create an A record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "example.com",
    "content": "192.0.2.1",
    "ttl": 3600,
    "proxied": true
  }'

# Create a CNAME record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "www",
    "content": "example.com",
    "ttl": 1,
    "proxied": true
  }'

# Create an MX record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "MX",
    "name": "example.com",
    "content": "mail.example.com",
    "priority": 10,
    "ttl": 3600
  }'
```

### Step 4: Verify DNS Resolution

```bash
# Check DNS propagation
dig @1.1.1.1 example.com

# Check all record types
dig @1.1.1.1 example.com ANY

# Verify DNSSEC
dig @1.1.1.1 example.com +dnssec

# Use Cloudflare's DNS checker
curl "https://1.1.1.1/dns-query?name=example.com&type=A" \
  -H "accept: application/dns-json"
```

## Core Features

### 1. DNS Record Management

Manage all standard DNS record types:

```bash
# A Record (IPv4)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "blog",
    "content": "203.0.113.1",
    "ttl": 3600,
    "proxied": false
  }'

# AAAA Record (IPv6)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "AAAA",
    "name": "www",
    "content": "2001:0db8::1",
    "ttl": 3600,
    "proxied": true
  }'

# TXT Record (SPF, DKIM, verification)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "TXT",
    "name": "example.com",
    "content": "v=spf1 include:_spf.google.com ~all",
    "ttl": 3600
  }'

# SRV Record (service discovery)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "SRV",
    "data": {
      "service": "_sip",
      "proto": "_tcp",
      "name": "example.com",
      "priority": 10,
      "weight": 60,
      "port": 5060,
      "target": "sipserver.example.com"
    }
  }'

# CAA Record (certificate authority authorization)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CAA",
    "name": "example.com",
    "data": {
      "flags": 0,
      "tag": "issue",
      "value": "letsencrypt.org"
    }
  }'
```

### 2. Bulk DNS Operations

```bash
# List all DNS records
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"

# Filter by type
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Search by name
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name=www.example.com" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Update a record
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "www",
    "content": "203.0.113.2",
    "ttl": 1,
    "proxied": true
  }'

# Delete a record
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### 3. DNSSEC Configuration

Enable cryptographic DNS authentication:

```bash
# Enable DNSSEC
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/dnssec" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "status": "active"
  }'

# Get DNSSEC details
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dnssec" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Response includes DS record to add at registrar:
# {
#   "result": {
#     "status": "active",
#     "ds": "example.com. 3600 IN DS 2371 13 2 ...",
#     "digest": "...",
#     "digest_type": "2",
#     "key_tag": 2371,
#     "algorithm": "13"
#   }
# }
```

Add the DS record at your domain registrar to complete DNSSEC setup.

### 4. Proxied vs DNS-Only Records

```bash
# Proxied (orange cloud) - traffic goes through Cloudflare
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "app",
    "content": "192.0.2.1",
    "proxied": true
  }'
# Benefits: CDN, DDoS protection, WAF, SSL
# IP shows Cloudflare's, not origin

# DNS-Only (gray cloud) - direct to origin
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "mail",
    "content": "192.0.2.2",
    "proxied": false
  }'
# Use for: mail servers, FTP, SSH, non-HTTP services
```

### 5. Wildcard Records

```bash
# Create wildcard record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "*.example.com",
    "content": "192.0.2.1",
    "ttl": 3600,
    "proxied": true
  }'

# Matches:
# - anything.example.com
# - subdomain.example.com
# - test.example.com
# Does NOT match:
# - example.com (needs separate record)
# - multi.level.example.com (use *.*.example.com)
```

## Common Use Cases

### Multi-Environment Setup

```bash
# Production
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "example.com",
    "content": "192.0.2.10",
    "proxied": true
  }'

# Staging
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "staging.example.com",
    "content": "192.0.2.20",
    "proxied": true
  }'

# Development
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "dev.example.com",
    "content": "192.0.2.30",
    "proxied": false
  }'
```

### Email Configuration

```bash
# MX Records
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "MX",
    "name": "example.com",
    "content": "mail1.example.com",
    "priority": 10,
    "ttl": 3600
  }'

# SPF Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "TXT",
    "name": "example.com",
    "content": "v=spf1 include:_spf.google.com include:spf.protection.outlook.com ~all",
    "ttl": 3600
  }'

# DKIM Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "TXT",
    "name": "default._domainkey",
    "content": "v=DKIM1; k=rsa; p=MIGfMA0GCS...",
    "ttl": 3600
  }'

# DMARC Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "TXT",
    "name": "_dmarc",
    "content": "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com",
    "ttl": 3600
  }'
```

### Subdomain Delegation

```bash
# Delegate subdomain to another nameserver
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "NS",
    "name": "subdomain",
    "content": "ns1.other-provider.com",
    "ttl": 3600
  }'

curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "NS",
    "name": "subdomain",
    "content": "ns2.other-provider.com",
    "ttl": 3600
  }'
```

### Dynamic DNS with Workers

```javascript
// Cloudflare Worker for DDNS
export default {
  async fetch(request, env) {
    // Authenticate request
    const authToken = request.headers.get('X-Auth-Token');
    if (authToken !== env.DDNS_SECRET) {
      return new Response('Unauthorized', { status: 401 });
    }

    const clientIP = request.headers.get('CF-Connecting-IP');
    const hostname = new URL(request.url).searchParams.get('hostname');

    if (!hostname) {
      return new Response('Missing hostname parameter', { status: 400 });
    }

    // Get existing DNS record
    const listResponse = await fetch(
      `https://api.cloudflare.com/client/v4/zones/${env.ZONE_ID}/dns_records?name=${hostname}`,
      {
        headers: {
          'Authorization': `Bearer ${env.CF_API_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const records = await listResponse.json();
    const record = records.result?.[0];

    if (!record) {
      return new Response('Record not found', { status: 404 });
    }

    // Update if IP changed
    if (record.content !== clientIP) {
      const updateResponse = await fetch(
        `https://api.cloudflare.com/client/v4/zones/${env.ZONE_ID}/dns_records/${record.id}`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${env.CF_API_TOKEN}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            type: 'A',
            name: hostname,
            content: clientIP,
            ttl: 120,
            proxied: false,
          }),
        }
      );

      const result = await updateResponse.json();
      
      if (result.success) {
        return new Response(`Updated ${hostname} to ${clientIP}`);
      } else {
        return new Response('Update failed', { status: 500 });
      }
    }

    return new Response(`No update needed. ${hostname} -> ${clientIP}`);
  }
};
```

### DNS-Based Load Balancing

```bash
# Create multiple A records with same name (round-robin)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "app.example.com",
    "content": "192.0.2.1",
    "ttl": 300,
    "proxied": false
  }'

curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "app.example.com",
    "content": "192.0.2.2",
    "ttl": 300,
    "proxied": false
  }'

# For intelligent load balancing, use Cloudflare Load Balancing product
```

## Integration

### Terraform Provider

```hcl
# Configure Cloudflare provider
terraform {
  required_providers {
    cloudflare = {
      source = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# Create DNS records
resource "cloudflare_record" "www" {
  zone_id = var.zone_id
  name    = "www"
  value   = "192.0.2.1"
  type    = "A"
  ttl     = 3600
  proxied = true
}

resource "cloudflare_record" "api" {
  zone_id = var.zone_id
  name    = "api"
  value   = "api-backend.example.com"
  type    = "CNAME"
  ttl     = 1
  proxied = true
}

resource "cloudflare_record" "mx" {
  zone_id  = var.zone_id
  name     = "@"
  value    = "mail.example.com"
  type     = "MX"
  priority = 10
  ttl      = 3600
}

# Enable DNSSEC
resource "cloudflare_zone_dnssec" "example" {
  zone_id = var.zone_id
}
```

### Python SDK

```python
import CloudFlare

# Initialize client
cf = CloudFlare.CloudFlare(token='YOUR_API_TOKEN')

# Get zone ID
zones = cf.zones.get(params={'name': 'example.com'})
zone_id = zones[0]['id']

# Create DNS record
dns_record = {
    'name': 'blog',
    'type': 'A',
    'content': '192.0.2.1',
    'ttl': 3600,
    'proxied': True
}
result = cf.zones.dns_records.post(zone_id, data=dns_record)
print(f"Created record: {result['id']}")

# List all records
records = cf.zones.dns_records.get(zone_id)
for record in records:
    print(f"{record['name']}: {record['type']} -> {record['content']}")

# Update record
record_id = 'record_id_here'
updated_record = {
    'name': 'blog',
    'type': 'A',
    'content': '203.0.113.1',
    'ttl': 1,
    'proxied': True
}
cf.zones.dns_records.put(zone_id, record_id, data=updated_record)

# Delete record
cf.zones.dns_records.delete(zone_id, record_id)

# Enable DNSSEC
cf.zones.dnssec.patch(zone_id, data={'status': 'active'})
```

### Node.js SDK

```javascript
const Cloudflare = require('cloudflare');

const cf = new Cloudflare({
  token: 'YOUR_API_TOKEN'
});

const zoneId = 'your_zone_id';

// Create DNS record
async function createRecord() {
  const record = await cf.dnsRecords.add(zoneId, {
    type: 'A',
    name: 'api',
    content: '192.0.2.1',
    ttl: 3600,
    proxied: true
  });
  console.log('Created:', record.id);
}

// List all DNS records
async function listRecords() {
  const records = await cf.dnsRecords.browse(zoneId);
  records.result.forEach(record => {
    console.log(`${record.name}: ${record.type} -> ${record.content}`);
  });
}

// Update DNS record
async function updateRecord(recordId) {
  await cf.dnsRecords.edit(zoneId, recordId, {
    type: 'A',
    name: 'api',
    content: '203.0.113.1',
    ttl: 1,
    proxied: true
  });
}

// Delete DNS record
async function deleteRecord(recordId) {
  await cf.dnsRecords.del(zoneId, recordId);
}

// Bulk operations
async function bulkUpdate() {
  const records = await cf.dnsRecords.browse(zoneId, { type: 'A' });
  
  for (const record of records.result) {
    if (record.content === '192.0.2.1') {
      await cf.dnsRecords.edit(zoneId, record.id, {
        ...record,
        content: '203.0.113.1'
      });
    }
  }
}
```

### GitHub Actions Integration

```yaml
name: Update DNS

on:
  push:
    branches: [main]

jobs:
  update-dns:
    runs-on: ubuntu-latest
    steps:
      - name: Update staging DNS
        run: |
          RECORD_ID=$(curl -X GET \
            "https://api.cloudflare.com/client/v4/zones/${{ secrets.ZONE_ID }}/dns_records?name=staging.example.com" \
            -H "Authorization: Bearer ${{ secrets.CF_API_TOKEN }}" \
            -H "Content-Type: application/json" | jq -r '.result[0].id')
          
          curl -X PUT \
            "https://api.cloudflare.com/client/v4/zones/${{ secrets.ZONE_ID }}/dns_records/$RECORD_ID" \
            -H "Authorization: Bearer ${{ secrets.CF_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            --data '{
              "type": "A",
              "name": "staging",
              "content": "${{ secrets.NEW_IP }}",
              "ttl": 300,
              "proxied": true
            }'
```

## Best Practices

### 1. Use Appropriate TTL Values

```bash
# Short TTL (300s) for frequently changing records
# Good for: Blue/green deployments, failover testing
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  --data '{"type":"A","name":"canary","content":"192.0.2.1","ttl":300}'

# Auto TTL (1) for proxied records (Cloudflare optimizes)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  --data '{"type":"A","name":"www","content":"192.0.2.1","ttl":1,"proxied":true}'

# Long TTL (86400s) for static records
# Good for: Mail servers, rarely-changing infrastructure
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  --data '{"type":"MX","name":"@","content":"mail.example.com","priority":10,"ttl":86400}'
```

### 2. Implement DNS Record Validation

```python
import ipaddress
import re

def validate_dns_record(record_type, content):
    """Validate DNS record content before creation"""
    
    if record_type == 'A':
        try:
            ipaddress.IPv4Address(content)
            return True
        except ValueError:
            return False
    
    elif record_type == 'AAAA':
        try:
            ipaddress.IPv6Address(content)
            return True
        except ValueError:
            return False
    
    elif record_type == 'CNAME':
        # Valid domain name
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]{2,}$'
        return bool(re.match(pattern, content))
    
    elif record_type == 'TXT':
        # TXT records have max length
        return len(content) <= 255
    
    return True

# Use before creating records
if validate_dns_record('A', '192.0.2.1'):
    # Create record
    pass
```

### 3. Monitor DNS Changes

```bash
# Export DNS records for backup
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" | \
  jq '.result' > dns_backup_$(date +%Y%m%d).json

# Compare before/after changes
diff dns_backup_before.json dns_backup_after.json
```

### 4. Use DNS Record Comments (Enterprise)

```bash
# Add comments to track changes
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "temp-service",
    "content": "192.0.2.50",
    "comment": "Temporary service for Q4 campaign - Remove after Dec 31"
  }'
```

### 5. Implement Gradual DNS Migration

```bash
# Step 1: Lower TTL on old records (24-48 hours before migration)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  --data '{"ttl":300}'

# Step 2: Update to new IP
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  --data '{"content":"NEW_IP","ttl":300}'

# Step 3: Monitor for 24 hours

# Step 4: Increase TTL back to normal
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  --data '{"ttl":3600}'
```

## Troubleshooting

### DNS Not Resolving

```bash
# Check nameserver delegation
dig example.com NS

# Should return Cloudflare nameservers
# If not, update at registrar

# Check specific record
dig @1.1.1.1 www.example.com

# Verify DNSSEC
dig @1.1.1.1 example.com +dnssec

# Check from multiple locations
for ns in 1.1.1.1 8.8.8.8 9.9.9.9; do
  echo "Checking $ns:"
  dig @$ns example.com +short
done
```

### Slow DNS Propagation

```bash
# Check current TTL
dig example.com | grep -i ttl

# Lower TTL before making changes
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  --data '{"ttl":60}'

# Wait for old TTL to expire before updating content
```

### DNSSEC Validation Failures

```bash
# Verify DNSSEC configuration
dig example.com +dnssec +multi

# Check for DS record at parent
dig example.com DS +trace

# Validate DNSSEC chain
delv @1.1.1.1 example.com

# If broken, disable and re-enable DNSSEC
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/dnssec" \
  --data '{"status":"disabled"}'
  
# Wait 24 hours, then re-enable
```

### API Rate Limiting

```python
import time
import requests

def create_records_with_backoff(records, zone_id, api_token):
    """Create DNS records with exponential backoff"""
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    for record in records:
        retries = 0
        max_retries = 5
        
        while retries < max_retries:
            response = requests.post(
                f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
                headers=headers,
                json=record
            )
            
            if response.status_code == 429:
                # Rate limited
                wait_time = 2 ** retries
                print(f'Rate limited. Waiting {wait_time}s...')
                time.sleep(wait_time)
                retries += 1
            elif response.status_code == 200:
                print(f'Created: {record["name"]}')
                break
            else:
                print(f'Error: {response.text}')
                break
        
        # Small delay between requests
        time.sleep(0.1)
```

## See Also

- **Cloudflare Load Balancing**: https://developers.cloudflare.com/load-balancing/
- **Cloudflare Pages**: https://developers.cloudflare.com/pages/
- **Cloudflare Workers**: https://developers.cloudflare.com/workers/
- **DNS Firewall**: https://developers.cloudflare.com/dns/dns-firewall/
- **1.1.1.1 Resolver**: https://developers.cloudflare.com/1.1.1.1/
- **Cloudflare API**: https://developers.cloudflare.com/api/
- **Zone Versioning**: https://developers.cloudflare.com/dns/zone-versioning/
- **Secondary DNS**: https://developers.cloudflare.com/dns/zone-setups/zone-transfers/
