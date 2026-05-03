---
name: Cloudflare Tunnel
description: Set up Cloudflare Tunnel (formerly Argo Tunnel) to create secure connections between your origin and Cloudflare without public IPs using the cloudflared daemon. Provides Zero Trust access with API and CLI management. Trigger phrases include "Cloudflare Tunnel", "cloudflared", "secure tunnel", "Argo Tunnel", "connect without public IP", and "Zero Trust tunnel".
license: MIT
---

# Cloudflare Tunnel

Cloudflare Tunnel provides secure, outbound-only connections from your infrastructure to Cloudflare's network without requiring publicly routable IP addresses. Using the lightweight `cloudflared` daemon, you can expose applications, services, and internal resources while maintaining full control over access policies and eliminating inbound firewall rules.

## When to Use

Use Cloudflare Tunnel when you need to:

- **Expose internal applications** to the internet without public IPs
- **Eliminate inbound firewall rules** for improved security posture
- **Connect on-premise services** to Cloudflare's network
- **Provide secure access** to development and staging environments
- **Protect origin servers** from direct internet exposure
- **Implement Zero Trust access** for internal applications
- **Simplify network architecture** by removing VPNs and bastion hosts
- **Enable remote access** to private services
- **Connect multi-cloud resources** through a unified network
- **Support SSH and RDP** access without exposing ports

Cloudflare Tunnel is ideal for organizations looking to modernize their network security with a Zero Trust approach while simplifying infrastructure management.

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Install and Setup cloudflared**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
- **Tunnel Configuration**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/
- **Routing Traffic**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/routing-to-tunnel/
- **Private Networks**: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- **Tunnel Management via API**: https://developers.cloudflare.com/api/operations/cloudflare-tunnel-list-cloudflare-tunnels
- **Tunnel Origins**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/routing-to-tunnel/dns/
- **Best Practices**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/deployment-guides/

## Quick Start

### Install cloudflared

**macOS (Homebrew):**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux (Debian/Ubuntu):**
```bash
# Download and install
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify installation
cloudflared --version
```

**Linux (RPM-based):**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
sudo rpm -i cloudflared-linux-x86_64.rpm
```

**Windows:**
```powershell
# Download from GitHub releases
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "cloudflared.exe"

# Move to Program Files
Move-Item cloudflared.exe "C:\Program Files\cloudflared.exe"
```

**Docker:**
```bash
docker pull cloudflare/cloudflared:latest
```

### Authenticate cloudflared

```bash
# Login to Cloudflare
cloudflared tunnel login

# This opens a browser window to authenticate
# After authentication, a certificate is saved to:
# ~/.cloudflared/cert.pem (Linux/macOS)
# %USERPROFILE%\.cloudflared\cert.pem (Windows)
```

### Create Your First Tunnel

```bash
# Create a tunnel
cloudflared tunnel create my-tunnel

# This generates:
# - Tunnel UUID
# - Credentials file: ~/.cloudflared/<TUNNEL_UUID>.json

# List tunnels
cloudflared tunnel list

# Example output:
# ID                                   NAME       CREATED              CONNECTIONS
# a1b2c3d4-e5f6-7890-abcd-ef1234567890 my-tunnel  2024-01-15T10:30:00Z 0
```

### Configure the Tunnel

Create a configuration file at `~/.cloudflared/config.yml`:

```yaml
tunnel: a1b2c3d4-e5f6-7890-abcd-ef1234567890
credentials-file: /home/user/.cloudflared/a1b2c3d4-e5f6-7890-abcd-ef1234567890.json

ingress:
  # Route requests to app.example.com to local service
  - hostname: app.example.com
    service: http://localhost:8080
  
  # Route requests to api.example.com to different port
  - hostname: api.example.com
    service: http://localhost:3000
  
  # Catch-all rule (required)
  - service: http_status:404
```

### Create DNS Record

```bash
# Create DNS route to tunnel
cloudflared tunnel route dns my-tunnel app.example.com

# Or manually create CNAME record:
# app.example.com CNAME a1b2c3d4-e5f6-7890-abcd-ef1234567890.cfargotunnel.com
```

### Run the Tunnel

```bash
# Run tunnel (foreground)
cloudflared tunnel run my-tunnel

# Run tunnel as a service (background)
cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

# Check status
sudo systemctl status cloudflared
```

### Quick Test

```bash
# Test locally before DNS propagation
curl -H "Host: app.example.com" http://localhost:8080

