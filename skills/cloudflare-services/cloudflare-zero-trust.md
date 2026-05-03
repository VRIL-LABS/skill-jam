---
name: Cloudflare Zero Trust
description: Implement Cloudflare Zero Trust (formerly Cloudflare for Teams) for identity-aware access control that replaces traditional VPNs. Configure device posture, WARP client, and access policies for secure application access. Trigger phrases include "Zero Trust", "Cloudflare Access", "replace VPN", "device posture", "WARP client", and "identity-based access".
license: MIT
---

# Cloudflare Zero Trust

Cloudflare Zero Trust is a comprehensive security platform that replaces legacy VPNs and perimeter-based security with a modern, identity-aware approach. It provides secure access to applications, networks, and data based on user identity, device health, and contextual signals, implementing true Zero Trust Network Access (ZTNA) principles.

## When to Use

Use Cloudflare Zero Trust when you need to:

- **Replace legacy VPNs** with modern, identity-based access
- **Implement Zero Trust security** across your organization
- **Secure remote access** for distributed workforce
- **Protect internal applications** without exposing them to the internet
- **Enforce device posture** checks before granting access
- **Control SaaS application** access with inline inspection
- **Filter internet traffic** for remote and office users
- **Implement CASB** (Cloud Access Security Broker) functionality
- **Secure private networks** without traditional network perimeters
- **Comply with regulatory requirements** for access control and logging
- **Reduce attack surface** by making applications invisible to unauthorized users
- **Enable secure BYOD** (Bring Your Own Device) policies

Cloudflare Zero Trust is essential for organizations modernizing security infrastructure and enabling secure, flexible access for today's distributed workforces.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/cloudflare-one/
- **Getting Started**: https://developers.cloudflare.com/cloudflare-one/setup/
- **Access Application Protection**: https://developers.cloudflare.com/cloudflare-one/applications/
- **Tunnel Connections**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **WARP Client**: https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/
- **Gateway Policies**: https://developers.cloudflare.com/cloudflare-one/policies/
- **Device Posture**: https://developers.cloudflare.com/cloudflare-one/identity/devices/
- **Identity Providers**: https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/
- **Tutorials**: https://developers.cloudflare.com/cloudflare-one/tutorials/

## Quick Start

### Initial Setup

1. **Create Cloudflare Zero Trust Account**
   ```
   Navigate to: https://one.dash.cloudflare.com
   Sign up or log in with Cloudflare account
   Choose a team name (e.g., "acme-corp")
   ```

2. **Configure Authentication**
   ```
   Go to Settings > Authentication
   Add Identity Provider (IdP):
   - One-time PIN (email)
   - Azure AD / Okta / Google Workspace
   - SAML / OIDC
   ```

3. **Install WARP Client (Optional but Recommended)**
   ```
   Download from: https://1.1.1.1/
   Install on user devices
   Configure device enrollment
   ```

### Protect Your First Application

**Step 1: Create Access Application**

Via Dashboard:
```
1. Navigate to Access > Applications
2. Click "Add an application"
3. Select "Self-hosted"
4. Configure:
   - Application name: "Internal Dashboard"
   - Application domain: dashboard.internal.example.com
   - Session duration: 24 hours
5. Add Access Policy:
   - Policy name: "Allow team members"
   - Action: Allow
   - Include: Emails ending in @example.com
6. Save application
```

Via API:
```bash
ACCOUNT_ID="your_account_id"
API_TOKEN="your_api_token"

curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Internal Dashboard",
    "domain": "dashboard.internal.example.com",
    "type": "self_hosted",
    "session_duration": "24h",
    "allowed_idps": [],
    "auto_redirect_to_identity": false,
    "enable_binding_cookie": false,
    "cors_headers": {
      "allow_all_origins": false
    }
  }'
```

**Step 2: Create Access Policy**

```bash
# Get application ID from previous step
APP_ID="app-id-from-previous-response"

curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps/${APP_ID}/policies" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Allow company email",
    "decision": "allow",
    "include": [
      {
        "email_domain": {
          "domain": "example.com"
        }
      }
    ],
    "precedence": 1,
    "session_duration": "24h"
  }'
```

**Step 3: Connect Application via Tunnel**

