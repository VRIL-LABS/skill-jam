---
name: Cloudflare Email Routing
description: Configure Cloudflare Email Routing for email forwarding and routing with custom addresses, spam protection, and API management. Route emails to multiple destinations with powerful filtering rules. Trigger phrases include "email routing", "email forwarding", "custom email addresses", "email spam protection", and "route emails".
license: MIT
---

# Cloudflare Email Routing

Cloudflare Email Routing enables you to create custom email addresses for your domain and route incoming messages to your preferred destinations. It provides built-in spam protection, flexible routing rules, and easy management through dashboard or API, all without requiring email hosting infrastructure.

## When to Use

Use Cloudflare Email Routing when you need to:

- **Create professional email addresses** using your custom domain
- **Forward emails** from custom addresses to existing mailboxes
- **Route emails** based on patterns and conditions
- **Protect against spam** with Cloudflare's email security
- **Simplify email management** without managing email servers
- **Create catch-all addresses** for your domain
- **Handle multiple destinations** for the same email address
- **Implement email aliases** for different purposes
- **Enable team email addresses** without individual mailboxes
- **Receive emails** at your domain without email hosting costs

Cloudflare Email Routing is ideal for individuals, small businesses, and organizations that need professional email addresses without the complexity and cost of traditional email hosting.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/email-routing/
- **Get Started**: https://developers.cloudflare.com/email-routing/get-started/
- **Email Workers**: https://developers.cloudflare.com/email-routing/email-workers/
- **Routing Rules**: https://developers.cloudflare.com/email-routing/setup/email-routing-addresses/
- **API Reference**: https://developers.cloudflare.com/api/operations/email-routing-routing-rules-list-routing-rules
- **Troubleshooting**: https://developers.cloudflare.com/email-routing/troubleshooting/
- **Limits**: https://developers.cloudflare.com/email-routing/limits/

## Quick Start

### Prerequisites

1. **Domain on Cloudflare**: Your domain must be active on Cloudflare
2. **Valid MX Records**: Cloudflare will configure MX records for you
3. **Verified Destination**: At least one verified email destination

### Enable Email Routing

**Via Dashboard:**

1. **Navigate to Email Routing**
   ```
   Log in to Cloudflare Dashboard
   Select your domain
   Go to Email > Email Routing
   Click "Get started" or "Enable Email Routing"
   ```

2. **Configure DNS Records**
   ```
   Cloudflare automatically adds required MX records:
   - MX record: route1.mx.cloudflare.net (priority 46)
   - MX record: route2.mx.cloudflare.net (priority 86)
   - MX record: route3.mx.cloudflare.net (priority 13)
   - TXT record: v=spf1 include:_spf.mx.cloudflare.net ~all
   ```

3. **Add Destination Address**
   ```
   Enter your existing email address (e.g., user@gmail.com)
   Click "Send verification email"
   Open the verification email and click the link
   ```

4. **Create Routing Rules**
   ```
   Define source addresses (e.g., info@example.com)
   Select destination address
   Save the rule
   ```

### Via API

**Enable Email Routing:**

```bash
ZONE_ID="your_zone_id"
API_TOKEN="your_api_token"

# Enable Email Routing for zone
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/enable" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json"

# Check status
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing" \
  -H "Authorization: Bearer ${API_TOKEN}"
```

**Add Destination Address:**

```bash
# Create destination email
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/email/routing/addresses" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@gmail.com"
  }'

# The API returns a verification token
# User must verify by clicking link in email
```

**Create Routing Rule:**

```bash
# Create forwarding rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "type": "forward",
        "value": ["user@gmail.com"]
      }
    ],
    "matchers": [
      {
        "type": "literal",
        "field": "to",
        "value": "info@example.com"
      }
    ],
    "enabled": true,
    "name": "Forward info@example.com",
    "priority": 0
  }'
```

### Test Email Routing

