---
name: kubernetes-orchestrator
description: Orchestrate Kubernetes clusters and workloads — deployment management, resource configuration, and cluster operations. Use when deploying applications to K8s, troubleshooting pod issues, scaling workloads, configuring ingress and services, managing namespaces, or setting up cluster autoscaling and resource quotas.
---

# kubernetes-orchestrator

Deploy, manage, and troubleshoot Kubernetes workloads with production-grade configurations.

## When to Use

Invoke this skill when you need to:
- **Deploy applications** to Kubernetes clusters with proper manifests
- **Troubleshoot** failing pods, services, or deployments
- **Scale workloads** horizontally or vertically
- **Configure networking** (Services, Ingress, NetworkPolicies)
- **Manage resources** (ConfigMaps, Secrets, PVCs)
- **Set up monitoring** and health checks
- **Optimize** resource requests and limits
- **Implement** blue-green or canary deployments
- **Debug** cluster issues and performance problems

## Quick Start

### Deploy a Simple Application

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v1.0.0
    spec:
      containers:
      - name: web-app
        image: myregistry.io/web-app:v1.0.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: connection-string
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  namespace: production
spec:
  selector:
    app: web-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: web-app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
```

## Common Scenarios

### Scenario 1: StatefulSet with Persistent Storage

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: database
spec:
  ports:
  - port: 5432
    name: postgres
  clusterIP: None
  selector:
    app: postgres
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: database
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 20Gi
```

### Scenario 2: CronJob for Scheduled Tasks

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: jobs
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: myregistry.io/db-backup:latest
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: connection-string
            - name: S3_BUCKET
              value: "backups.example.com"
            resources:
              requests:
                memory: "512Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "500m"
```

### Scenario 3: HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
```

### Scenario 4: NetworkPolicy for Security

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-app-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: monitoring
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```

## Troubleshooting Guide

### Pod Stuck in Pending

```bash
# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# 1. Insufficient resources - check node capacity
kubectl top nodes

# 2. PVC not bound - check persistent volumes
kubectl get pvc -n <namespace>

# 3. Node selector mismatch - verify labels
kubectl get nodes --show-labels
```

### CrashLoopBackOff

```bash
# View container logs
kubectl logs <pod-name> -n <namespace> --previous

# Check resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Limits"

# Common fixes:
# - Increase memory/CPU limits
# - Fix application startup issues
# - Verify environment variables
```

### ImagePullBackOff

```bash
# Check image pull secrets
kubectl get secrets -n <namespace>

# Verify image exists
docker pull <image-name>

# Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  -n <namespace>
```

### Service Not Reachable

```bash
# Verify service endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check pod labels match service selector
kubectl get pods -n <namespace> --show-labels

# Test connectivity from another pod
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
wget -O- http://<service-name>.<namespace>.svc.cluster.local
```

## Best Practices

### Resource Management
- **Always set** resource requests and limits
- **Requests** should match typical usage (95th percentile)
- **Limits** should allow for traffic spikes (2-3x requests)
- Use **VerticalPodAutoscaler** for right-sizing

### Health Checks
- **Liveness probes** detect and restart frozen containers
- **Readiness probes** prevent traffic to unready pods
- **Startup probes** handle slow-starting applications
- Set appropriate `initialDelaySeconds` and timeouts

### Security
- Run containers as **non-root** user
- Use **read-only** root filesystems where possible
- Implement **NetworkPolicies** to restrict traffic
- Scan images for vulnerabilities regularly
- Use **PodSecurityPolicies** or **PodSecurityStandards**

### High Availability
- Deploy at least **3 replicas** for critical services
- Use **PodDisruptionBudgets** to ensure availability during updates
- Spread pods across **availability zones** with topology constraints
- Implement **circuit breakers** at application level

### Configuration Management
- Use **ConfigMaps** for non-sensitive configuration
- Store secrets in **Secrets** or external secret managers
- Version control all manifests in Git
- Use **Kustomize** or **Helm** for environment-specific configs

## Advanced Patterns

### Blue-Green Deployment

```yaml
# Blue deployment (current)
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    version: blue
  ports:
  - port: 80

---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v2.0.0

# Switch traffic by updating service selector
kubectl patch service app-service -p '{"spec":{"selector":{"version":"green"}}}'
```

### Canary Deployment with Flagger

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: web-app
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
```

## Performance Optimization

### Resource Quotas per Namespace

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "50"
    pods: "100"
```

### Pod Priority Classes

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "High priority for critical workloads"
---
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  priorityClassName: high-priority
  containers:
  - name: app
    image: myapp:latest
```

## Related Skills

- **helm-packager**: Package K8s applications with Helm charts
- **service-mesh-configurator**: Set up Istio or Linkerd
- **cluster-autoscaler**: Configure automatic node scaling
- **monitoring-configurator**: Set up Prometheus for K8s
- **gitops-deployer**: Implement ArgoCD or Flux workflows
- **container-scanner**: Scan images for vulnerabilities
- **secrets-manager**: Integrate external secret stores

## Useful Commands

```bash
# Get cluster info
kubectl cluster-info
kubectl get nodes -o wide

# View all resources in namespace
kubectl get all -n <namespace>

# Watch pod status
kubectl get pods -n <namespace> -w

# Port forward for local testing
kubectl port-forward svc/<service-name> 8080:80 -n <namespace>

# Execute command in pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Copy files to/from pod
kubectl cp <local-file> <namespace>/<pod-name>:/path/to/file
kubectl cp <namespace>/<pod-name>:/path/to/file <local-file>

# View resource usage
kubectl top pods -n <namespace>
kubectl top nodes

# Drain node for maintenance
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -k ./kustomize-dir

# Rollback deployment
kubectl rollout undo deployment/<name> -n <namespace>
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout history deployment/<name> -n <namespace>
```

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Best Practices Guide](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Production Best Practices](https://learnk8s.io/production-best-practices)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