```bash
# Install and authenticate cloudflared
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create internal-apps

# Configure tunnel
cat > ~/.cloudflared/config.yml <<EOF
tunnel: <TUNNEL_ID>
credentials-file: /home/user/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: dashboard.internal.example.com
    service: http://localhost:8080
  - service: http_status:404
EOF

# Route DNS
cloudflared tunnel route dns internal-apps dashboard.internal.example.com

# Run tunnel
cloudflared tunnel run internal-apps
```

### Configure Gateway Policies

**Step 1: Enable Gateway**

```
1. Navigate to Gateway > Policies
2. Configure DNS filtering
3. Set up HTTP filtering (requires WARP client)
4. Enable logging and analytics
```

**Step 2: Create DNS Policy**

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/gateway/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Block malware domains",
    "description": "Block known malicious domains",
    "action": "block",
    "filters": ["dns"],
    "traffic": "any(dns.security_category[*] in {\"Malware\" \"Phishing\"})",
    "enabled": true,
    "precedence": 1
  }'
```

**Step 3: Create HTTP Policy**

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/gateway/rules" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Block social media",
    "description": "Prevent access to social media sites",
    "action": "block",
    "filters": ["http"],
    "traffic": "any(http.request.domains[*] in $social_media)",
    "enabled": true,
    "precedence": 2,
    "rule_settings": {
      "block_page_enabled": true,
      "block_reason": "Social media access restricted during work hours"
    }
  }'
```

## Core Features

### 1. Access - Application Protection

Secure access to internal applications with identity-based authentication.

**Self-Hosted Applications:**
```hcl
# Terraform configuration
resource "cloudflare_access_application" "internal_app" {
  account_id = var.account_id
  name       = "Internal CRM"
  domain     = "crm.internal.example.com"
  type       = "self_hosted"
  
  session_duration = "24h"
  
  auto_redirect_to_identity = true
  enable_binding_cookie     = true
  
  cors_headers {
    allow_all_origins  = false
    allow_all_methods  = false
    allow_all_headers  = false
    allowed_origins    = ["https://crm.internal.example.com"]
    allowed_methods    = ["GET", "POST", "PUT", "DELETE"]
    allowed_headers    = ["Content-Type", "Authorization"]
    allow_credentials  = true
    max_age            = 86400
  }
}

resource "cloudflare_access_policy" "internal_app_policy" {
  application_id = cloudflare_access_application.internal_app.id
  account_id     = var.account_id
  name           = "Allow employees and contractors"
  precedence     = 1
  decision       = "allow"

  include {
    group = ["employees-group-id"]
  }

  include {
    email = ["contractor@partner.com"]
  }

  require {
    device_posture = ["managed-device"]
  }

  exclude {
    email = ["suspended@example.com"]
  }
  
  session_duration = "12h"
}
```

**SaaS Applications:**
```hcl
resource "cloudflare_access_application" "saas_app" {
  account_id   = var.account_id
  name         = "GitHub Enterprise"
  type         = "saas"
  
  saas_app {
    consumer_service_url = "https://github.com/orgs/your-org/sso"
    sp_entity_id         = "https://github.com/orgs/your-org"
    name_id_format       = "email"
    
    custom_attributes {
      name         = "department"
      name_format  = "urn:oasis:names:tc:SAML:2.0:attrname-format:basic"
      source {
        name = "department"
      }
    }
  }
  
  allowed_idps    = [var.okta_idp_id]
  session_duration = "24h"
}
```

**Bookmark Applications:**
```bash
# Create bookmark app for quick access
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AWS Console",
    "type": "bookmark",
    "domain": "https://console.aws.amazon.com",
    "logo_url": "https://example.com/aws-logo.png",
    "app_launcher_visible": true
  }'
```

### 2. Gateway - Secure Web Gateway

Filter and inspect internet traffic for security and compliance.