```bash
# Send a test email
echo "This is a test email" | mail -s "Test Email Routing" info@example.com

# Check if email was delivered to destination
# Check your destination inbox (e.g., user@gmail.com)
```

## Core Features

### 1. Custom Email Addresses

Create professional email addresses using your domain.

**Simple Forwarding:**
```bash
# Forward sales@example.com to personal email
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": ["sales-team@gmail.com"]
    }],
    "matchers": [{
      "type": "literal",
      "field": "to",
      "value": "sales@example.com"
    }],
    "enabled": true,
    "name": "Sales Email",
    "priority": 0
  }'
```

**Multiple Destinations:**
```bash
# Forward support@example.com to multiple addresses
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": [
        "support-1@company.com",
        "support-2@company.com",
        "support-backup@company.com"
      ]
    }],
    "matchers": [{
      "type": "literal",
      "field": "to",
      "value": "support@example.com"
    }],
    "enabled": true,
    "name": "Support Team Distribution"
  }'
```

**Terraform Configuration:**
```hcl
# Destination addresses
resource "cloudflare_email_routing_address" "personal" {
  account_id = var.account_id
  email      = "user@gmail.com"
}

resource "cloudflare_email_routing_address" "work" {
  account_id = var.account_id
  email      = "user@company.com"
}

# Routing rule
resource "cloudflare_email_routing_rule" "info" {
  zone_id = var.zone_id
  name    = "Info Email"
  enabled = true
  
  matcher {
    type  = "literal"
    field = "to"
    value = "info@example.com"
  }
  
  action {
    type  = "forward"
    value = [cloudflare_email_routing_address.personal.email]
  }
  
  priority = 0
}
```

### 2. Pattern-Based Routing

Route emails based on patterns and wildcards.

**Wildcard Routing:**
```bash
# Route all team-* emails to a group address
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": ["team-inbox@company.com"]
    }],
    "matchers": [{
      "type": "literal",
      "field": "to",
      "value": "team-*@example.com"
    }],
    "enabled": true,
    "name": "Team Email Pattern"
  }'
```

**Catch-All Address:**
```bash
# Forward all unmatched emails to catch-all
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": ["catchall@gmail.com"]
    }],
    "matchers": [{
      "type": "all"
    }],
    "enabled": true,
    "name": "Catch-All",
    "priority": 999
  }'
```

**Terraform Catch-All:**
```hcl
resource "cloudflare_email_routing_catch_all" "default" {
  zone_id = var.zone_id
  name    = "Catch-all routing"
  enabled = true
  
  matcher {
    type = "all"
  }
  
  action {
    type  = "forward"
    value = ["admin@company.com"]
  }
}
```

### 3. Advanced Routing Rules

Complex routing logic with multiple conditions.

**Department-Based Routing:**
```bash
# Route based on department prefixes
# sales-* -> sales team
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": ["sales@company.com"]
    }],
    "matchers": [{
      "type": "literal",
      "field": "to",
      "value": "sales-*@example.com"
    }],
    "enabled": true,
    "name": "Sales Department",
    "priority": 1
  }'

# engineering-* -> engineering team
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": ["engineering@company.com"]
    }],
    "matchers": [{
      "type": "literal",
      "field": "to",
      "value": "engineering-*@example.com"
    }],
    "enabled": true,
    "name": "Engineering Department",
    "priority": 2
  }'
```

**Priority-Based Routing:**
```hcl
# High priority for specific addresses
resource "cloudflare_email_routing_rule" "ceo" {
  zone_id  = var.zone_id
  name     = "CEO Email"
  enabled  = true
  priority = 0  # Highest priority
  
  matcher {
    type  = "literal"
    field = "to"
    value = "ceo@example.com"
  }
  
  action {
    type  = "forward"
    value = ["ceo@personal.com", "assistant@company.com"]
  }
}

# Lower priority for general inquiries
resource "cloudflare_email_routing_rule" "contact" {
  zone_id  = var.zone_id
  name     = "Contact Form"
  enabled  = true
  priority = 10
  
  matcher {
    type  = "literal"
    field = "to"
    value = "contact@example.com"
  }
  
  action {
    type  = "forward"
    value = ["inbox@company.com"]
  }
}
```

