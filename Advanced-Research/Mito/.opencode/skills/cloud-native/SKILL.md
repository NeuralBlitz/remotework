-----
name: cloud-native
description: >
  Expert in cloud-native application architecture using containers, microservices, 
  and modern DevOps practices. Use this skill for designing scalable, resilient, 
  and observable cloud-native systems on Kubernetes, implementing serverless, and 
  building event-driven architectures. Covers containers, orchestration, service 
  meshes, GitOps, and cloud-native patterns.
license: MIT
compatibility: opencode
metadata:
  audience: developer, architect, devops-engineer
  category: devops
  tags: [kubernetes, containers, microservices, serverless, service-mesh, gitops]

# Cloud-Native Application Architecture

Covers: **Containerization · Kubernetes · Service Mesh · Serverless · Event-Driven · GitOps · Observability · Microservices Patterns**

-----

## Twelve-Factor App Principles

The twelve-factor app methodology provides best practices for building software-as-a-service applications:

| Factor | Principle | Implementation |
|--------|-----------|----------------|
| **Codebase** | One repo per app, multiple deploys | Monorepo or separate repos per service |
| **Dependencies** | Explicitly declare, never implicit | Package managers (pip, npm, etc.) |
| **Config** | Store in environment | Environment variables, config maps |
| **Backing Services** | Treat as attached resources | Databases, caches as services |
| **Build/Release/Run** | Strict separation | CI builds, artifact registry |
| **Processes** | Stateless, share nothing | Externalize state |
| **Port Binding** | Export via port binding | Container ports |
| **Concurrency** | Scale via process model | Horizontal scaling |
| **Disposability** | Fast startup/shutdown | Graceful termination |
| **Dev/Prod Parity** | Keep environments similar | Container parity |
| **Logs** | Treat as event streams | Structured logging |
| **Admin Processes** | Run same as processes | One-off tasks in containers |

```python
# Example: Environment-based configuration
import os
import json

class CloudNativeConfig:
    """Configuration following twelve-factor app principles"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from environment"""
        return {
            # Database configuration
            'database_url': os.environ.get('DATABASE_URL'),
            'database_pool_size': int(os.environ.get('DB_POOL_SIZE', '10')),
            'database_timeout': int(os.environ.get('DB_TIMEOUT', '30')),
            
            # Redis/cache configuration
            'redis_url': os.environ.get('REDIS_URL'),
            'cache_ttl': int(os.environ.get('CACHE_TTL', '300')),
            
            # Service configuration
            'service_name': os.environ.get('SERVICE_NAME', 'app'),
            'log_level': os.environ.get('LOG_LEVEL', 'INFO'),
            'port': int(os.environ.get('PORT', '8080')),
            
            # Feature flags
            'features': json.loads(os.environ.get('FEATURES', '{}'))
        }
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
```

-----

## Container Best Practices

### Dockerfile Optimization

```dockerfile
# Multi-stage build for Python
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Production image
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Set permissions
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Run the application
CMD ["python", "main.py"]
```

### Container Security

```yaml
# Kubernetes security context
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10000
    runAsGroup: 10000
    fsGroup: 10000
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "256Mi"
        cpu: "500m"
```

-----

## Kubernetes Architecture

### Deployment Patterns

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: myapp-config
              key: database_url
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
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
        startupProbe:
          httpGet:
            path: /health
            port: 8080
          failureThreshold: 30
          periodSeconds: 10
```

### Service Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: 9090

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  externalTrafficPolicy: Local
```

-----

## Service Mesh Integration

### Istio Configuration

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: myapp
        subset: v2
      weight: 100
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http2MaxRequests: 1000
    loadBalancer:
      simple: LEAST_CONN
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: myapp-auth
spec:
  selector:
    matchLabels:
      app: myapp
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/myapp"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/*"]
```

### Traffic Management

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: myapp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "myapp.example.com"
    tls:
      httpsRedirect: true
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "myapp.example.com"
    tls:
      mode: SIMPLE
      credentialName: myapp-tls

---
apiVersion: networking.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
```

-----

## Observability Stack

### Prometheus Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    alerting:
      alertmanagers:
      - static_configs:
        - targets: ['alertmanager:9093']
    rule_files:
    - '/etc/prometheus/rules/*.yml'
    scrape_configs:
    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - default
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    - job_name: 'kubernetes-nodes'
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Grafana Dashboard

```yaml
apiVersion: integreatly.org/v1alpha1
kind: GrafanaDashboard
metadata:
  name: myapp-dashboard
spec:
  json: |
    {
      "dashboard": {
        "title": "MyApp Metrics",
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])",
                "legendFormat": "{{method}} {{path}}"
              }
            ]
          },
          {
            "title": "Latency (p50, p95, p99)",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "p50"
              },
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "p95"
              },
              {
                "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "p99"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
                "legendFormat": "{{status}}"
              }
            ]
          }
        ]
      }
    }
```

