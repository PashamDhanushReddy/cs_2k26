# 🚀 CodeStorm 2026 S3 PPT Upload Setup Script
# Simplified PowerShell script for manual setup

Write-Host "🚀 CodeStorm 2026 S3 PPT Upload Setup" -ForegroundColor Green
Write-Host "=" * 50

# Check Python availability
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Python not found - manual setup required" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Python not found - manual setup required" -ForegroundColor Yellow
}

# Check environment variables
Write-Host "`n🔍 Checking Environment Variables:" -ForegroundColor Yellow
Write-Host "-" * 40

$requiredVars = @(
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY", 
    "AWS_STORAGE_BUCKET_NAME",
    "AWS_REGION",
    "NEON_DATABASE_URL"
)

$allSet = $true
foreach ($var in $requiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        if ($var -like "*SECRET*" -or $var -like "*PASSWORD*") {
            $displayValue = $value.Substring(0, [Math]::Min(4, $value.Length)) + "****"
        } else {
            $displayValue = $value
        }
        Write-Host "✅ $var : $displayValue" -ForegroundColor Green
    } else {
        Write-Host "❌ $var : NOT SET" -ForegroundColor Red
        $allSet = $false
    }
}

# Create test file function
function Create-TestFile {
    Write-Host "`n📄 Creating Test File..." -ForegroundColor Yellow
    $testContent = @"
This is a test file for CodeStorm 2026 S3 PPT upload testing.
Created: $(Get-Date)
"@
    $testFile = "$PWD\test_ppt_upload.txt"
    $testContent | Out-File -FilePath $testFile -Encoding UTF8
    Write-Host "✅ Test file created: $testFile" -ForegroundColor Green
}

# Set environment variables function
function Set-EnvironmentVars {
    Write-Host "`n🔧 Setting Environment Variables..." -ForegroundColor Yellow
    
    Write-Host "Enter AWS Access Key ID:" -ForegroundColor Cyan -NoNewline
    $accessKey = Read-Host
    [Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", $accessKey, "User")
    
    Write-Host "Enter AWS Secret Access Key:" -ForegroundColor Cyan -NoNewline
    $secretKey = Read-Host
    [Environment]::SetEnvironmentVariable("AWS_SECRET_ACCESS_KEY", $secretKey, "User")
    
    [Environment]::SetEnvironmentVariable("AWS_STORAGE_BUCKET_NAME", "codestorm2026-ppts", "User")
    [Environment]::SetEnvironmentVariable("AWS_REGION", "us-east-1", "User")
    
    Write-Host "✅ Environment variables set!" -ForegroundColor Green
}

# Show setup instructions
function Show-Instructions {
    Write-Host "`n📋 AWS S3 Setup Instructions:" -ForegroundColor Yellow
    Write-Host "-" * 50
    Write-Host "1. Go to: https://s3.console.aws.amazon.com/s3/" -ForegroundColor Cyan
    Write-Host "2. Create bucket: codestorm2026-ppts" -ForegroundColor Cyan
    Write-Host "3. Set bucket policy for public read access" -ForegroundColor Cyan
    Write-Host "4. Get AWS credentials from IAM console" -ForegroundColor Cyan
    Write-Host "5. Set environment variables in your deployment" -ForegroundColor Cyan
    Write-Host "6. Test with a file upload" -ForegroundColor Cyan
}

# Main menu
Write-Host "`n📋 Setup Options:" -ForegroundColor Yellow
Write-Host "1. Check environment variables (current)" -ForegroundColor Cyan
Write-Host "2. Set AWS environment variables" -ForegroundColor Cyan
Write-Host "3. Create test file" -ForegroundColor Cyan
Write-Host "4. Show setup instructions" -ForegroundColor Cyan
Write-Host "Q. Quit" -ForegroundColor Cyan

Write-Host "`nSelect option:" -ForegroundColor Green -NoNewline
$choice = Read-Host

switch ($choice.ToUpper()) {
    "1" {
        # Already checked above
    }
    "2" {
        Set-EnvironmentVars
    }
    "3" {
        Create-TestFile
    }
    "4" {
        Show-Instructions
    }
    "Q" {
        Write-Host "👋 Goodbye!" -ForegroundColor Green
        exit
    }
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
    }
}

Write-Host "`n✨ Setup complete! Check the MANUAL_S3_SETUP.md file for detailed instructions." -ForegroundColor Green