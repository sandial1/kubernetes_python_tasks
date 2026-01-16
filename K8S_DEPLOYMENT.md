# Kubernetes Deployment Guide

This document provides comprehensive instructions for deploying the Dictionary API to a Kubernetes cluster.

## Prerequisites

1. A working Kubernetes cluster (1.24+)
2. `kubectl` configured to access your cluster
3. Docker image built and available (or in a registry)
4. NGINX Ingress Controller installed (optional, for ingress support)

## Project Structure

```
k8s/
├── namespace.yaml              # Kubernetes namespace
├── configmap.yaml              # Application configuration
├── secret.yaml                 # Database credentials
├── mariadb-pvc.yaml           # PersistentVolumeClaim for MariaDB
├── mariadb-service.yaml       # Headless service for MariaDB
├── mariadb-statefulset.yaml   # MariaDB database
├── api-service.yaml           # Service for API
├── api-deployment.yaml        # FastAPI deployment
├── ingress.yaml               # Ingress configuration
└── kustomization.yaml         # Kustomize manifest
```

## Deployment Steps

### 1. Build and Push Docker Image

```bash
# Build the Docker image
docker build -t kubernetes-python-tasks:latest .

# Push to your registry (replace 'your-registry' with your actual registry)
docker tag kubernetes-python-tasks:latest your-registry/kubernetes-python-tasks:latest
docker push your-registry/kubernetes-python-tasks:latest
```

If using a private registry, update the `imagePullPolicy` and add `imagePullSecrets` in `api-deployment.yaml`.

### 2. Configure Secrets

Edit `k8s/secret.yaml` and update the credentials if needed (currently using default demo credentials):

```bash
# Encode a secret in base64
echo -n "your-password" | base64
```

Replace values in `secret.yaml` with your actual credentials.

### 3. Deploy Using Kustomize

```bash
# Apply all resources
kubectl apply -k k8s/

# Or using kustomize directly
kustomize build k8s/ | kubectl apply -f -
```

### 4. Deploy Individual Components

If you prefer to deploy components individually:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create configuration and secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Deploy MariaDB
kubectl apply -f k8s/mariadb-pvc.yaml
kubectl apply -f k8s/mariadb-service.yaml
kubectl apply -f k8s/mariadb-statefulset.yaml

# Wait for MariaDB to be ready
kubectl wait --for=condition=ready pod -l app=mariadb -n dictionary-api --timeout=300s

# Deploy API
kubectl apply -f k8s/api-service.yaml
kubectl apply -f k8s/api-deployment.yaml

# Deploy Ingress (optional)
kubectl apply -f k8s/ingress.yaml
```

## Verification

### Check Deployment Status

```bash
# Check all resources
kubectl get all -n dictionary-api

# Check pods
kubectl get pods -n dictionary-api
kubectl get pods -n dictionary-api -w  # Watch mode

# Check services
kubectl get svc -n dictionary-api

# Check StatefulSet
kubectl get statefulset -n dictionary-api

# Check PersistentVolumeClaim
kubectl get pvc -n dictionary-api
```

### View Logs

```bash
# View API logs
kubectl logs deployment/dictionary-api -n dictionary-api
kubectl logs -f deployment/dictionary-api -n dictionary-api --all-containers=true

# View MariaDB logs
kubectl logs statefulset/mariadb -n dictionary-api
kubectl logs -f statefulset/mariadb -n dictionary-api

# View logs from a specific pod
kubectl logs pod/dictionary-api-<pod-hash> -n dictionary-api
```

### Test the Application

```bash
# Port forward to the API service
kubectl port-forward -n dictionary-api svc/dictionary-api-service 8000:80

# In another terminal, test the API
curl http://localhost:8000/
curl http://localhost:8000/docs  # Swagger UI

# Test with dictionary endpoints
curl -X GET http://localhost:8000/dictionary
curl -X POST http://localhost:8000/dictionary \
  -H "Content-Type: application/json" \
  -d '{"word": "test", "definition": "a test definition"}'
```

### Check Database Connectivity

```bash
# Connect to MariaDB pod
kubectl exec -it statefulset/mariadb -n dictionary-api -- bash

# Inside the pod, connect to MySQL
mysql -u demo -pdemo -h localhost