# Test through Cloudflare after DNS setup
curl https://app.example.com
```

## Core Features

### 1. HTTP/HTTPS Application Tunneling

Expose web applications securely through Cloudflare's network.

**Basic Configuration:**
```yaml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  - hostname: web.example.com
    service: http://localhost:8080
    originRequest:
      noTLSVerify: false
      connectTimeout: 30s
      http2Origin: true
  - service: http_status:404
```

**Advanced Configuration with Path-Based Routing:**
```yaml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  # Route specific paths to different services
  - hostname: app.example.com
    path: /api/*
    service: http://localhost:3000
  
  - hostname: app.example.com
    path: /admin/*
    service: http://localhost:4000
  
  - hostname: app.example.com
    service: http://localhost:8080
  
  # Static files from local directory
  - hostname: static.example.com
    service: hello_world
  
  - service: http_status:404
```

**TLS Configuration:**
```yaml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  - hostname: secure.example.com
    service: https://localhost:8443
    originRequest:
      # Use custom CA certificate
      caPool: /path/to/ca-cert.pem
      # Skip TLS verification (not recommended for production)
      noTLSVerify: false
      # Custom origin server name
      originServerName: internal.server.local
  - service: http_status:404
```

### 2. Private Network Access (WARP Connector)

Connect entire private networks to Cloudflare for Zero Trust access.

**Configuration:**
```yaml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json

# Enable WARP routing
warp-routing:
  enabled: true

ingress:
  # No public hostnames needed for private network access
  - service: http_status:404
```

**Route Private IPs through Tunnel:**
```bash
# Add IP routes to tunnel
cloudflared tunnel route ip add 10.0.0.0/24 my-tunnel
cloudflared tunnel route ip add 192.168.1.0/24 my-tunnel

# List IP routes
cloudflared tunnel route ip show

# Delete route
cloudflared tunnel route ip delete 10.0.0.0/24
```

**Access Private Resources:**
Users with WARP client can access private IPs:
```bash
# Install WARP client on user device
# Configure Zero Trust device enrollment
# Users can now access: http://10.0.0.50:8080
```

### 3. TCP and SSH Access

Enable TCP-level access for databases, SSH, and other services.

**SSH Configuration:**
```yaml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  - hostname: ssh.example.com
    service: ssh://localhost:22
  - service: http_status:404
```

**SSH Client Setup:**
```bash
# Add to ~/.ssh/config
Host ssh.example.com
  ProxyCommand cloudflared access ssh --hostname %h
  User your-username
  IdentityFile ~/.ssh/id_rsa

# Connect via SSH
ssh ssh.example.com
```

**Database Tunnel (MySQL Example):**
```yaml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  - hostname: mysql.example.com
    service: tcp://localhost:3306
  - service: http_status:404
```

**Connect to Database:**
```bash
# Install cloudflared access helper
cloudflared access tcp --hostname mysql.example.com --url localhost:13306

# In another terminal, connect to local port
mysql -h 127.0.0.1 -P 13306 -u user -p
```

### 4. Load Balancing and High Availability

Deploy multiple tunnel replicas for reliability and performance.

**Multi-Replica Deployment:**
```bash
# Create tunnel
cloudflared tunnel create ha-tunnel

# Deploy on Server 1
cloudflared tunnel --config /etc/cloudflared/config.yml run ha-tunnel

# Deploy on Server 2 (same tunnel ID)
cloudflared tunnel --config /etc/cloudflared/config.yml run ha-tunnel

# Cloudflare automatically load balances between replicas
```

**Health Checks:**
```yaml
tunnel: ha-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  - hostname: app.example.com
    service: http://localhost:8080
    originRequest:
      # Configure connection parameters
      keepAliveConnections: 100
      keepAliveTimeout: 90s
      tcpKeepAlive: 30s
      # Retry logic
      noHappyEyeballs: false
      connectTimeout: 10s
  - service: http_status:404
```

**Configuration for Multiple Origins:**
```yaml
tunnel: ha-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  - hostname: app.example.com
    service: http://backend-1:8080
  
  # Fallback configured at DNS level via Load Balancer
  # or deploy multiple tunnel replicas pointing to different backends
  
  - service: http_status:404
```

### 5. Docker and Kubernetes Deployment

Run tunnels in containerized environments.

**Docker Compose:**
```yaml
version: '3'

services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    restart: unless-stopped
    command: tunnel --config /etc/cloudflared/config.yml run
    volumes:
      - ./config.yml:/etc/cloudflared/config.yml:ro
      - ./credentials.json:/etc/cloudflared/credentials.json:ro
    networks:
      - app-network
  
  web-app:
    image: nginx:latest
    container_name: web-app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Kubernetes Deployment:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tunnel-credentials
  namespace: default
type: Opaque
stringData:
  credentials.json: |
    {
      "AccountTag": "your-account-id",
      "TunnelSecret": "your-tunnel-secret",
      "TunnelID": "your-tunnel-id"
    }

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cloudflared-config
  namespace: default
data:
  config.yml: |
    tunnel: your-tunnel-id
    credentials-file: /etc/cloudflared/credentials.json
    ingress:
      - hostname: k8s-app.example.com
        service: http://web-service:80
      - service: http_status:404

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudflared
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cloudflared
  template:
    metadata:
      labels:
        app: cloudflared
    spec:
      containers:
      - name: cloudflared
        image: cloudflare/cloudflared:latest
        args:
          - tunnel
          - --config
          - /etc/cloudflared/config.yml
          - run
        volumeMounts:
          - name: config
            mountPath: /etc/cloudflared/config.yml
            subPath: config.yml
            readOnly: true
          - name: credentials
            mountPath: /etc/cloudflared/credentials.json
            subPath: credentials.json
            readOnly: true
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
      volumes:
        - name: config
          configMap:
            name: cloudflared-config
        - name: credentials
          secret:
            secretName: tunnel-credentials
```

## Common Use Cases

### 1. Internal Dashboard Access

Expose internal dashboards without VPN.

```yaml
# config.yml
tunnel: dashboard-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  # Grafana
  - hostname: grafana.internal.example.com
    service: http://localhost:3000
  
  # Prometheus
  - hostname: prometheus.internal.example.com
    service: http://localhost:9090
  
  # Kibana
  - hostname: kibana.internal.example.com
    service: http://localhost:5601
  
  - service: http_status:404
```

**Apply Zero Trust Access Policy:**
```bash
# Create Access Application via Cloudflare Zero Trust dashboard
# Configure authentication (email, SAML, OAuth)
# Restrict access by email domain or group membership
```

### 2. Development Environment Access

Provide secure access to staging and dev environments.

```yaml
# config.yml for dev environment
tunnel: dev-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  # Frontend dev server
  - hostname: frontend-dev.example.com
    service: http://localhost:3000
    originRequest:
      noTLSVerify: true
      disableChunkedEncoding: false
      http2Origin: false
  
  # Backend API dev
  - hostname: api-dev.example.com
    service: http://localhost:8080
  
  # Database admin (pgAdmin)
  - hostname: pgadmin-dev.example.com
    service: http://localhost:5050
  
  - service: http_status:404
```

### 3. Multi-Cloud Application Integration

Connect services across different cloud providers.

```yaml
# Tunnel on AWS connecting to GCP services
tunnel: multi-cloud-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  # AWS-hosted frontend accessing GCP backend
  - hostname: app.example.com
    service: http://localhost:8080
  
  # Private network routing for inter-cloud communication
  # Configure IP routes for GCP VPC ranges
  
  - service: http_status:404
```

```bash
# Route GCP private IPs through tunnel
cloudflared tunnel route ip add 10.128.0.0/20 multi-cloud-tunnel
```

### 4. IoT Device Management

Secure access to IoT devices behind NAT.

```yaml
# Tunnel on edge gateway
tunnel: iot-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  # IoT device management interface
  - hostname: iot-manager.example.com
    service: http://10.0.1.100:80
  
  # MQTT broker
  - hostname: mqtt.example.com
    service: tcp://localhost:1883
  
  # Device logs and monitoring
  - hostname: iot-logs.example.com
    service: http://localhost:3000
  
  - service: http_status:404
```

### 5. CI/CD Pipeline Integration

Expose build agents and runners securely.

```yaml
# config.yml for CI/CD
tunnel: cicd-tunnel-uuid
credentials-file: /path/to/credentials.json

ingress:
  # Jenkins
  - hostname: jenkins.internal.example.com
    service: http://localhost:8080
  
  # GitLab Runner
  - hostname: gitlab-runner.internal.example.com
    service: http://localhost:9090
  
  # Artifact repository
  - hostname: artifacts.internal.example.com
    service: http://localhost:8081
  
  - service: http_status:404
```

## Integration

### 1. Integration with Cloudflare Zero Trust

Combine tunnels with Access policies for secure authentication.

**Create Access Application:**
```bash
# Via Cloudflare Zero Trust Dashboard:
# 1. Go to Access > Applications
# 2. Add an application
# 3. Select "Self-hosted"
# 4. Set application domain: app.example.com
# 5. Configure authentication methods
# 6. Set access policies
```

**API-Based Access Policy Creation:**
```bash
ACCOUNT_ID="your_account_id"
API_TOKEN="your_api_token"

curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Internal App",
    "domain": "app.example.com",
    "session_duration": "24h",
    "allowed_idps": ["idp-id-here"],
    "policies": [{
      "name": "Allow team members",
      "decision": "allow",
      "include": [{
        "email_domain": {"domain": "example.com"}
      }]
    }]
  }'
```

### 2. Integration with Terraform

Manage tunnels as infrastructure-as-code.

```hcl
# Provider configuration
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# Create tunnel
resource "cloudflare_tunnel" "app_tunnel" {
  account_id = var.cloudflare_account_id
  name       = "app-tunnel"
  secret     = var.tunnel_secret
}

# Configure tunnel
resource "cloudflare_tunnel_config" "app_tunnel_config" {
  account_id = var.cloudflare_account_id
  tunnel_id  = cloudflare_tunnel.app_tunnel.id

  config {
    ingress_rule {
      hostname = "app.example.com"
      service  = "http://localhost:8080"
      
      origin_request {
        connect_timeout      = "30s"
        no_tls_verify        = false
        http2_origin         = true
        keep_alive_timeout   = "90s"
        keep_alive_connections = 100
      }
    }

    ingress_rule {
      service = "http_status:404"
    }
  }
}

# Create DNS record
resource "cloudflare_record" "app_tunnel_dns" {
  zone_id = var.cloudflare_zone_id
  name    = "app"
  value   = "${cloudflare_tunnel.app_tunnel.id}.cfargotunnel.com"
  type    = "CNAME"
  proxied = true
}

# Create Access application
resource "cloudflare_access_application" "app_access" {
  account_id = var.cloudflare_account_id
  name       = "Internal App"
  domain     = "app.example.com"
  
  session_duration = "24h"
  
  cors_headers {
    allow_all_origins = false
    allowed_origins   = ["https://app.example.com"]
  }
}

# Access policy
resource "cloudflare_access_policy" "app_policy" {
  account_id     = var.cloudflare_account_id
  application_id = cloudflare_access_application.app_access.id
  name           = "Allow employees"
  precedence     = 1
  decision       = "allow"

  include {
    email_domain = ["example.com"]
  }
}

# Output tunnel token for cloudflared
output "tunnel_token" {
  value     = cloudflare_tunnel.app_tunnel.tunnel_token
  sensitive = true
}
```

**Deploy with Tunnel Token:**
```bash
# Get tunnel token from Terraform output
TUNNEL_TOKEN=$(terraform output -raw tunnel_token)

# Run cloudflared with token (no config file needed)
cloudflared tunnel --no-autoupdate run --token ${TUNNEL_TOKEN}
```

### 3. Integration with Monitoring and Logging

Monitor tunnel health and performance.

**Metrics Collection:**
```yaml
# config.yml with metrics enabled
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json
metrics: localhost:2000

ingress:
  - hostname: app.example.com
    service: http://localhost:8080
  - service: http_status:404
```

**Prometheus Scraping:**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'cloudflared'
    static_configs:
      - targets: ['localhost:2000']
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'cloudflared_.*'
        action: keep
```

**Grafana Dashboard:**
```json
{
  "dashboard": {
    "title": "Cloudflare Tunnel Metrics",
    "panels": [
      {
        "title": "Active Connections",
        "targets": [{
          "expr": "cloudflared_tunnel_ha_connections"
        }]
      },
      {
        "title": "Request Rate",
        "targets": [{
          "expr": "rate(cloudflared_tunnel_requests_total[5m])"
        }]
      },
      {
        "title": "Response Time",
        "targets": [{
          "expr": "histogram_quantile(0.95, cloudflared_tunnel_request_duration_seconds_bucket)"
        }]
      }
    ]
  }
}
```

**Log Forwarding:**
```yaml
# config.yml with structured logging
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json
loglevel: info
logfile: /var/log/cloudflared.log

ingress:
  - hostname: app.example.com
    service: http://localhost:8080
  - service: http_status:404
```

## Best Practices

### 1. Security Hardening

- **Rotate Credentials**: Regularly rotate tunnel credentials
- **Least Privilege**: Grant minimal permissions to service accounts
- **Network Segmentation**: Isolate tunnel endpoints in dedicated VLANs
- **TLS Verification**: Always verify origin TLS certificates in production
- **Access Policies**: Implement strict Zero Trust access controls

### 2. High Availability

- **Multiple Replicas**: Deploy at least 2 tunnel replicas per environment
- **Geographic Distribution**: Spread replicas across availability zones
- **Health Monitoring**: Implement automated health checks
- **Graceful Degradation**: Configure fallback services
- **Auto-Recovery**: Use systemd or container orchestration for auto-restart

### 3. Performance Optimization

- **HTTP/2**: Enable HTTP/2 to origin for multiplexing
- **Connection Pooling**: Configure appropriate keepAlive settings
- **Compression**: Enable compression at origin
- **Caching**: Leverage Cloudflare's edge caching
- **Regional Routing**: Deploy tunnels close to origin services

### 4. Configuration Management

- **Version Control**: Store configs in Git
- **Environment Separation**: Use separate tunnels for dev/staging/prod
- **Automated Deployment**: Use CI/CD for tunnel configuration updates
- **Documentation**: Maintain up-to-date topology diagrams
- **Change Management**: Implement approval workflow for config changes

### 5. Monitoring and Alerting

- **Metrics Dashboard**: Create comprehensive monitoring dashboards
- **Alert Thresholds**: Set alerts for connection drops and errors
- **Log Aggregation**: Centralize logs for analysis
- **Performance Baselines**: Establish and monitor SLIs/SLOs
- **Incident Response**: Develop runbooks for common issues

## Troubleshooting

### Issue: Tunnel Won't Start

**Symptoms:**
- `cloudflared` exits immediately
- Authentication errors
- Configuration validation failures

**Solutions:**
```bash
# Check authentication
ls -la ~/.cloudflared/cert.pem
# If missing, re-authenticate:
cloudflared tunnel login

# Validate configuration
cloudflared tunnel --config /path/to/config.yml ingress validate

# Check credentials file permissions
chmod 600 ~/.cloudflared/*.json

# Run with verbose logging
cloudflared tunnel --config /path/to/config.yml --loglevel debug run my-tunnel

# Check for port conflicts
sudo lsof -i :7844  # Default metrics port
```

### Issue: 502 Bad Gateway

**Symptoms:**
- Cloudflare returns 502 error
- Origin unreachable
- DNS resolution failures

**Solutions:**
```bash
# Verify tunnel is running
cloudflared tunnel list
# Should show active connections

# Check origin service is accessible from tunnel host
curl http://localhost:8080

# Verify DNS record
dig app.example.com
# Should resolve to *.cfargotunnel.com

# Check ingress configuration
cloudflared tunnel --config /path/to/config.yml ingress validate

# Test specific route
cloudflared tunnel --config /path/to/config.yml ingress rule https://app.example.com

# Review tunnel logs
journalctl -u cloudflared -f
```

### Issue: Connection Drops

**Symptoms:**
- Intermittent connectivity
- Tunnel shows 0 connections
- Timeout errors

**Solutions:**
```yaml
# Optimize connection settings in config.yml
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json
protocol: quic  # Or http2 for stability

ingress:
  - hostname: app.example.com
    service: http://localhost:8080
    originRequest:
      connectTimeout: 30s
      tcpKeepAlive: 30s
      keepAliveTimeout: 90s
      keepAliveConnections: 100
      noHappyEyeballs: false
  - service: http_status:404
```

```bash
# Check network connectivity
cloudflared tunnel --config /path/to/config.yml run --protocol http2

# Monitor metrics
curl http://localhost:2000/metrics | grep cloudflared_tunnel

# Check system resources
top -p $(pgrep cloudflared)
```

### Issue: Slow Performance

**Symptoms:**
- High latency
- Slow page loads
- Request timeouts

**Solutions:**
```yaml
# Optimize configuration
tunnel: my-tunnel-uuid
credentials-file: /path/to/credentials.json
no-autoupdate: true
retries: 5
grace-period: 30s

ingress:
  - hostname: app.example.com
    service: http://localhost:8080
    originRequest:
      http2Origin: true
      noTLSVerify: false
      disableChunkedEncoding: false
      connectTimeout: 10s
  - service: http_status:404
```

```bash
# Deploy additional tunnel replicas
# On server 2:
cloudflared tunnel --config /path/to/config.yml run my-tunnel

# Enable compression at origin
# Configure caching headers in application

# Monitor performance metrics
curl http://localhost:2000/metrics | grep request_duration
```

## See Also

- **[Cloudflare Zero Trust](cloudflare-zero-trust.md)** - Identity-aware access control and policies
- **[Cloudflare WARP](cloudflare-warp.md)** - Client application for Zero Trust network access
- **[Cloudflare Access](cloudflare-access.md)** - Application-level authentication and authorization
- **[Cloudflare Load Balancing](cloudflare-load-balancing.md)** - Global load balancing for tunnel origins
- **[Cloudflare DNS](cloudflare-dns.md)** - DNS management for tunnel routing
