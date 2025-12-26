# 🚀 CodeStorm 2026 S3 PPT Upload - Final Setup Summary

## ✅ **What's Already Done**

Your Django application is **fully configured** for AWS S3 PPT uploads with metadata storage:

- ✅ **views.py** - S3 upload logic implemented with metadata storage
- ✅ **settings.py** - AWS S3 configuration added
- ✅ **requirements.txt** - boto3 dependencies included
- ✅ **SQL script** - Database table for metadata storage created
- ✅ **Test scripts** - Setup and testing tools provided

## 🎯 **What You Need To Do Now**

### **Step 1: Set Up AWS S3 (5 minutes)**

1. **Create S3 Bucket:**
   - Go to: https://s3.console.aws.amazon.com/s3/
   - Click "Create bucket"
   - **Bucket name:** `codestorm2026-ppts`
   - **Region:** Choose your preferred region
   - Keep defaults and create

2. **Set Bucket Policy:**
   - Click your bucket → "Permissions" → "Bucket Policy"
   - Add this policy:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": "*",
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::codestorm2026-ppts/*"
           }
       ]
   }
   ```

3. **Set CORS Configuration:**
   - Go to "Permissions" → "Cross-origin resource sharing (CORS)"
   - Add:
   ```json
   [
       {
           "AllowedHeaders": ["*"],
           "AllowedMethods": ["GET", "PUT", "POST"],
           "AllowedOrigins": ["*"]
       }
   ]
   ```

### **Step 2: Get AWS Credentials (3 minutes)**

1. **Create IAM User:**
   - Go to: https://console.aws.amazon.com/iam/
   - "Users" → "Add users"
   - **Username:** `codestorm-ppt-uploader`
   - **Access type:** ✓ Programmatic access

2. **Attach Permissions:**
   - "Attach existing policies directly"
   - Search and select: `AmazonS3FullAccess`
   - Create user

3. **Save Credentials:**
   - **Access Key ID:** Copy this (starts with AKIA...)
   - **Secret Access Key:** Copy this (shown only once!)

### **Step 3: Set Environment Variables (2 minutes)**

**Option A: Use the batch file I created:**
1. Edit `setup_env.bat` with your actual credentials
2. Run: `setup_env.bat`

**Option B: Manual setup:**
```batch
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_STORAGE_BUCKET_NAME=codestorm2026-ppts
set AWS_REGION=us-east-1
set NEON_DATABASE_URL=your_neon_database_url
```

**Option C: Set in your deployment platform:**
Add these to your deployment environment variables (Render, Heroku, etc.)

### **Step 4: Create Database Table (2 minutes)**

**Connect to your Neon database and run:**
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

-- Add PPT file reference to registrations
ALTER TABLE codestorm_registrations 
ADD COLUMN IF NOT EXISTS ppt_file_id INTEGER REFERENCES codestorm_ppt_files(id);
```

### **Step 5: Deploy and Test (1 minute)**

1. **Deploy your application** with the new environment variables
2. **Test the registration form** with a PPT upload
3. **Verify uploads:**
   - Check S3 bucket for uploaded files
   - Check database for metadata records
   - Test public URLs are accessible

## 🔍 **How to Verify It Works**

**Check your database:**
```sql
SELECT team_name, original_name, file_size, s3_url, uploaded_at 
FROM codestorm_ppt_files 
ORDER BY uploaded_at DESC;
```

**Check S3 bucket:**
- Go to your S3 console
- Look for files in `codestorm_ppts/` folder
- Test the "Open" link on a file

**Test public access:**
Copy an S3 URL from your database and paste in browser (incognito mode).

## 📁 **Files You Have**

- `setup_env.bat` - Set environment variables
- `quick_setup.ps1` - Check current setup
- `MANUAL_S3_SETUP.md` - Detailed manual instructions
- `test_s3_setup.py` - Python test script (when available)
- `create_ppt_metadata_table.sql` - Database table creation

## ⚡ **Quick Commands**

**Check current setup:**
```powershell
.\quick_setup.ps1
```

**Set environment variables:**
```batch
setup_env.bat
```

**Test S3 (when Python available):**
```bash
python test_s3_setup.py
```

## 🎯 **Expected Results**

When someone uploads a PPT:

1. **File uploads to:** `s3://codestorm2026-ppts/codestorm_ppts/{uuid}.pptx`
2. **Public URL:** `https://codestorm2026-ppts.s3.amazonaws.com/codestorm_ppts/{uuid}.pptx`
3. **Database stores:** Team name, file info, S3 URL, metadata
4. **Registration links:** PPT file linked to registration record

## 🚨 **Common Issues & Fixes**

**"Access Denied" on S3 URL:**
- Check bucket policy is set correctly
- Verify file was uploaded with public-read ACL

**"Bucket not found":**
- Verify bucket name: `codestorm2026-ppts`
- Check you're in correct AWS region

**Database errors:**
- Verify `NEON_DATABASE_URL` is correct
- Ensure table was created successfully

**Upload fails:**
- Check AWS credentials are correct
- Verify IAM user has S3 permissions
- Ensure bucket exists and is accessible

---

## 🎉 **You're Ready!**

Your CodeStorm 2026 registration form now supports:
- ✅ PPT uploads to AWS S3
- ✅ Public URLs accessible globally
- ✅ Complete metadata storage in Neon DB
- ✅ Files linked to registrations

**Total setup time: ~13 minutes**

Follow the steps above and your PPT upload system will be **production-ready**! 🚀