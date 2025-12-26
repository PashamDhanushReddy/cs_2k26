# CodeStorm 2026 S3 PPT Upload Setup Script
# This PowerShell script helps you set up and test your S3 configuration

Write-Host "🚀 CodeStorm 2026 S3 PPT Upload Setup" -ForegroundColor Green
Write-Host "=" * 50

# Function to test if Python is available
function Test-Python {
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Python not found in PATH" -ForegroundColor Red
        return $false
    }
}

# Function to check environment variables
function Test-Environment {
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
            # Mask sensitive data
            if ($var -like "*SECRET*" -or $var -like "*PASSWORD*") {
                $displayValue = $value.Substring(0, [Math]::Min(4, $value.Length)) + "****" + $value.Substring([Math]::Max($value.Length - 4, 4))
            } else {
                $displayValue = $value
            }
            Write-Host "✅ $var : $displayValue" -ForegroundColor Green
        } else {
            Write-Host "❌ $var : NOT SET" -ForegroundColor Red
            $allSet = $false
        }
    }
    
    return $allSet
}

# Function to set environment variables
function Set-EnvironmentVariable {
    param(
        [string]$Name,
        [string]$Value,
        [string]$Description
    )
    
    if (-not $Value) {
        Write-Host "Enter $Description :" -ForegroundColor Cyan -NoNewline
        $Value = Read-Host
    }
    
    [Environment]::SetEnvironmentVariable($Name, $Value, "User")
    Write-Host "✅ Set $Name" -ForegroundColor Green
}

# Function to create AWS credentials file
function Create-AWSCredentials {
    Write-Host "`n📁 Creating AWS Credentials File..." -ForegroundColor Yellow
    
    $awsDir = "$HOME\.aws"
    if (-not (Test-Path $awsDir)) {
        New-Item -ItemType Directory -Path $awsDir -Force | Out-Null
    }
    
    $credentialsFile = "$awsDir\credentials"
    $configFile = "$awsDir\config"
    
    # Get credentials from environment or user input
    $accessKey = [Environment]::GetEnvironmentVariable("AWS_ACCESS_KEY_ID")
    $secretKey = [Environment]::GetEnvironmentVariable("AWS_SECRET_ACCESS_KEY")
    $region = [Environment]::GetEnvironmentVariable("AWS_REGION") -or "us-east-1"
    
    if (-not $accessKey) {
        Write-Host "Enter AWS Access Key ID:" -ForegroundColor Cyan -NoNewline
        $accessKey = Read-Host
    }
    
    if (-not $secretKey) {
        Write-Host "Enter AWS Secret Access Key:" -ForegroundColor Cyan -NoNewline
        $secretKey = Read-Host
    }
    
    # Create credentials file
    @"
[default]
aws_access_key_id = $accessKey
aws_secret_access_key = $secretKey
"@ | Out-File -FilePath $credentialsFile -Encoding ASCII

    # Create config file
    @"
[default]
region = $region
"@ | Out-File -FilePath $configFile -Encoding ASCII

    Write-Host "✅ AWS credentials files created" -ForegroundColor Green
}

# Function to test S3 bucket access
function Test-S3Bucket {
    Write-Host "`n🪣 Testing S3 Bucket Access:" -ForegroundColor Yellow
    Write-Host "-" * 40
    
    $bucketName = [Environment]::GetEnvironmentVariable("AWS_STORAGE_BUCKET_NAME") -or "codestorm2026-ppts"
    $region = [Environment]::GetEnvironmentVariable("AWS_REGION") -or "us-east-1"
    
    Write-Host "Bucket: $bucketName" -ForegroundColor Cyan
    Write-Host "Region: $region" -ForegroundColor Cyan
    
    # Test using AWS CLI if available
    try {
        $awsVersion = aws --version 2>$null
        if ($awsVersion) {
            Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
            
            # Test bucket access
            $bucketTest = aws s3 ls s3://$bucketName 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Bucket '$bucketName' is accessible" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Bucket '$bucketName' may not exist or be accessible" -ForegroundColor Yellow
                Write-Host "   Create it at: https://s3.console.aws.amazon.com/s3/" -ForegroundColor Cyan
            }
        } else {
            Write-Host "⚠️  AWS CLI not found. Install from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  AWS CLI not available" -ForegroundColor Yellow
    }
}

# Function to create test file
function Create-TestFile {
    Write-Host "`n📄 Creating Test PPT File..." -ForegroundColor Yellow
    
    $testContent = @"
This is a test file for CodeStorm 2026 S3 PPT upload testing.
You can delete this file after testing.
Created: $(Get-Date)
"@
    
    $testFile = "$PWD\test_ppt_upload.txt"
    $testContent | Out-File -FilePath $testFile -Encoding UTF8
    
    Write-Host "✅ Test file created: $testFile" -ForegroundColor Green
    Write-Host "   (You can rename this to .pptx for testing)" -ForegroundColor Cyan
}

