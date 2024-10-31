#!/bin/bash

# Apply the Kubernetes configuration
kubectl apply -f vllm-gemma2-2b.yaml

# Check if the command was successful
if [ $? -eq 0 ];
then
  echo "Kubernetes configuration applied successfully."
else
  echo "Failed to apply Kubernetes configuration."
  exit 1
fi

# wait 10 seconds for the deployment to be ready
echo "Waiting 30s for the deployment to be ready..."
sleep 30

# Check if the deployment is ready
kubectl logs -f -l app=gemma2-server
