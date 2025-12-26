# 🚀 CodeStorm 2026 S3 Setup - Simple Version
Write-Host "🚀 CodeStorm 2026 S3 PPT Upload Setup" -ForegroundColor Green
Write-Host "=" * 50

# Check environment variables
Write-Host "`n🔍 Checking Environment Variables:" -ForegroundColor Yellow

$aws_key = [Environment]::GetEnvironmentVariable("AWS_ACCESS_KEY_ID")
$aws_secret = [Environment]::GetEnvironmentVariable("AWS_SECRET_ACCESS_KEY")
$bucket = [Environment]::GetEnvironmentVariable("AWS_STORAGE_BUCKET_NAME")
$region = [Environment]::GetEnvironmentVariable("AWS_REGION")
$database = [Environment]::GetEnvironmentVariable("NEON_DATABASE_URL")

Write-Host "AWS_ACCESS_KEY_ID: $(if($aws_key){"✅ SET"}else{"❌ NOT SET"})" -ForegroundColor $(if($aws_key){"Green"}else{"Red"})
Write-Host "AWS_SECRET_ACCESS_KEY: $(if($aws_secret){"✅ SET"}else{"❌ NOT SET"})" -ForegroundColor $(if($aws_secret){"Green"}else{"Red"})
Write-Host "AWS_STORAGE_BUCKET_NAME: $(if($bucket){"✅ $bucket"}else{"❌ NOT SET"})" -ForegroundColor $(if($bucket){"Green"}else{"Red"})
Write-Host "AWS_REGION: $(if($region){"✅ $region"}else{"❌ NOT SET"})" -ForegroundColor $(if($region){"Green"}else{"Red"})
Write-Host "NEON_DATABASE_URL: $(if($database){"✅ SET"}else{"❌ NOT SET"})" -ForegroundColor $(if($database){"Green"}else{"Red"})

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Go to AWS Console: https://s3.console.aws.amazon.com/s3/" -ForegroundColor Cyan
Write-Host "2. Create bucket: codestorm2026-ppts" -ForegroundColor Cyan
Write-Host "3. Set bucket policy for public access" -ForegroundColor Cyan
Write-Host "4. Get AWS credentials from IAM" -ForegroundColor Cyan
Write-Host "5. Set environment variables in your deployment" -ForegroundColor Cyan

Write-Host "`n✨ Check MANUAL_S3_SETUP.md for detailed instructions!" -ForegroundColor Green