### 4. Email Workers

Process emails with custom logic using Cloudflare Workers.

**Basic Email Worker:**
```javascript
// email-worker.js
export default {
  async email(message, env, ctx) {
    // Log email details
    console.log('From:', message.from);
    console.log('To:', message.to);
    console.log('Subject:', message.headers.get('subject'));
    
    // Forward to destination
    await message.forward('destination@example.com');
  }
}
```

**Email Parser Worker:**
```javascript
// Parse and route based on content
export default {
  async email(message, env, ctx) {
    const subject = message.headers.get('subject') || '';
    const from = message.from;
    
    // Route based on subject
    if (subject.toLowerCase().includes('urgent')) {
      await message.forward('urgent@company.com');
    } else if (subject.toLowerCase().includes('invoice')) {
      await message.forward('billing@company.com');
    } else {
      await message.forward('general@company.com');
    }
    
    // Log to analytics
    await fetch('https://analytics.example.com/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: from,
        subject: subject,
        timestamp: new Date().toISOString()
      })
    });
  }
}
```

**Auto-Reply Worker:**
```javascript
// Send automatic replies
export default {
  async email(message, env, ctx) {
    const from = message.from;
    const subject = message.headers.get('subject');
    
    // Forward original message
    await message.forward('support@company.com');
    
    // Send auto-reply
    const reply = new EmailMessage(
      'noreply@example.com',
      from,
      `Re: ${subject}`
    );
    
    reply.setBody(`
      Thank you for contacting us!
      
      We have received your message and will respond within 24 hours.
      
      Best regards,
      Support Team
    `);
    
    await reply.send();
  }
}
```

**Spam Filter Worker:**
```javascript
// Custom spam filtering
export default {
  async email(message, env, ctx) {
    const from = message.from;
    const subject = message.headers.get('subject') || '';
    const body = await streamToString(message.raw);
    
    // Check spam indicators
    const spamKeywords = ['viagra', 'lottery', 'prince', 'inheritance'];
    const isSpam = spamKeywords.some(keyword => 
      subject.toLowerCase().includes(keyword) ||
      body.toLowerCase().includes(keyword)
    );
    
    if (isSpam) {
      // Drop spam
      message.setReject('Spam detected');
    } else {
      // Forward legitimate email
      await message.forward('inbox@example.com');
    }
  }
}

async function streamToString(stream) {
  const chunks = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf-8');
}
```

**Deploy Email Worker:**
```bash
# Create worker
cat > wrangler.toml <<EOF
name = "email-router"
main = "src/index.js"
compatibility_date = "2024-01-01"

[[routes]]
pattern = "example.com/*"
zone_name = "example.com"
EOF

# Deploy
npx wrangler deploy

# Bind to email routing
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "worker",
      "value": ["email-router"]
    }],
    "matchers": [{
      "type": "all"
    }],
    "enabled": true,
    "name": "Email Worker Processing"
  }'
```

### 5. Spam Protection

Built-in spam filtering and security features.

**Automatic Spam Filtering:**
- SPF verification
- DKIM validation
- DMARC compliance
- Reputation-based filtering
- Content analysis

**Check SPF/DKIM Configuration:**
```bash
# Verify SPF record
dig TXT example.com | grep spf

# Should include:
# v=spf1 include:_spf.mx.cloudflare.net ~all

# Check DKIM
dig TXT default._domainkey.example.com

# Verify DMARC
dig TXT _dmarc.example.com
```

