# 🚀 Manual S3 PPT Upload Setup Guide (No Python Required)

Since Python isn't available in your current environment, here's how to manually set up and test your S3 PPT upload functionality:

## 📋 What You Need to Do

### 1️⃣ Set Up AWS S3 Bucket (Manual Steps)

**Go to AWS Console:**
1. Visit: https://s3.console.aws.amazon.com/s3/
2. Click "Create bucket"
3. **Bucket name:** `codestorm2026-ppts`
4. **Region:** Choose your preferred region (e.g., US East - N. Virginia)
5. Keep default settings for now
6. Click "Create bucket"

**Set Bucket Policy for Public Access:**
1. Click on your bucket name
2. Go to "Permissions" tab
3. Scroll down to "Bucket Policy"
4. Add this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::codestorm2026-ppts/*"
        }
    ]
}
```

**Set CORS Configuration:**
1. In "Permissions" tab, scroll to "Cross-origin resource sharing (CORS)"
2. Add this configuration:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

### 2️⃣ Get Your AWS Credentials

**Create IAM User (if you don't have one):**
1. Go to: https://console.aws.amazon.com/iam/
2. Click "Users" → "Add users"
3. **User name:** `codestorm-ppt-uploader`
4. **Access type:** Check "Programmatic access"
5. Click "Next"

**Attach Permissions:**
1. Click "Attach existing policies directly"
2. Search for and select: `AmazonS3FullAccess`
3. Click "Next" → "Create user"

**Save Your Credentials:**
- **Access Key ID:** Copy this (starts with AKIA...)
- **Secret Access Key:** Copy this (long random string)
- **Important:** Save these securely - you can't get the secret key again!

### 3️⃣ Set Environment Variables

**Option A: Using PowerShell Script**
```powershell
# Run the setup script I created
.\setup_s3_powershell.ps1
```

**Option B: Manual Setup**
```powershell
# Set these in your deployment environment
[Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", "your_access_key_here", "User")
[Environment]::SetEnvironmentVariable("AWS_SECRET_ACCESS_KEY", "your_secret_key_here", "User")
[Environment]::SetEnvironmentVariable("AWS_STORAGE_BUCKET_NAME", "codestorm2026-ppts", "User")
[Environment]::SetEnvironmentVariable("AWS_REGION", "us-east-1", "User")
```

### 4️⃣ Create Database Table (Manual SQL)

**Connect to your Neon database** and run this SQL:

```sql
-- Create PPT files metadata table
CREATE TABLE IF NOT EXISTS codestorm_ppt_files (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(255) NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    original_name VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    s3_url TEXT NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registration_id INTEGER REFERENCES codestorm_registrations(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add PPT file reference to registrations table
ALTER TABLE codestorm_registrations 
ADD COLUMN IF NOT EXISTS ppt_file_id INTEGER REFERENCES codestorm_ppt_files(id);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_team_name ON codestorm_ppt_files(team_name);
CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_s3_key ON codestorm_ppt_files(s3_key);
CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_registration_id ON codestorm_ppt_files(registration_id);
```

### 5️⃣ Test Your Setup

**Create a test file:**
```powershell
# Create a small test file
"Test content for CodeStorm 2026" | Out-File -FilePath "test_upload.txt" -Encoding UTF8
```

**Test with AWS CLI (if installed):**
```bash
# Install AWS CLI if needed: https://aws.amazon.com/cli/
aws configure
aws s3 cp test_upload.txt s3://codestorm2026-ppts/test/test_upload.txt --acl public-read
aws s3 ls s3://codestorm2026-ppts/test/
```

**Test the URL:**
Open in browser: `https://codestorm2026-ppts.s3.amazonaws.com/test/test_upload.txt`

### 6️⃣ Deploy Your Application

**Update your deployment with environment variables:**
```bash
# Add these to your deployment platform
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_STORAGE_BUCKET_NAME=codestorm2026-ppts
AWS_REGION=us-east-1
```

**Deploy and test:**
1. Upload a PPT through your registration form
2. Check your S3 bucket for the uploaded file
3. Check your database for metadata records

## 📊 Verify Everything Works

**Check your database:**
```sql
-- See all PPT uploads
SELECT 
    team_name,
    original_name,
    file_size,
    s3_url,
    uploaded_at
FROM codestorm_ppt_files 
ORDER BY uploaded_at DESC;
```

**Check S3 bucket:**
1. Go to your S3 console
2. Look for files in `codestorm_ppts/` folder
3. Click on a file and test the "Open" link

**Test public access:**
Copy the S3 URL from your database and paste it in a browser (incognito mode) to verify it's publicly accessible.

## 🎯 Expected Results

When someone uploads a PPT through your form:

1. **File gets uploaded to:** `s3://codestorm2026-ppts/codestorm_ppts/{uuid}.pptx`
2. **Public URL becomes:** `https://codestorm2026-ppts.s3.amazonaws.com/codestorm_ppts/{uuid}.pptx`
3. **Database stores:** Team name, file size, original name, S3 URL, etc.
4. **Registration links:** `ppt_file_id` connects the registration to the PPT file

## 🚨 Common Issues & Fixes

**"Access Denied" when testing URL:**
- Check bucket policy is set correctly
- Verify file was uploaded with `public-read` ACL
- Check CORS configuration

**"Bucket does not exist":**
- Verify bucket name matches exactly: `codestorm2026-ppts`
- Check you're in the correct AWS region

**"Invalid credentials":**
- Double-check your AWS Access Key ID and Secret
- Make sure the IAM user has S3 permissions

**Database errors:**
- Verify `NEON_DATABASE_URL` is correct
- Check table was created successfully
- Ensure foreign key constraints are satisfied

## ✅ Success Checklist

- [ ] S3 bucket created: `codestorm2026-ppts`
- [ ] Bucket policy set for public read access
- [ ] CORS configuration added
- [ ] AWS credentials obtained
- [ ] Environment variables set in deployment
- [ ] Database table created successfully
- [ ] Test file uploaded and accessible via URL
- [ ] Registration form successfully uploads PPTs
- [ ] Database contains metadata records
- [ ] S3 URLs are globally accessible

## 📞 Need Help?

If you run into issues:
1. Check AWS CloudTrail for detailed error logs
2. Verify all environment variables are set correctly
3. Test S3 access with AWS CLI or console
4. Check your application logs for specific errors

---

**🎉 Once you've completed these steps, your PPT uploads will work with AWS S3 and store all metadata in your Neon database!**