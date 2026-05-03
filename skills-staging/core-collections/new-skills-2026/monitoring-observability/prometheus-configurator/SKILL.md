---
name: prometheus-configurator
description: Configure Prometheus for metrics collection — scraping, alerting rules, recording rules, and service discovery. Use when setting up monitoring infrastructure, creating custom metrics, defining SLIs/SLOs, building dashboards, or implementing alerting strategies for production systems.
---

# prometheus-configurator

Configure and manage Prometheus monitoring infrastructure with production-grade best practices.

## When to Use

Invoke this skill when you need to:
- **Set up Prometheus** for metrics collection and monitoring
- **Configure scrape targets** with service discovery
- **Create alerting rules** for proactive monitoring
- **Define recording rules** for performance optimization
- **Instrument applications** with custom metrics
- **Integrate** with Grafana, AlertManager, or other tools
- **Troubleshoot** metrics collection or alerting issues
- **Optimize** Prometheus performance and storage

## Quick Start

### Basic Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

# AlertManager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 'alertmanager:9093'

# Load rules
rule_files:
  - 'alerts/*.yml'
  - 'rules/*.yml'

# Scrape configurations
scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  # Node Exporter for system metrics
  - job_name: 'node-exporter'
    static_configs:
      - targets:
          - 'node1:9100'
          - 'node2:9100'
          - 'node3:9100'
    relabel_configs:
      - source_labels: [__address__]
        regex: '([^:]+):.*'
        target_label: instance
        replacement: '${1}'
  
  # Application metrics
  - job_name: 'web-app'
    static_configs:
      - targets:
          - 'app1:8080'
          - 'app2:8080'
          - 'app3:8080'
    metrics_path: '/metrics'
    params:
      format: ['prometheus']
```

### Kubernetes Service Discovery

```yaml
scrape_configs:
  # Kubernetes API Server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https
  
  # Kubernetes Nodes
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
  
  # Kubernetes Pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
```

## Common Scenarios

### Scenario 1: Application Instrumentation

**Go Application with Prometheus Client**

```go
package main

import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    // Counter: monotonically increasing value
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )
    
    // Histogram: request duration distribution
    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
    
    // Gauge: current value that can go up or down
    activeConnections = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "active_connections",
            Help: "Number of active connections",
        },
    )
    
    // Summary: sliding time window of observations
    cacheHitRatio = promauto.NewSummary(
        prometheus.SummaryOpts{
            Name:       "cache_hit_ratio",
            Help:       "Cache hit ratio",
            Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
        },
    )
)

func instrumentedHandler(w http.ResponseWriter, r *http.Request) {
    timer := prometheus.NewTimer(httpRequestDuration.WithLabelValues(r.Method, r.URL.Path))
    defer timer.ObserveDuration()
    
    activeConnections.Inc()
    defer activeConnections.Dec()
    
    // Handler logic here
    status := http.StatusOK
    w.WriteHeader(status)
    
    httpRequestsTotal.WithLabelValues(r.Method, r.URL.Path, string(status)).Inc()
}

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.HandleFunc("/api/users", instrumentedHandler)
    http.ListenAndServe(":8080", nil)
}
```

**Python Application with Prometheus Client**

```python
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
from flask import Flask, request
import time

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'active_requests',
    'Number of active requests'
)

CACHE_SIZE = Gauge(
    'cache_size_bytes',
    'Cache size in bytes'
)

@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    ACTIVE_REQUESTS.dec()
    return response

@app.route('/api/users')
def get_users():
    return {"users": []}

if __name__ == '__main__':
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    # Start Flask app on port 5000
    app.run(port=5000)
```

### Scenario 2: Alerting Rules

```yaml
# alerts/application.yml
groups:
  - name: application_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          component: application
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "{{ $labels.service }} has error rate of {{ $value | humanizePercentage }} (threshold: 5%)"
          runbook_url: "https://wiki.company.com/runbooks/high-error-rate"
      
      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1.0
        for: 10m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High latency on {{ $labels.service }}"
          description: "{{ $labels.service }} p95 latency is {{ $value }}s (threshold: 1s)"
      
      # Service down
      - alert: ServiceDown
        expr: up{job="web-app"} == 0
        for: 2m
        labels:
          severity: critical
          component: infrastructure
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.job }} on {{ $labels.instance }} has been down for more than 2 minutes"
      
      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          (
            node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
          ) / node_memory_MemTotal_bytes > 0.90
        for: 5m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanizePercentage }} on {{ $labels.instance }}"
      
      # Disk space low
      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{mountpoint="/"}
            /
            node_filesystem_size_bytes{mountpoint="/"}
          ) < 0.10
        for: 5m
        labels:
          severity: critical
          component: infrastructure
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk space is {{ $value | humanizePercentage }} available on {{ $labels.instance }}:{{ $labels.mountpoint }}"