**Configure DMARC:**
```bash
# Add DMARC record via API
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TXT",
    "name": "_dmarc",
    "content": "v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@example.com; ruf=mailto:dmarc-failures@example.com; pct=100",
    "ttl": 3600
  }'
```

**Terraform DMARC Configuration:**
```hcl
resource "cloudflare_record" "dmarc" {
  zone_id = var.zone_id
  name    = "_dmarc"
  type    = "TXT"
  value   = "v=DMARC1; p=reject; rua=mailto:dmarc@example.com; fo=1"
  ttl     = 3600
}

resource "cloudflare_record" "spf" {
  zone_id = var.zone_id
  name    = "@"
  type    = "TXT"
  value   = "v=spf1 include:_spf.mx.cloudflare.net ~all"
  ttl     = 3600
}
```

## Common Use Cases

### 1. Small Business Email Setup

Professional emails for a small business without email hosting.

```hcl
# Destination addresses for team members
resource "cloudflare_email_routing_address" "owner" {
  account_id = var.account_id
  email      = "owner@personal.com"
}

resource "cloudflare_email_routing_address" "manager" {
  account_id = var.account_id
  email      = "manager@personal.com"
}

# Business email addresses
resource "cloudflare_email_routing_rule" "info" {
  zone_id  = var.zone_id
  name     = "General Inquiries"
  enabled  = true
  priority = 0
  
  matcher {
    type  = "literal"
    field = "to"
    value = "info@mybusiness.com"
  }
  
  action {
    type  = "forward"
    value = [
      cloudflare_email_routing_address.owner.email,
      cloudflare_email_routing_address.manager.email
    ]
  }
}

resource "cloudflare_email_routing_rule" "sales" {
  zone_id  = var.zone_id
  name     = "Sales Inquiries"
  enabled  = true
  priority = 1
  
  matcher {
    type  = "literal"
    field = "to"
    value = "sales@mybusiness.com"
  }
  
  action {
    type  = "forward"
    value = [cloudflare_email_routing_address.owner.email]
  }
}

resource "cloudflare_email_routing_rule" "support" {
  zone_id  = var.zone_id
  name     = "Customer Support"
  enabled  = true
  priority = 2
  
  matcher {
    type  = "literal"
    field = "to"
    value = "support@mybusiness.com"
  }
  
  action {
    type  = "forward"
    value = [cloudflare_email_routing_address.manager.email]
  }
}

# Catch-all for typos
resource "cloudflare_email_routing_catch_all" "default" {
  zone_id = var.zone_id
  name    = "Catch All"
  enabled = true
  
  matcher {
    type = "all"
  }
  
  action {
    type  = "forward"
    value = [cloudflare_email_routing_address.owner.email]
  }
}
```

### 2. Personal Domain Email Aliases

Create multiple aliases for different purposes.

```bash
# Personal inbox
DESTINATION="me@gmail.com"

# Professional alias
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"actions\": [{\"type\": \"forward\", \"value\": [\"${DESTINATION}\"]}],
    \"matchers\": [{\"type\": \"literal\", \"field\": \"to\", \"value\": \"professional@mydomain.com\"}],
    \"enabled\": true,
    \"name\": \"Professional\"
  }"

# Shopping alias (for online purchases)
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"actions\": [{\"type\": \"forward\", \"value\": [\"${DESTINATION}\"]}],
    \"matchers\": [{\"type\": \"literal\", \"field\": \"to\", \"value\": \"shopping@mydomain.com\"}],
    \"enabled\": true,
    \"name\": \"Shopping\"
  }"

# Newsletter alias
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"actions\": [{\"type\": \"forward\", \"value\": [\"${DESTINATION}\"]}],
    \"matchers\": [{\"type\": \"literal\", \"field\": \"to\", \"value\": \"newsletters@mydomain.com\"}],
    \"enabled\": true,
    \"name\": \"Newsletters\"
  }"

# Per-service aliases (track who sells your email)
for service in amazon facebook twitter linkedin; do
  curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
      \"actions\": [{\"type\": \"forward\", \"value\": [\"${DESTINATION}\"]}],
      \"matchers\": [{\"type\": \"literal\", \"field\": \"to\", \"value\": \"${service}@mydomain.com\"}],
      \"enabled\": true,
      \"name\": \"${service^}\"
    }"
done
```