### Distributed Tracing

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-collector
spec:
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
          http:
      jaeger:
        protocols:
          grpc:
          thrift_http:
    processors:
      batch:
        timeout: 1s
        send_batch_size: 1024
      memory_limiter:
        limit_mib: 400
    exporters:
      jaeger:
        endpoint: jaeger:14250
        tls:
          insecure: true
      prometheus:
        endpoint: "0.0.0.0:8889"
    service:
      pipelines:
        traces:
          receivers: [otlp, jaeger]
          processors: [batch, memory_limiter]
          exporters: [jaeger]
        metrics:
          receivers: [otlp]
          processors: [batch, memory_limiter]
          exporters: [prometheus]
```

-----

## Cloud-Native Patterns

### Sidecar Pattern

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-with-sidecar
spec:
  containers:
  - name: myapp
    image: myapp:latest
    ports:
    - containerPort: 8080
  - name: proxy
    image: envoyproxy/envoy:latest
    volumeMounts:
    - name: envoy-config
      mountPath: /etc/envoy
  volumes:
  - name: envoy-config
    configMap:
      name: envoy-config
```

### Ambassador Pattern

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-with-ambassador
spec:
  containers:
  - name: myapp
    image: myapp:latest
  - name: redis-proxy
    image: redis:alpine
    command: ["redis-server", "--proxy", "ambassador"]
    env:
    - name: REDIS_HOST
      value: "redis-master"
```

### Adapter Pattern

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legacy-app
spec:
  template:
    spec:
      containers:
      - name: legacy-app
        image: legacy:v1
      - name: metrics-adapter
        image: prometheus-adapter:latest
        volumeMounts:
        - name: adapter-config
          mountPath: /config
      volumes:
      - name: adapter-config
        configMap:
          name: adapter-config
```

### Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp-circuit-breaker
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

-----

## GitOps Workflow

### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp-gitops.git
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Flux Configuration

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta1
GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m0s
  url: https://github.com/myorg/myapp-gitops.git
  ref:
    branch: main

---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m0s
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./k8s/overlays/production
  prune: true
  validation: client
```

-----

## Serverless Patterns

### AWS Lambda Function

```python
import json
import boto3

def handler(event, context):
    """
    AWS Lambda handler function
    """
    # Parse event
    http_method = event.get('httpMethod')
    path = event.get('path')
    body = event.get('body')
    
    # Process request
    response = process_request(http_method, path, body)
    
    return {
        'statusCode': response.get('statusCode', 200),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response.get('body', {}))
    }

def process_request(method, path, body):
    """Route and process request"""
    
    routes = {
        ('GET', '/items'): get_items,
        ('POST', '/items'): create_item,
        ('GET', '/items/{id}'): get_item,
        ('PUT', '/items/{id}'): update_item,
        ('DELETE', '/items/{id}'): delete_item
    }
    
    handler = routes.get((method, path))
    
    if handler:
        return handler(body)
    
    return {'statusCode': 404, 'body': {'error': 'Not found'}}

def get_items(body):
    """Get all items"""
    # Implement retrieval logic
    return {'statusCode': 200, 'body': {'items': []}}
```

### Kubernetes Knative Service

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
        autoscaling.knative.dev/target: "100"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: myapp:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
```

-----

## Event-Driven Architecture

### Message Queue Patterns

```python
import pika
import json

class EventPublisher:
    """Publish events to message queue"""
    
    def __init__(self, rabbitmq_url: str):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()
    
    def publish(self, exchange: str, routing_key: str, message: dict):
        """Publish message to exchange"""
        
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent
                content_type='application/json',
                headers={
                    'event_type': message.get('type', 'unknown'),
                    'timestamp': message.get('timestamp')
                }
            )
        )
    
    def close(self):
        self.connection.close()


class EventConsumer:
    """Consume events from message queue"""
    
    def __init__(self, rabbitmq_url: str, queue: str):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()
        self.queue = queue
    
    def consume(self, callback, exchange: str, routing_keys: list):
        """Start consuming messages"""
        
        # Declare exchange
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type='topic',
            durable=True
        )
        
        # Declare queue
        self.channel.queue_declare(queue=self.queue, durable=True)
        
        # Bind to routing keys
        for key in routing_keys:
            self.channel.queue_bind(
                exchange=exchange,
                queue=self.queue,
                routing_key=key
            )
        
        # Set QoS
        self.channel.basic_qos(prefetch_count=10)
        
        # Start consuming
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback,
            auto_ack=False
        )
        
        self.channel.start_consuming()
    
    def acknowledge(self, delivery_tag):
        """Acknowledge message processing"""
        self.channel.basic_ack(delivery_tag=delivery_tag)
```
