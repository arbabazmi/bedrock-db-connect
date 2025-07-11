#!/bin/bash
# Deployment script for AWS Lambda

# Create deployment directory
mkdir -p deployment
cd deployment

# Copy lambda_function.py to root
cp ../lambda_function.py .

# Copy all Python files from src directory to root level (flatten structure)
cp ../src/*.py .

# Install dependencies if any (excluding boto3 as it's provided by Lambda)
# Since boto3 is the only dependency and it's provided by Lambda, we skip this step
# If you had other dependencies, you would run:
# pip install -r ../requirements.txt -t .

# Create ZIP file
zip -r ../lambda-deployment.zip .

# Clean up
cd ..
rm -rf deployment

echo "Deployment package created: lambda-deployment.zip"
echo "Files included at root level for Lambda compatibility"
echo "You can now upload this ZIP file to AWS Lambda"