### 3. Project-Based Email Management

Separate email addresses for different projects.

```hcl
# Project A
resource "cloudflare_email_routing_rule" "project_a" {
  zone_id  = var.zone_id
  name     = "Project A"
  enabled  = true
  
  matcher {
    type  = "literal"
    field = "to"
    value = "project-a@example.com"
  }
  
  action {
    type  = "forward"
    value = [
      "project-a-lead@company.com",
      "team-shared@company.com"
    ]
  }
}

# Project B
resource "cloudflare_email_routing_rule" "project_b" {
  zone_id  = var.zone_id
  name     = "Project B"
  enabled  = true
  
  matcher {
    type  = "literal"
    field = "to"
    value = "project-b@example.com"
  }
  
  action {
    type  = "forward"
    value = ["project-b-lead@company.com"]
  }
}

# All project emails with wildcard
resource "cloudflare_email_routing_rule" "all_projects" {
  zone_id  = var.zone_id
  name     = "All Projects"
  enabled  = true
  priority = 50
  
  matcher {
    type  = "literal"
    field = "to"
    value = "project-*@example.com"
  }
  
  action {
    type  = "forward"
    value = ["pm-team@company.com"]
  }
}
```

### 4. Newsletter and Mailing List

Manage newsletter subscriptions with dedicated addresses.

```javascript
// Email Worker for newsletter management
export default {
  async email(message, env, ctx) {
    const to = message.to;
    const from = message.from;
    const subject = message.headers.get('subject') || '';
    
    // Check if it's a subscribe/unsubscribe request
    if (subject.toLowerCase().includes('subscribe')) {
      // Add to mailing list (KV or external service)
      await env.SUBSCRIBERS.put(from, JSON.stringify({
        email: from,
        subscribed: true,
        date: new Date().toISOString()
      }));
      
      // Send confirmation
      await sendConfirmation(from, 'subscribed');
      
    } else if (subject.toLowerCase().includes('unsubscribe')) {
      // Remove from list
      await env.SUBSCRIBERS.delete(from);
      
      // Send confirmation
      await sendConfirmation(from, 'unsubscribed');
      
    } else {
      // Forward to newsletter team
      await message.forward('newsletter-team@company.com');
    }
  }
}

async function sendConfirmation(to, action) {
  // Implementation to send confirmation email
  console.log(`Sent ${action} confirmation to ${to}`);
}
```

### 5. Support Ticket System Integration

Route support emails to ticketing system.

```javascript
// Forward to ticketing system API
export default {
  async email(message, env, ctx) {
    const from = message.from;
    const subject = message.headers.get('subject') || 'No Subject';
    const body = await streamToArrayBuffer(message.raw);
    
    // Create ticket in system (e.g., Zendesk, Freshdesk)
    const ticket = await fetch('https://api.ticketsystem.com/v1/tickets', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.TICKET_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        requester: { email: from },
        subject: subject,
        description: body.toString(),
        priority: 'normal',
        status: 'open',
        tags: ['email-routing']
      })
    });
    
    const ticketData = await ticket.json();
    
    // Send auto-reply with ticket number
    const reply = `
      Thank you for contacting support!
      
      Your ticket #${ticketData.id} has been created.
      We will respond within 24 hours.
      
      Support Team
    `;
    
    // Send confirmation (implementation depends on email service)
    console.log(`Created ticket ${ticketData.id} for ${from}`);
  }
}

async function streamToArrayBuffer(stream) {
  const chunks = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}
```

## Integration

### 1. Integration with External Email Services

Forward to Gmail, Outlook, or other providers.