**DNS Filtering:**
```hcl
# Block malicious domains
resource "cloudflare_teams_rule" "block_malware" {
  account_id  = var.account_id
  name        = "Block Malware and Phishing"
  description = "Block known malicious domains"
  action      = "block"
  enabled     = true
  filters     = ["dns"]
  
  traffic = "any(dns.security_category[*] in {\"Malware\" \"Phishing\" \"Command and Control\"})"
  
  rule_settings {
    block_page_enabled = true
    block_page_reason  = "This domain has been blocked due to security concerns"
  }
}

# Block specific categories
resource "cloudflare_teams_rule" "block_adult_content" {
  account_id = var.account_id
  name       = "Block Adult Content"
  action     = "block"
  enabled    = true
  filters    = ["dns"]
  
  traffic = "any(dns.content_category[*] in {\"Adult Themes\" \"Gambling\"})"
}

# Allow specific domains (exemption)
resource "cloudflare_teams_rule" "allow_trusted" {
  account_id = var.account_id
  name       = "Allow Trusted Domains"
  action     = "allow"
  enabled    = true
  filters    = ["dns"]
  precedence = 1  # Higher precedence = evaluated first
  
  traffic = "any(dns.domains[*] in {\"trusted.example.com\" \"partner.example.com\"})"
}
```

**HTTP/HTTPS Filtering:**
```hcl
# Inspect and filter HTTP traffic
resource "cloudflare_teams_rule" "http_inspection" {
  account_id  = var.account_id
  name        = "Block File Downloads"
  description = "Prevent downloading executable files"
  action      = "block"
  enabled     = true
  filters     = ["http"]
  
  traffic = "any(http.request.uri.path[*] matches \".*\\\\.(exe|msi|dmg|pkg)$\")"
  
  rule_settings {
    block_page_enabled = true
    block_page_reason  = "Executable downloads are not permitted"
  }
}

# Data Loss Prevention
resource "cloudflare_teams_rule" "dlp_sensitive_data" {
  account_id = var.account_id
  name       = "Block Credit Card Uploads"
  action     = "block"
  enabled    = true
  filters    = ["http"]
  
  traffic = "any(http.request.body.raw[*] matches \"[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}\")"
  
  rule_settings {
    block_page_enabled = true
    block_page_reason  = "Uploading credit card numbers is prohibited"
    override_ips       = []
    override_host      = ""
  }
}

# Time-based filtering
resource "cloudflare_teams_rule" "block_streaming_work_hours" {
  account_id = var.account_id
  name       = "Block Streaming During Work Hours"
  action     = "block"
  enabled    = true
  filters    = ["http"]
  
  traffic = "any(http.request.domains[*] in $streaming_services) and identity.time.hour >= 9 and identity.time.hour < 17"
}
```

**Network Filtering (Layer 4):**
```hcl
resource "cloudflare_teams_rule" "block_rdp" {
  account_id  = var.account_id
  name        = "Block RDP Traffic"
  description = "Prevent unauthorized RDP connections"
  action      = "block"
  enabled     = true
  filters     = ["l4"]
  
  traffic = "net.dst.port == 3389"
}

resource "cloudflare_teams_rule" "allow_office_ips" {
  account_id = var.account_id
  name       = "Allow Office Network"
  action     = "allow"
  enabled    = true
  filters    = ["l4"]
  precedence = 1
  
  traffic = "ip.src in {203.0.113.0/24 198.51.100.0/24}"
}
```

### 3. Device Posture Checks

Verify device health and compliance before granting access.

**Configure Posture Checks:**
```hcl
# Require antivirus running
resource "cloudflare_device_posture_rule" "require_antivirus" {
  account_id  = var.account_id
  name        = "Antivirus Running"
  type        = "file"
  description = "Check if antivirus is running"
  
  match {
    platform = "windows"
  }
  
  input {
    path = "C:\\Program Files\\Antivirus\\av.exe"
    exists = true
  }
}

# Require OS version
resource "cloudflare_device_posture_rule" "os_version" {
  account_id  = var.account_id
  name        = "Minimum macOS Version"
  type        = "os_version"
  description = "Require macOS 13.0 or later"
  
  match {
    platform = "mac"
  }
  
  input {
    version        = "13.0.0"
    operator       = ">="
  }
}

# Require disk encryption
resource "cloudflare_device_posture_rule" "disk_encryption" {
  account_id = var.account_id
  name       = "Disk Encryption Enabled"
  type       = "disk_encryption"
  
  match {
    platform = "windows"
  }
  
  input {
    require_all = true
  }
}

# Require domain joined
resource "cloudflare_device_posture_rule" "domain_joined" {
  account_id = var.account_id
  name       = "Domain Joined Device"
  type       = "domain_joined"
  
  match {
    platform = "windows"
  }
  
  input {
    domain = "corp.example.com"
  }
}

# Serial number list (managed devices)
resource "cloudflare_device_posture_rule" "serial_number" {
  account_id = var.account_id
  name       = "Managed Device"
  type       = "serial_number"
  
  input {
    serial_numbers = [
      "C02ABC123456",
      "C02DEF789012"
    ]
  }
}
```

