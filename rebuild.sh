#!/bin/bash

# Configuration
APP_NAME="dictionary-api"
NAMESPACE="dictionary-api"
IMAGE_NAME="kubernetes-python-tasks"
TAG="latest"

echo "🚀 Starting rebuild process for $APP_NAME..."

# 1. Build the image locally
# Using 'docker' or 'nerdctl' depending on your Rancher Desktop settings
echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME:$TAG .

# 2. If using Rancher Desktop/k3s, we need to ensure the image is available to the cluster
# This step is crucial if your api-deployment.yaml has 'imagePullPolicy: Never'
echo "syncing image to local cluster..."
# For Rancher Desktop (k3s), this is the common way to import images:
# docker save $IMAGE_NAME:$TAG | sudo k3s ctr images import -

# 3. Force Kubernetes to restart the pods to pick up the new build
echo "🔄 Restarting deployment..."
kubectl rollout restart deployment $APP_NAME -n $NAMESPACE

# 4. Wait for the new pod to be ready
echo "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment $APP_NAME -n $NAMESPACE

echo "✅ Rebuild complete! Tracking logs..."
kubectl logs -f -l app=$APP_NAME -n $NAMESPACE --tail=20