**Gmail Integration:**
```bash
# Add Gmail as destination
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/email/routing/addresses" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@gmail.com"
  }'

# Create forwarding rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [{
      "type": "forward",
      "value": ["user@gmail.com"]
    }],
    "matchers": [{
      "type": "literal",
      "field": "to",
      "value": "me@example.com"
    }],
    "enabled": true,
    "name": "Forward to Gmail"
  }'
```

**ProtonMail Integration:**
```hcl
resource "cloudflare_email_routing_address" "protonmail" {
  account_id = var.account_id
  email      = "user@protonmail.com"
}

resource "cloudflare_email_routing_rule" "secure_email" {
  zone_id = var.zone_id
  name    = "Secure Email to ProtonMail"
  enabled = true
  
  matcher {
    type  = "literal"
    field = "to"
    value = "secure@example.com"
  }
  
  action {
    type  = "forward"
    value = [cloudflare_email_routing_address.protonmail.email]
  }
}
```

### 2. Integration with CRM Systems

Forward emails to CRM for lead tracking.

```javascript
// Email to Salesforce
export default {
  async email(message, env, ctx) {
    const from = message.from;
    const subject = message.headers.get('subject');
    const body = await getEmailBody(message);
    
    // Create lead in Salesforce
    await fetch('https://api.salesforce.com/services/data/v55.0/sobjects/Lead', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.SF_ACCESS_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        FirstName: parseFirstName(from),
        LastName: parseLastName(from),
        Email: from,
        Company: 'Unknown',
        Description: `Email Subject: ${subject}\n\n${body}`,
        LeadSource: 'Email',
        Status: 'Open - Not Contacted'
      })
    });
    
    // Also forward to sales team
    await message.forward('sales@company.com');
  }
}
```

### 3. Integration with Analytics

Track email metrics and engagement.

```javascript
// Email analytics tracking
export default {
  async email(message, env, ctx) {
    const from = message.from;
    const to = message.to;
    const subject = message.headers.get('subject');
    
    // Log to analytics service
    await fetch('https://analytics.example.com/api/email-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: 'email_received',
        from: from,
        to: to,
        subject: subject,
        timestamp: new Date().toISOString(),
        user_agent: message.headers.get('user-agent'),
        size: message.size
      })
    });
    
    // Store in Cloudflare Analytics Engine
    if (env.EMAIL_ANALYTICS) {
      env.EMAIL_ANALYTICS.writeDataPoint({
        indexes: [to],
        blobs: [from, subject],
        doubles: [message.size]
      });
    }
    
    // Forward email
    await message.forward('inbox@example.com');
  }
}
```

### 4. Integration with Slack/Discord

Send notifications for important emails.

```javascript
// Slack notification for important emails
export default {
  async email(message, env, ctx) {
    const from = message.from;
    const subject = message.headers.get('subject');
    const to = message.to;
    
    // Check if email is important
    const isImportant = 
      subject.toLowerCase().includes('urgent') ||
      subject.toLowerCase().includes('important') ||
      to === 'ceo@example.com';
    
    if (isImportant) {
      // Send Slack notification
      await fetch(env.SLACK_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: '📧 Important Email Received',
          blocks: [
            {
              type: 'section',
              text: {
                type: 'mrkdwn',
                text: `*From:* ${from}\n*To:* ${to}\n*Subject:* ${subject}`
              }
            }
          ]
        })
      });
    }
    
    // Forward email
    await message.forward('inbox@example.com');
  }
}
```

## Best Practices

### 1. Email Organization

- **Use Descriptive Names**: Create clear, purposeful email addresses
- **Implement Wildcards Wisely**: Use patterns for scalability
- **Set Priorities Correctly**: Order rules from specific to general
- **Document Routing Logic**: Maintain documentation of email flows
- **Regular Audits**: Review and clean up unused addresses

### 2. Security