**Apply Posture in Access Policy:**
```hcl
resource "cloudflare_access_policy" "secure_app_policy" {
  application_id = cloudflare_access_application.app.id
  account_id     = var.account_id
  name           = "Require Compliant Device"
  precedence     = 1
  decision       = "allow"

  include {
    email_domain = {
      domain = "example.com"
    }
  }

  require {
    device_posture = [
      cloudflare_device_posture_rule.require_antivirus.id,
      cloudflare_device_posture_rule.os_version.id,
      cloudflare_device_posture_rule.disk_encryption.id
    ]
  }
}
```

### 4. WARP Client Configuration

Deploy and configure the WARP client for Zero Trust network access.

**Device Enrollment Rules:**
```hcl
resource "cloudflare_device_settings_policy" "default_policy" {
  account_id  = var.account_id
  name        = "Default WARP Policy"
  description = "Default settings for enrolled devices"
  
  match = "identity.email.domain == \"example.com\""
  
  # WARP mode
  switch_locked = false  # Allow users to disable WARP
  
  # Service mode
  service_mode_v2_mode = "warp"  # Options: proxy, warp, warp_dot, warp_dot_doh
  
  # Gateway with WARP
  captive_portal = 180  # Seconds to wait for captive portal
  disable_auto_fallback = false
  
  # Split tunnel configuration
  exclude {
    address = "192.168.1.0/24"
  }
  exclude {
    host = "internal.company.lan"
  }
  
  # Include specific routes
  include {
    address = "10.0.0.0/8"
  }
  
  # Local domain fallback
  local_domain_fallback {
    domain = "corp.example.com"
    dns_server = ["10.0.0.53"]
  }
}
```

**Managed Deployment:**
```xml
<!-- Windows - GPO deployment -->
<!-- ADMX policy for WARP -->
<policy name="CloudflareWARP" class="Machine">
  <key>Software\Cloudflare\WARP</key>
  <valueName>OrganizationName</valueName>
  <value>example-corp</value>
</policy>
```

```bash
# macOS - MDM deployment
defaults write /Library/Preferences/com.cloudflare.warp organization "example-corp"
defaults write /Library/Preferences/com.cloudflare.warp auto_connect -int 1
defaults write /Library/Preferences/com.cloudflare.warp switch_locked -bool true
```

```json
// Android/iOS - MDM configuration
{
  "organization": "example-corp",
  "auto_connect": 1,
  "switch_locked": false,
  "service_mode": "warp",
  "support_url": "https://support.example.com/warp"
}
```

### 5. Identity Provider Integration

Integrate with existing identity providers for seamless authentication.

**Azure AD Configuration:**
```hcl
resource "cloudflare_access_identity_provider" "azure_ad" {
  account_id = var.account_id
  name       = "Azure AD"
  type       = "azureAD"
  
  config {
    client_id     = var.azure_client_id
    client_secret = var.azure_client_secret
    directory_id  = var.azure_directory_id
    
    support_groups = true
    
    conditional_access_enabled = true
  }
}
```

**Okta Configuration:**
```hcl
resource "cloudflare_access_identity_provider" "okta" {
  account_id = var.account_id
  name       = "Okta"
  type       = "okta"
  
  config {
    client_id      = var.okta_client_id
    client_secret  = var.okta_client_secret
    authorization_server_id = var.okta_auth_server
    okta_account   = "example.okta.com"
  }
}
```

