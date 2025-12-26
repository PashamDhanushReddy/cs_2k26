@echo off
echo 🚀 CodeStorm 2026 S3 Environment Setup
echo ========================================
echo.
echo This batch file will help you set up AWS S3 environment variables.
echo.
echo ⚠️  You need to edit this file with your actual AWS credentials!
echo.
echo 1. Edit this file and replace the placeholder values with your actual:
echo    - AWS Access Key ID
echo    - AWS Secret Access Key
echo    - S3 Bucket Name (default: codestorm2026-ppts)
echo    - AWS Region (default: us-east-1)
echo    - Neon Database URL
echo.
echo 2. Run this batch file to set the variables
echo 3. Deploy your application
echo.
echo 📋 Instructions:
echo - Get AWS credentials from: https://console.aws.amazon.com/iam/
echo - Create S3 bucket at: https://s3.console.aws.amazon.com/s3/
echo - Check MANUAL_S3_SETUP.md for detailed steps
echo.

REM Replace these with your actual values:
set AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_HERE
set AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY_HERE
set AWS_STORAGE_BUCKET_NAME=codestorm2026-ppts
set AWS_REGION=us-east-1
set NEON_DATABASE_URL=YOUR_NEON_DATABASE_URL_HERE

echo ✅ Environment variables set!
echo.
echo Current values (masked):
echo AWS_ACCESS_KEY_ID: %AWS_ACCESS_KEY_ID:~0,4%****
echo AWS_SECRET_ACCESS_KEY: %AWS_SECRET_ACCESS_KEY:~0,4%****
echo AWS_STORAGE_BUCKET_NAME: %AWS_STORAGE_BUCKET_NAME%
echo AWS_REGION: %AWS_REGION%
echo NEON_DATABASE_URL: %NEON_DATABASE_URL:~0,10%****
echo.
echo 🎯 Next steps:
echo 1. Create your S3 bucket at AWS Console
echo 2. Set bucket policy for public access
echo 3. Deploy your Django application
echo 4. Test PPT upload through registration form
echo.
echo ✨ Check MANUAL_S3_SETUP.md for complete instructions!
pause