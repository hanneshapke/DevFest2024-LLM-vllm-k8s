#!/bin/bash

# Update package lists
sudo apt-get update

# Install Google Cloud CLI GKE gcloud auth plugin
sudo apt-get install -y google-cloud-cli-gke-gcloud-auth-plugin

# Install kubectl
sudo apt-get install -y kubectl
