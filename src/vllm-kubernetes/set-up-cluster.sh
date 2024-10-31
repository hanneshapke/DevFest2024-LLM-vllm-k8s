#!/bin/bash

# Set variables
PROJECT_ID=<YOUR GCP PROJECT>
CLUSTER_NAME=<YOUR CLUSTER NAME>
REGION=<GCP REGION>
INSTANCE_TYPE=g2-standard-8
NUM_NODES=1
ZONE=${REGION}-a
HF_TOKEN=<YOUR HUGGINGFACE TOKEN>

# Authenticate with Google Cloud
gcloud auth login --no-browser

# Set the project
gcloud config set project $PROJECT_ID

# Create the Kubernetes cluster
gcloud container clusters create ${CLUSTER_NAME} \
  --project=${PROJECT_ID} \
  --zone=${ZONE} \
  --workload-pool=${PROJECT_ID}.svc.id.goog \
  --release-channel=rapid \
  --num-nodes=${NUM_NODES}

# Create a GPU node pool
gcloud container node-pools create gpupool \
  --accelerator type=nvidia-l4,count=1,gpu-driver-version=latest \
  --project=${PROJECT_ID} \
  --location=${REGION} \
  --node-locations=${ZONE} \
  --cluster=${CLUSTER_NAME} \
  --machine-type=${INSTANCE_TYPE} \
  --num-nodes=${NUM_NODES}

# Get credentials for kubectl
gcloud container clusters get-credentials \
  ${CLUSTER_NAME} \
  --location=${REGION} \
  --project=${PROJECT_ID}

# Create a secret for the Hugging Face API token
kubectl create secret generic hf-secret \
--from-literal=hf_api_token=${HF_TOKEN} \
--dry-run=client -o yaml | kubectl apply -f -

# Verify the cluster is running
kubectl get nodes

echo "Kubernetes cluster $CLUSTER_NAME set up successfully in project $PROJECT_ID."