# Run SQL commands
use demo;
show tables;
select * from words;
```

## Accessing the Application

### Using Port Forward

```bash
kubectl port-forward -n dictionary-api svc/dictionary-api-service 8000:80
# Access at http://localhost:8000
```

### Using Ingress

```bash
# Get the Ingress IP/hostname
kubectl get ingress -n dictionary-api

# Add to your /etc/hosts file (on Linux/Mac)
<ingress-ip> dictionary-api.local

# Access at http://dictionary-api.local
```

### Using LoadBalancer

To expose the service externally, change the service type in `api-service.yaml`:

```yaml
spec:
  type: LoadBalancer  # Change from ClusterIP to LoadBalancer
```

Then redeploy:

```bash
kubectl apply -f k8s/api-service.yaml
```

## Scaling

### Scale the API Deployment

```bash
# Scale to 5 replicas
kubectl scale deployment dictionary-api -n dictionary-api --replicas=5

# Or edit the deployment directly
kubectl edit deployment dictionary-api -n dictionary-api
# Change replicas field to desired number
```

### Monitor Scaling

```bash
kubectl get pods -n dictionary-api -w
```

## Updating the Application

### Update the Docker Image

```bash
# Build and push new image
docker build -t your-registry/kubernetes-python-tasks:v1.1.0 .
docker push your-registry/kubernetes-python-tasks:v1.1.0

# Update deployment
kubectl set image deployment/dictionary-api \
  api=your-registry/kubernetes-python-tasks:v1.1.0 \
  -n dictionary-api

# Or edit the deployment
kubectl edit deployment dictionary-api -n dictionary-api
```

### Rollback to Previous Version

```bash
# Check rollout history
kubectl rollout history deployment/dictionary-api -n dictionary-api

# Rollback to previous version
kubectl rollout undo deployment/dictionary-api -n dictionary-api

# Rollback to specific revision
kubectl rollout undo deployment/dictionary-api -n dictionary-api --to-revision=2
```

## Cleanup

### Delete All Resources

```bash
# Delete using kustomize
kubectl delete -k k8s/

# Or delete the namespace (deletes all resources within it)
kubectl delete namespace dictionary-api

# Delete individual resources
kubectl delete deployment dictionary-api -n dictionary-api
kubectl delete statefulset mariadb -n dictionary-api
kubectl delete service dictionary-api-service -n dictionary-api
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status and events
kubectl describe pod <pod-name> -n dictionary-api

# Check pod logs
kubectl logs pod/<pod-name> -n dictionary-api

# Check resource requests/limits
kubectl top pods -n dictionary-api
```

### Database Connection Issues

```bash
# Check if MariaDB is ready
kubectl get statefulset mariadb -n dictionary-api

# Test connectivity from API pod
kubectl exec -it deployment/dictionary-api -n dictionary-api -- bash
# Inside container:
curl http://mariadb-service.dictionary-api.svc.cluster.local:3306
```

### Ingress Not Working

```bash
# Check ingress status
kubectl get ingress -n dictionary-api
kubectl describe ingress dictionary-api-ingress -n dictionary-api

# Check NGINX controller logs (if using nginx-ingress)
kubectl logs -n ingress-nginx deployment/nginx-ingress-controller
```

## Environment Variables Reference

The API deployment uses the following environment variables:

- `DATABASE_URL`: Connection string for MariaDB (set from Secret)
- `APP_NAME`: Application name (set from ConfigMap)
- `APP_VERSION`: Application version (set from ConfigMap)

These can be modified in `k8s/secret.yaml` and `k8s/configmap.yaml` respectively.

## Advanced Configuration

### Resource Limits and Requests

Edit `api-deployment.yaml` to adjust resource allocations:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Replica Count

Edit `api-deployment.yaml` to change the number of API instances:

```yaml
replicas: 3
```

### Database Storage Size

Edit `mariadb-pvc.yaml` to adjust storage:

```yaml
resources:
  requests:
    storage: 5Gi
```

## Next Steps

For Phase 4 (Grafana Operator integration), consider adding:

- ServiceMonitor for Prometheus metrics collection
- PrometheusRule for alerting
- Grafana dashboards for visualization
- Custom metrics in the FastAPI application

For Phase 5 (Gatling performance testing), consider:

- Setting up a separate namespace for load testing
- Configuring HPA (Horizontal Pod Autoscaler) for auto-scaling
- Monitoring performance metrics during load tests