**SAML Integration:**
```hcl
resource "cloudflare_access_identity_provider" "saml_idp" {
  account_id = var.account_id
  name       = "Corporate SAML"
  type       = "saml"
  
  config {
    issuer_url       = "https://idp.example.com/saml"
    sso_target_url   = "https://idp.example.com/sso"
    sign_request     = true
    idp_public_cert  = var.saml_cert
    
    attributes = [
      "email",
      "groups",
      "department"
    ]
    
    email_attribute_name = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
  }
}
```

## Common Use Cases

### 1. Replace Corporate VPN

Migrate from traditional VPN to Zero Trust access.

**Architecture:**
```hcl
# Tunnel for internal apps
resource "cloudflare_tunnel" "corporate_apps" {
  account_id = var.account_id
  name       = "corporate-apps-tunnel"
  secret     = var.tunnel_secret
}

resource "cloudflare_tunnel_config" "corporate_apps_config" {
  account_id = var.account_id
  tunnel_id  = cloudflare_tunnel.corporate_apps.id

  config {
    warp_routing {
      enabled = true
    }
    
    ingress_rule {
      hostname = "intranet.example.com"
      service  = "http://10.0.1.100:80"
    }
    
    ingress_rule {
      hostname = "wiki.example.com"
      service  = "http://10.0.1.200:80"
    }
    
    ingress_rule {
      service = "http_status:404"
    }
  }
}

# Route private networks
resource "cloudflare_tunnel_virtual_network" "corporate_network" {
  account_id = var.account_id
  name       = "Corporate Network"
  comment    = "Main office and data center networks"
}

resource "cloudflare_tunnel_route" "office_network" {
  account_id = var.account_id
  tunnel_id  = cloudflare_tunnel.corporate_apps.id
  network    = "10.0.0.0/8"
  comment    = "Route office network through tunnel"
  virtual_network_id = cloudflare_tunnel_virtual_network.corporate_network.id
}

# Access policies for internal resources
resource "cloudflare_access_application" "intranet" {
  account_id       = var.account_id
  name             = "Corporate Intranet"
  domain           = "intranet.example.com"
  session_duration = "12h"
  
  auto_redirect_to_identity = true
}

resource "cloudflare_access_policy" "intranet_policy" {
  application_id = cloudflare_access_application.intranet.id
  account_id     = var.account_id
  name           = "Employees Only"
  decision       = "allow"

  include {
    group = [var.employees_group_id]
  }

  require {
    device_posture = [
      cloudflare_device_posture_rule.disk_encryption.id,
      cloudflare_device_posture_rule.os_version.id
    ]
  }
}
```

### 2. Secure Contractor Access

Provide time-limited access to external contractors.

```hcl
# Contractor access group
resource "cloudflare_access_group" "contractors" {
  account_id = var.account_id
  name       = "Contractors"

  include {
    email = [
      "contractor1@vendor.com",
      "contractor2@vendor.com"
    ]
  }
}

# Time-limited access application
resource "cloudflare_access_application" "contractor_portal" {
  account_id       = var.account_id
  name             = "Contractor Portal"
  domain           = "contractors.example.com"
  session_duration = "4h"  # Short session for contractors
  
  app_launcher_visible = true
}

resource "cloudflare_access_policy" "contractor_policy" {
  application_id = cloudflare_access_application.contractor_portal.id
  account_id     = var.account_id
  name           = "Contractor Access"
  decision       = "allow"

  include {
    group = [cloudflare_access_group.contractors.id]
  }

  require {
    # Require approval from full-time employee
    everyone = false
  }
  
  # Access only during work hours
  require {
    auth_method = {
      auth_method = "otp"  # Require OTP for contractors
    }
  }
}

# Audit logging for contractor access
resource "cloudflare_access_policy" "contractor_audit" {
  application_id = cloudflare_access_application.contractor_portal.id
  account_id     = var.account_id
  name           = "Audit Contractor Actions"
  decision       = "allow"

  include {
    group = [cloudflare_access_group.contractors.id]
  }
  
  session_duration = "4h"
}
```

### 3. Multi-Region Application Access

Provide optimal access to globally distributed applications.

