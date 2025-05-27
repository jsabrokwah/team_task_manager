#!/bin/bash

# Script to deploy static website files to S3 bucket after SAM deployment

# Get the S3 bucket name from CloudFormation outputs
STACK_NAME=$1
if [ -z "$STACK_NAME" ]; then
  echo "Usage: $0 <stack-name>"
  exit 1
fi

# Get the S3 bucket name from CloudFormation outputs
S3_BUCKET=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='WebsiteURL'].OutputValue" --output text | sed 's/http:\/\///' | sed 's/\/.*//')

if [ -z "$S3_BUCKET" ]; then
  echo "Could not find S3 bucket in CloudFormation outputs"
  exit 1
fi

echo "Deploying static website files to S3 bucket: $S3_BUCKET"

# Deploy static website files to S3 bucket
aws s3 sync static-site/ s3://$S3_BUCKET/ --delete

# Set content types for files
aws s3 cp s3://$S3_BUCKET/js/ s3://$S3_BUCKET/js/ --recursive --content-type "application/javascript" --metadata-directive REPLACE
aws s3 cp s3://$S3_BUCKET/css/ s3://$S3_BUCKET/css/ --recursive --content-type "text/css" --metadata-directive REPLACE
aws s3 cp s3://$S3_BUCKET/*.html s3://$S3_BUCKET/ --recursive --content-type "text/html" --metadata-directive REPLACE

echo "Static website deployment complete"
echo "Website URL: http://$S3_BUCKET.s3-website-$(aws configure get region).amazonaws.com"

# Get the API endpoint from CloudFormation outputs
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)

echo "API Endpoint: $API_ENDPOINT"
echo "Update the config.js file with this API endpoint"