# alerts/slo.yml
groups:
  - name: slo_alerts
    interval: 30s
    rules:
      # Error budget burn rate
      - alert: ErrorBudgetBurnRateHigh
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[1h]))
              /
              sum(rate(http_requests_total[1h]))
            )
          ) > (1 - 0.999) * 14.4
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Error budget burning too fast"
          description: "At current rate, monthly error budget will be exhausted in {{ $value }} hours"
      
      # SLO violation
      - alert: SLOViolation
        expr: |
          (
            sum(rate(http_requests_total{status!~"5.."}[30d]))
            /
            sum(rate(http_requests_total[30d]))
          ) < 0.999
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "SLO violation: Availability below 99.9%"
          description: "Current availability is {{ $value | humanizePercentage }}, below SLO of 99.9%"
```

### Scenario 3: Recording Rules

```yaml
# rules/recording.yml
groups:
  - name: recording_rules
    interval: 30s
    rules:
      # Pre-aggregate request rate by service
      - record: service:http_requests:rate5m
        expr: |
          sum(rate(http_requests_total[5m])) by (service)
      
      # Pre-aggregate error rate by service
      - record: service:http_errors:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      
      # Error ratio
      - record: service:http_error_ratio:rate5m
        expr: |
          service:http_errors:rate5m / service:http_requests:rate5m
      
      # Request latency quantiles
      - record: service:http_request_duration:p50
        expr: |
          histogram_quantile(0.50,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )
      
      - record: service:http_request_duration:p95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )
      
      - record: service:http_request_duration:p99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )
      
      # CPU utilization by node
      - record: node:cpu_utilization:ratio
        expr: |
          1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)
      
      # Memory utilization by node
      - record: node:memory_utilization:ratio
        expr: |
          1 - (
            node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
          )
      
      # Disk utilization by node and mountpoint
      - record: node:disk_utilization:ratio
        expr: |
          1 - (
            node_filesystem_avail_bytes / node_filesystem_size_bytes
          )
      
      # Network throughput
      - record: node:network_receive_bytes:rate5m
        expr: |
          sum(rate(node_network_receive_bytes_total[5m])) by (instance)
      
      - record: node:network_transmit_bytes:rate5m
        expr: |
          sum(rate(node_network_transmit_bytes_total[5m])) by (instance)
```

### Scenario 4: Federation Setup

```yaml
# Central Prometheus federating from regional instances
scrape_configs:
  - job_name: 'federate-us-east-1'
    scrape_interval: 30s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="web-app"}'
        - '{job="database"}'
        - '{__name__=~"service:.*"}'  # All recording rules
    static_configs:
      - targets:
          - 'prometheus-us-east-1:9090'
        labels:
          region: 'us-east-1'
  
  - job_name: 'federate-us-west-2'
    scrape_interval: 30s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="web-app"}'
        - '{job="database"}'
        - '{__name__=~"service:.*"}'
    static_configs:
      - targets:
          - 'prometheus-us-west-2:9090'
        labels:
          region: 'us-west-2'
```

## Best Practices

### Metric Naming Conventions

Follow Prometheus naming best practices:

```
# Counter: _total suffix
http_requests_total
database_queries_total
cache_hits_total

# Gauge: no suffix
memory_usage_bytes
active_connections
queue_size

# Histogram: _bucket, _sum, _count
http_request_duration_seconds_bucket
http_request_duration_seconds_sum
http_request_duration_seconds_count

# Summary: quantiles
http_request_size_bytes{quantile="0.5"}
http_request_size_bytes{quantile="0.9"}
http_request_size_bytes{quantile="0.99"}
```

### Label Best Practices

```yaml
# Good labels (low cardinality)
labels:
  - service: "web-app"
  - environment: "production"
  - region: "us-east-1"
  - method: "GET"
  - status: "200"

# Bad labels (high cardinality - avoid!)
# - user_id: "12345"  # Too many unique values
# - request_id: "uuid"  # Infinite cardinality
# - email: "user@example.com"  # PII and high cardinality
# - timestamp: "1234567890"  # Use Prometheus timestamp instead
```

### Storage and Retention

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

# Storage configuration
storage:
  tsdb:
    path: /prometheus/data
    retention.time: 15d  # Keep 15 days of data
    retention.size: 50GB  # Or 50GB, whichever comes first
    
# For longer retention, use remote storage
remote_write:
  - url: "https://prometheus-remote-storage.example.com/api/v1/write"
    queue_config:
      capacity: 10000
      max_shards: 50
      min_shards: 1
      max_samples_per_send: 5000
      batch_send_deadline: 5s
      min_backoff: 30ms
      max_backoff: 100ms

remote_read:
  - url: "https://prometheus-remote-storage.example.com/api/v1/read"
```