```hcl
# US region tunnel
resource "cloudflare_tunnel" "us_region" {
  account_id = var.account_id
  name       = "us-apps-tunnel"
  secret     = var.us_tunnel_secret
}

# EU region tunnel
resource "cloudflare_tunnel" "eu_region" {
  account_id = var.account_id
  name       = "eu-apps-tunnel"
  secret     = var.eu_tunnel_secret
}

# Load balancer for geo-routing
resource "cloudflare_load_balancer" "global_app" {
  zone_id = var.zone_id
  name    = "app.example.com"
  
  default_pool_ids = [
    cloudflare_load_balancer_pool.us_pool.id,
    cloudflare_load_balancer_pool.eu_pool.id
  ]
  
  proxied          = true
  steering_policy  = "geo"
  session_affinity = "cookie"
  
  pop_pools {
    pop      = "LAX"
    pool_ids = [cloudflare_load_balancer_pool.us_pool.id]
  }
  
  pop_pools {
    pop      = "LHR"
    pool_ids = [cloudflare_load_balancer_pool.eu_pool.id]
  }
}

# Regional access policies
resource "cloudflare_access_policy" "us_employees" {
  application_id = cloudflare_access_application.app.id
  account_id     = var.account_id
  name           = "US Employees"
  decision       = "allow"

  include {
    geo = ["US", "CA", "MX"]
  }
  
  include {
    email_domain = {
      domain = "example.com"
    }
  }
}
```

### 4. CASB for SaaS Applications

Secure and monitor access to third-party SaaS applications.

```hcl
# Configure HTTP filtering for SaaS apps
resource "cloudflare_teams_rule" "monitor_saas_uploads" {
  account_id  = var.account_id
  name        = "Monitor File Uploads to Cloud Storage"
  description = "Log and inspect uploads to cloud storage"
  action      = "allow"  # Allow but log
  enabled     = true
  filters     = ["http"]
  
  traffic = "any(http.request.domains[*] in {\"drive.google.com\" \"dropbox.com\" \"onedrive.live.com\"}) and http.request.method == \"POST\""
  
  rule_settings {
    check_session = true
    
    payload_log {
      enabled = true
    }
  }
}

# Block unauthorized SaaS applications
resource "cloudflare_teams_rule" "block_shadow_it" {
  account_id = var.account_id
  name       = "Block Unauthorized SaaS"
  action     = "block"
  enabled    = true
  filters    = ["http"]
  
  traffic = "any(http.request.domains[*] in $unapproved_saas_apps)"
  
  rule_settings {
    block_page_enabled = true
    block_page_reason  = "This SaaS application is not approved. Contact IT for alternatives."
  }
}

# DLP for sensitive data in SaaS
resource "cloudflare_teams_rule" "dlp_saas" {
  account_id = var.account_id
  name       = "Prevent SSN Uploads"
  action     = "block"
  enabled    = true
  filters    = ["http"]
  
  traffic = "any(http.request.body.raw[*] matches \"[0-9]{3}-[0-9]{2}-[0-9]{4}\")"
}
```

### 5. Secure Remote Desktop Access

Enable secure RDP and SSH access without exposing ports.

```yaml
# cloudflared config for RDP/SSH
tunnel: remote-access-tunnel
credentials-file: /path/to/credentials.json

ingress:
  - hostname: rdp.example.com
    service: tcp://10.0.1.50:3389
  
  - hostname: ssh.example.com
    service: ssh://10.0.1.100:22
  
  - service: http_status:404
```

```hcl
# Access policies for remote desktop
resource "cloudflare_access_application" "rdp_access" {
  account_id       = var.account_id
  name             = "RDP Access"
  domain           = "rdp.example.com"
  type             = "self_hosted"
  session_duration = "2h"
}

resource "cloudflare_access_policy" "rdp_policy" {
  application_id = cloudflare_access_application.rdp_access.id
  account_id     = var.account_id
  name           = "IT Admins Only"
  decision       = "allow"

  include {
    group = [var.it_admins_group_id]
  }

  require {
    device_posture = [
      cloudflare_device_posture_rule.serial_number.id  # Managed devices only
    ]
  }
}
```

**Client-side RDP connection:**
```bash
# Install cloudflared
brew install cloudflare/cloudflare/cloudflared

# Access RDP through tunnel
cloudflared access rdp --hostname rdp.example.com --url localhost:13389

# In another terminal, connect RDP client to localhost:13389
```

## Integration

### 1. Integration with SIEM

Export Zero Trust logs to SIEM for security analytics.