- **Verify All Destinations**: Always verify destination addresses
- **Enable SPF/DKIM/DMARC**: Implement email authentication
- **Monitor Spam Levels**: Track rejected and suspicious emails
- **Use Email Workers for Validation**: Add custom security checks
- **Limit Catch-All Usage**: Be cautious with catch-all addresses

### 3. Deliverability

- **Configure DNS Properly**: Ensure MX records are correct
- **Maintain Sender Reputation**: Monitor email sending patterns
- **Avoid Forwarding Spam**: Implement spam filtering
- **Test Email Flow**: Regularly test routing rules
- **Monitor Bounce Rates**: Track delivery failures

### 4. Management

- **Use Infrastructure as Code**: Manage with Terraform/API
- **Version Control**: Track changes to routing configuration
- **Environment Separation**: Different rules for dev/prod
- **Access Control**: Limit who can modify routing rules
- **Backup Configuration**: Export and backup routing rules

### 5. Performance

- **Optimize Worker Logic**: Keep workers fast and efficient
- **Minimize External API Calls**: Cache where possible
- **Set Appropriate TTLs**: Configure DNS TTLs for performance
- **Monitor Quota Usage**: Track against Email Routing limits
- **Use Batch Operations**: Process multiple emails efficiently

## Troubleshooting

### Issue: Emails Not Being Received

**Symptoms:**
- Emails sent but not arriving at destination
- No delivery errors shown
- MX records appear correct

**Solutions:**
```bash
# Verify MX records
dig MX example.com

# Should show Cloudflare MX records:
# route1.mx.cloudflare.net (priority 46)
# route2.mx.cloudflare.net (priority 86)
# route3.mx.cloudflare.net (priority 13)

# Check Email Routing status
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Verify destination is verified
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/email/routing/addresses" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Check routing rules
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/rules" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Test with email sending
echo "Test message" | mail -s "Test" youraddress@example.com
```

### Issue: Destination Email Not Verified

**Symptoms:**
- Verification email not received
- Cannot add destination address
- Routing rule not working

**Solutions:**
```bash
# Resend verification email
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/email/routing/addresses/${ADDRESS_ID}/verify" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Check spam folder in destination email
# Check if domain allows emails from Cloudflare
# Try different email provider

# List addresses to check status
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/email/routing/addresses" \
  -H "Authorization: Bearer ${API_TOKEN}"
```

### Issue: Emails Marked as Spam

**Symptoms:**
- Forwarded emails going to spam
- Low sender reputation
- DMARC failures

**Solutions:**
```bash
# Verify SPF record
dig TXT example.com | grep spf

# Add/update DMARC record
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TXT",
    "name": "_dmarc",
    "content": "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com",
    "ttl": 3600
  }'

# Check email headers for authentication results
# Review sender reputation at https://www.senderscore.org/
# Ensure destination provider allows forwarded emails
```

### Issue: Catch-All Receiving Too Much Spam

**Symptoms:**
- Excessive spam emails
- Destination inbox overwhelmed
- Unwanted mail flooding

**Solutions:**
```bash
# Disable catch-all temporarily
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/catch_all" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": false
  }'

# Implement Email Worker with spam filtering
# Create specific rules instead of catch-all
# Use drop action for known spam patterns

# Re-enable with worker filter
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/email/routing/catch_all" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "actions": [{
      "type": "worker",
      "value": ["spam-filter-worker"]
    }]
  }'
```

## See Also

- **[Cloudflare DNS](cloudflare-dns.md)** - DNS management for email routing
- **[Cloudflare Workers](cloudflare-workers.md)** - Serverless functions for email processing
- **[Cloudflare Pages](cloudflare-pages.md)** - Host contact forms that trigger email routing
- **[Cloudflare Zero Trust](cloudflare-zero-trust.md)** - Secure access to email management
- **[Cloudflare API](cloudflare-api.md)** - Programmatic email routing management