# Function to show next steps
function Show-NextSteps {
    Write-Host "`n🎯 Next Steps:" -ForegroundColor Green
    Write-Host "-" * 50
    Write-Host "1. Set up your AWS S3 bucket:" -ForegroundColor Yellow
    Write-Host "   - Go to https://s3.console.aws.amazon.com/s3/" -ForegroundColor Cyan
    Write-Host "   - Create bucket: codestorm2026-ppts" -ForegroundColor Cyan
    Write-Host "   - Set bucket policy for public read access" -ForegroundColor Cyan
    
    Write-Host "`n2. Configure your environment variables:" -ForegroundColor Yellow
    Write-Host "   - AWS_ACCESS_KEY_ID" -ForegroundColor Cyan
    Write-Host "   - AWS_SECRET_ACCESS_KEY" -ForegroundColor Cyan
    Write-Host "   - AWS_STORAGE_BUCKET_NAME=codestorm2026-ppts" -ForegroundColor Cyan
    Write-Host "   - AWS_REGION=us-east-1" -ForegroundColor Cyan
    Write-Host "   - NEON_DATABASE_URL" -ForegroundColor Cyan
    
    Write-Host "`n3. Test the setup:" -ForegroundColor Yellow
    Write-Host "   - Run: python test_s3_setup.py" -ForegroundColor Cyan
    Write-Host "   - Or upload a PPT through your registration form" -ForegroundColor Cyan
    
    Write-Host "`n4. Verify uploads:" -ForegroundColor Yellow
    Write-Host "   - Check your S3 bucket for uploaded files" -ForegroundColor Cyan
    Write-Host "   - Check your database for metadata records" -ForegroundColor Cyan
}

# Main menu
function Show-Menu {
    Write-Host "`n📋 Setup Menu:" -ForegroundColor Yellow
    Write-Host "1. Check environment variables" -ForegroundColor Cyan
    Write-Host "2. Set AWS credentials" -ForegroundColor Cyan
    Write-Host "3. Create AWS credentials files" -ForegroundColor Cyan
    Write-Host "4. Test S3 bucket access" -ForegroundColor Cyan
    Write-Host "5. Create test file" -ForegroundColor Cyan
    Write-Host "6. Run full setup check" -ForegroundColor Cyan
    Write-Host "7. Show next steps" -ForegroundColor Cyan
    Write-Host "Q. Quit" -ForegroundColor Cyan
    
    Write-Host "`nSelect option:" -ForegroundColor Green -NoNewline
    return Read-Host
}

# Main function
function Main {
    Write-Host "🚀 CodeStorm 2026 S3 PPT Upload Setup" -ForegroundColor Green
    Write-Host "=" * 50
    
    # Check Python availability
    $pythonAvailable = Test-Python
    
    while ($true) {
        $choice = Show-Menu
        
        switch ($choice.ToUpper()) {
            "1" {
                Test-Environment
            }
            "2" {
                Set-EnvironmentVariable -Name "AWS_ACCESS_KEY_ID" -Description "AWS Access Key ID"
                Set-EnvironmentVariable -Name "AWS_SECRET_ACCESS_KEY" -Description "AWS Secret Access Key"
                Set-EnvironmentVariable -Name "AWS_STORAGE_BUCKET_NAME" -Value "codestorm2026-ppts" -Description "S3 Bucket Name"
                Set-EnvironmentVariable -Name "AWS_REGION" -Value "us-east-1" -Description "AWS Region"
            }
            "3" {
                Create-AWSCredentials
            }
            "4" {
                Test-S3Bucket
            }
            "5" {
                Create-TestFile
            }
            "6" {
                Write-Host "`n🔧 Running Full Setup Check..." -ForegroundColor Yellow
                $envOk = Test-Environment
                if ($envOk -and $pythonAvailable) {
                    Write-Host "`n🧪 Running Python tests..." -ForegroundColor Yellow
                    python test_s3_setup.py
                } elseif (-not $pythonAvailable) {
                    Write-Host "⚠️  Python not available - skipping Python tests" -ForegroundColor Yellow
                }
            }
            "7" {
                Show-NextSteps
            }
            "Q" {
                Write-Host "👋 Goodbye!" -ForegroundColor Green
                return
            }
            default {
                Write-Host "❌ Invalid option" -ForegroundColor Red
            }
        }
    }
}

# Run the script
Main