```hcl
# Configure log push to S3
resource "cloudflare_logpush_job" "zero_trust_logs" {
  account_id          = var.account_id
  enabled             = true
  name                = "zero-trust-access-logs"
  destination_conf    = "s3://my-bucket/zero-trust-logs?region=us-east-1"
  dataset             = "access_requests"
  frequency           = "high"
  max_upload_bytes    = 5000000
  max_upload_records  = 1000
  
  ownership_challenge = var.ownership_token
}

# Gateway DNS logs
resource "cloudflare_logpush_job" "gateway_dns" {
  account_id       = var.account_id
  enabled          = true
  name             = "gateway-dns-logs"
  destination_conf = "s3://my-bucket/gateway-dns?region=us-east-1"
  dataset          = "gateway_dns"
  frequency        = "high"
}

# Gateway HTTP logs
resource "cloudflare_logpush_job" "gateway_http" {
  account_id       = var.account_id
  enabled          = true
  name             = "gateway-http-logs"
  destination_conf = "s3://my-bucket/gateway-http?region=us-east-1"
  dataset          = "gateway_http"
  frequency        = "high"
}
```

**Splunk Integration:**
```python
# Forward Cloudflare logs to Splunk
import boto3
import requests
from datetime import datetime

class CloudflareToSplunk:
    def __init__(self, splunk_hec_url, splunk_token, s3_bucket):
        self.splunk_url = splunk_hec_url
        self.splunk_token = splunk_token
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
    
    def process_logs(self, log_file):
        # Download from S3
        obj = self.s3.get_object(Bucket=self.bucket, Key=log_file)
        logs = obj['Body'].read().decode('utf-8')
        
        # Send to Splunk HEC
        headers = {
            'Authorization': f'Splunk {self.splunk_token}',
            'Content-Type': 'application/json'
        }
        
        for line in logs.splitlines():
            event = {
                'time': datetime.now().timestamp(),
                'sourcetype': 'cloudflare:zerotrust',
                'event': line
            }
            requests.post(self.splunk_url, json=event, headers=headers)
```

### 2. Integration with MDM

Deploy WARP client via Mobile Device Management.

**Jamf Pro (macOS):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>organization</key>
    <string>example-corp</string>
    <key>auto_connect</key>
    <integer>1</integer>
    <key>switch_locked</key>
    <false/>
    <key>service_mode</key>
    <string>warp</string>
    <key>support_url</key>
    <string>https://support.example.com/warp</string>
</dict>
</plist>
```

**Microsoft Intune (Windows):**
```xml
<Replace>
  <CmdID>1</CmdID>
  <Item>
    <Target>
      <LocURI>./Device/Vendor/MSFT/Policy/Config/Cloudflare~Policy~Cloudflare/Organization</LocURI>
    </Target>
    <Meta>
      <Format xmlns="syncml:metinf">chr</Format>
    </Meta>
    <Data>example-corp</Data>
  </Item>
</Replace>
```

### 3. Integration with Ticketing Systems

Automate access requests and approvals.

```python
# ServiceNow integration example
import requests
import json

class ZeroTrustAccessAutomation:
    def __init__(self, cf_account_id, cf_api_token, snow_instance, snow_credentials):
        self.cf_account_id = cf_account_id
        self.cf_api_token = cf_api_token
        self.snow_url = f"https://{snow_instance}.service-now.com/api/now"
        self.snow_auth = snow_credentials
    
    def create_temporary_access(self, email, app_id, duration_hours):
        """Create temporary access based on approved ticket"""
        
        # Create time-limited access group
        group_data = {
            "name": f"Temporary Access - {email}",
            "include": [{
                "email": [email]
            }],
            "exclude": []
        }
        
        # Add to Cloudflare Access
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{self.cf_account_id}/access/groups",
            headers={
                "Authorization": f"Bearer {self.cf_api_token}",
                "Content-Type": "application/json"
            },
            json=group_data
        )
        
        group_id = response.json()['result']['id']
        
        # Schedule removal after duration
        # (implement with cron or cloud scheduler)
        
        return group_id
    
    def revoke_access(self, group_id):
        """Revoke temporary access"""
        requests.delete(
            f"https://api.cloudflare.com/client/v4/accounts/{self.cf_account_id}/access/groups/{group_id}",
            headers={"Authorization": f"Bearer {self.cf_api_token}"}
        )
