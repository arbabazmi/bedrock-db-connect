@echo off
REM Deployment script for AWS Lambda (Windows)

REM Create deployment directory
if exist deployment rmdir /s /q deployment
mkdir deployment
cd deployment

REM Copy lambda_function.py to root
copy ..\lambda_function.py .

REM Copy all Python files from src directory to root level (flatten structure)
copy ..\src\*.py .

REM Install dependencies if any (excluding boto3 as it's provided by Lambda)
REM Since boto3 is the only dependency and it's provided by Lambda, we skip this step
REM If you had other dependencies, you would run:
REM pip install -r ..\requirements.txt -t .

REM Create ZIP file using PowerShell
powershell -command "Compress-Archive -Path .\* -DestinationPath ..\lambda-deployment.zip -Force"

REM Clean up
cd ..
rmdir /s /q deployment

echo Deployment package created: lambda-deployment.zip
echo Files included at root level for Lambda compatibility
echo You can now upload this ZIP file to AWS Lambda
