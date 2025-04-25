#!/bin/bash

# Exit if any command fails
set -e

echo "⚡ Tearing down the AWS infrastructure..."

# Go to terraform directory
cd ../terraform

# Destroy Terraform-managed infrastructure
terraform destroy -auto-approve

echo "AWS resources destroyed."