```

## Best Practices

### 1. Policy Design

- **Least Privilege**: Grant minimum necessary access
- **Defense in Depth**: Layer multiple security controls
- **Explicit Deny**: Use deny rules for known threats
- **Regular Review**: Audit policies quarterly
- **Document Changes**: Maintain policy change logs

### 2. Device Management

- **Enforce Posture**: Require device compliance checks
- **Serial Number Tracking**: Maintain device inventory
- **Regular Updates**: Keep WARP client current
- **Certificate Management**: Rotate device certificates
- **Lost Device Protocol**: Have revocation procedures

### 3. Identity Integration

- **SSO Everywhere**: Use single identity provider where possible
- **MFA Enforcement**: Require multi-factor authentication
- **Group-Based Access**: Use groups instead of individual emails
- **JIT Provisioning**: Implement just-in-time user provisioning
- **Regular Sync**: Keep directory synchronization current

### 4. Monitoring and Logging

- **Enable All Logging**: Capture access and gateway logs
- **SIEM Integration**: Forward logs to security analytics platform
- **Alert on Anomalies**: Set up alerts for suspicious activity
- **Regular Review**: Review access patterns monthly
- **Compliance Reports**: Generate audit reports for compliance

### 5. Performance Optimization

- **Geographic Distribution**: Deploy tunnels near users
- **Split Tunneling**: Exclude local resources from tunnel
- **DNS Optimization**: Use Cloudflare resolver for performance
- **Session Duration**: Balance security with user experience
- **Connection Pooling**: Optimize tunnel connections

## Troubleshooting

### Issue: Users Cannot Access Application

**Symptoms:**
- Access denied error
- Authentication loop
- Policy evaluation failures

**Solutions:**
```bash
# Check user's group membership
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/groups" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Verify policy configuration
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps/${APP_ID}/policies" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Check Access logs
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/logs/access-requests" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  --data-urlencode "since=2024-01-01T00:00:00Z"

# Test device posture compliance
# Have user run: cloudflared access device-posture
```

### Issue: WARP Client Won't Connect

**Symptoms:**
- Client shows disconnected
- Registration failures
- Network errors

**Solutions:**
```bash
# Verify team name
# Settings > Account > Team name should match client configuration

# Check device settings policy
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/devices/policies" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Review device enrollment
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/devices" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Client-side diagnostics
# macOS/Linux: cat /var/log/cloudflared.log
# Windows: Check Event Viewer > Applications > Cloudflare WARP
```

### Issue: Tunnel Connection Drops

**Symptoms:**
- Intermittent 502 errors
- Tunnel shows 0 connections
- Application timeouts

**Solutions:**
```bash
# Check tunnel status
cloudflared tunnel info <TUNNEL_ID>

# Monitor tunnel health
cloudflared tunnel --config /path/to/config.yml --loglevel debug run

# Verify tunnel routing
cloudflared tunnel route ip show

# Check origin reachability from tunnel host
curl -v http://localhost:8080
```

### Issue: Gateway Policies Not Applied

**Symptoms:**
- Sites not being blocked
- DNS filtering not working
- HTTP inspection failures

**Solutions:**
```bash
# Verify Gateway is enabled
# Zero Trust dashboard > Gateway > Policies

# Check policy order (precedence)
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/gateway/rules" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Verify WARP client is in Gateway mode
# WARP app > Preferences > Gateway with WARP should be enabled

# Test DNS resolution
# Should resolve through Gateway:
dig @1.1.1.1 example.com

# Review Gateway logs
# Zero Trust dashboard > Logs > Gateway
```

## See Also

- **[Cloudflare Tunnel](cloudflare-tunnel.md)** - Secure connections without public IPs
- **[Cloudflare WARP](cloudflare-warp.md)** - Client application for device connectivity
- **[Cloudflare Access](cloudflare-access.md)** - Application access control
- **[Cloudflare Gateway](cloudflare-gateway.md)** - Secure web gateway and DNS filtering
- **[Cloudflare DDoS Protection](cloudflare-ddos-protection.md)** - DDoS mitigation and protection
