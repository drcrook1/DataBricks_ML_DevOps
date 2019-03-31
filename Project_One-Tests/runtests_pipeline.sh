#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# -e: immediately exit if any command has a non-zero exit status
# -o: prevents errors in a pipeline from being masked
# IFS new value is less likely to cause confusing bugs when looping arrays or arguments (e.g. $@)

cd ml_temp/artifacts
str=$(jq -r '.image_location' artifacts.json)

echo "################### Image to be tested ################### : " $str
cd /
cd $(System.DefaultWorkingDirectory)/Project_One-Tests
echo "################### Updating Tests Docker File ################### "
sed "s|<AZMLGENERATEDCONTAINER>|${str}|g" dockerfile.base > dockerfile

echo "################### Logging into ACR ################### "
docker login $ACR_NAME -u $ACR_USER -p $ACR_PASSWORD 
echo "################### Building MLTESTS Image ################### "
docker build -t mltests .
echo "################### Running MLTests Container and Conducting Tests ################### "
docker run --name mltests -v $(Agent.HomeDirectory)/ml_temp/artifacts/test_results:/var/azureml-app/tests/junit mltests
echo "################### Ending Test Sequence ################### "
sudo chown -R $(id -u):$(id -u) $(Agent.HomeDirectory)/ml_temp/artifacts/test_results/cov_html/