### Performance Optimization

1. **Use recording rules** for expensive queries
2. **Limit label cardinality** (< 10 values per label)
3. **Aggregate metrics** before storage
4. **Use appropriate bucket sizes** for histograms
5. **Implement relabeling** to drop unnecessary metrics
6. **Set appropriate scrape intervals** (not too frequent)

## Troubleshooting

### High Cardinality Issues

```promql
# Find metrics with high cardinality
topk(10, count by (__name__)({__name__=~".+"}))

# Find labels with many unique values
topk(10, count by (label_name)({__name__="metric_name"}))
```

### Missing Metrics

```bash
# Check service discovery
curl http://localhost:9090/api/v1/targets

# Check metric endpoints
curl http://app-server:8080/metrics

# Verify relabel configs
promtool check config prometheus.yml
```

### Memory Issues

```yaml
# Limit query concurrency
global:
  query_log_file: /prometheus/query.log

# Reduce retention
storage:
  tsdb:
    retention.time: 7d
    
# Use recording rules to pre-aggregate
rule_files:
  - 'rules/*.yml'
```

## Advanced Patterns

### Multi-Tenancy with Relabeling

```yaml
scrape_configs:
  - job_name: 'multi-tenant-apps'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Extract tenant from namespace
      - source_labels: [__meta_kubernetes_namespace]
        regex: 'tenant-(.+)'
        target_label: tenant
        replacement: '${1}'
      
      # Drop metrics from non-tenant namespaces
      - source_labels: [tenant]
        action: keep
        regex: '.+'
      
      # Add tenant to all metrics
      - source_labels: [tenant]
        target_label: tenant_id
```

### Custom Exporters

```python
# Simple custom exporter
from prometheus_client import start_http_server, Gauge
import time
import requests

# Define metrics
QUEUE_SIZE = Gauge('queue_size', 'Current queue size')
PENDING_JOBS = Gauge('pending_jobs', 'Number of pending jobs')

def collect_metrics():
    """Collect metrics from external system"""
    while True:
        try:
            # Fetch data from API
            response = requests.get('http://queue-service:8080/stats')
            data = response.json()
            
            # Update metrics
            QUEUE_SIZE.set(data['queue_size'])
            PENDING_JOBS.set(data['pending_jobs'])
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
        
        time.sleep(15)  # Collect every 15 seconds

if __name__ == '__main__':
    start_http_server(9100)
    collect_metrics()
```

### High Availability Setup

```yaml
# Two Prometheus instances with identical config
# prometheus-1.yml
global:
  external_labels:
    replica: 'prometheus-1'

# prometheus-2.yml
global:
  external_labels:
    replica: 'prometheus-2'

# Both write to same AlertManager cluster
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 'alertmanager-1:9093'
            - 'alertmanager-2:9093'
            - 'alertmanager-3:9093'
```

## Kubernetes Deployment

```yaml
# prometheus-configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true

---
# prometheus-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      serviceAccountName: prometheus
      containers:
      - name: prometheus
        image: prom/prometheus:v2.45.0
        args:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--storage.tsdb.retention.time=15d'
          - '--web.enable-lifecycle'
        ports:
        - containerPort: 9090
          name: http
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: storage
          mountPath: /prometheus
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: storage
        persistentVolumeClaim:
          claimName: prometheus-storage

---
# prometheus-service.yml
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: monitoring
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
  type: ClusterIP
```

## Useful PromQL Queries

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))

# Success rate (percentage)
(
  sum(rate(http_requests_total{status!~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
) * 100

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) 
/ node_memory_MemTotal_bytes * 100

# CPU usage percentage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Disk I/O
rate(node_disk_read_bytes_total[5m])
rate(node_disk_written_bytes_total[5m])

# Top 5 endpoints by request count
topk(5, sum(rate(http_requests_total[5m])) by (endpoint))

# Prediction (linear regression)
predict_linear(node_filesystem_avail_bytes[1h], 4 * 3600)

# Aggregation by labels
sum(rate(http_requests_total[5m])) by (service, status)

# Rate of increase
increase(http_requests_total[1h])

# Moving average
avg_over_time(metric[5m])
```

## Related Skills

- **grafana-dashboard-builder**: Visualize Prometheus metrics
- **alert-manager**: Handle Prometheus alerts
- **kubernetes-orchestrator**: Deploy Prometheus on K8s
- **elk-stack-manager**: Complement metrics with logs
- **distributed-tracer**: Add tracing to observability
- **slo-calculator**: Define SLOs using Prometheus
- **apm-integrator**: Application performance monitoring

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Best Practices](https://prometheus.io/docs/practices/)
- [Exporters and Integrations](https://prometheus.io/docs/instrumenting/exporters/)
- [Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
