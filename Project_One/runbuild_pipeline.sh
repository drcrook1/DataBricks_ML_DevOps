#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# -e: immediately exit if any command has a non-zero exit status
# -o: prevents errors in a pipeline from being masked
# IFS new value is less likely to cause confusing bugs when looping arrays or arguments (e.g. $@)

#Creating Artifact and Test Results Directories
mkdir ml_temp && cd ml_temp
mkdir artifacts && cd artifacts
mkdir test_results

#Switching to Project Directory
cd /
cd $(System.DefaultWorkingDirectory)/Project_One

#Docker Build Inf Container
echo "Building Inference Container"
docker build -t mlbuild .

#Run Built Container
echo "Running Inference Container"
docker run -e SUBSCRIPTION_ID=$(SUBSCRIPTION_ID) -e RESOURCE_GROUP=$(RESOURCE_GROUP) -e WORKSPACE_NAME=$(WORKSPACE_NAME) -e STATE=$(STATE) -e AUTHOR=$(AUTHOR) -e MODEL_NAME=$(MODEL_NAME) -e IMAGE_NAME=$(IMAGE_NAME) --name mlbuild --rm -v $(Agent.HomeDirectory)/ml_temp/artifacts:/artifacts/ -v /home/vsts/.azure/:/root/.azure/ mlbuild





