# 🚀 CodeStorm 2026 S3 PPT Upload - Quick Setup for Your Table

## ✅ **Your Table is Perfect!**

Your `codestorm_registrations` table already has the `ppt_upload_url` field - exactly what we need! The S3 integration is already configured to store URLs there.

## 🎯 **What You Need To Do (10 minutes)**

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

**Option A: Use the batch file:**
1. Edit `setup_env.bat` with your credentials
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
Add these to your deployment environment variables

### **Step 4: Deploy and Test (1 minute)**

1. **Deploy your application** with the new environment variables
2. **Test the registration form** with a PPT upload
3. **Verify uploads:**
   - Check S3 bucket for uploaded files
   - Check database - `ppt_upload_url` should contain S3 URLs
   - Test public URLs are accessible

## 🔍 **How to Verify It Works**

**Check your database:**
```sql
SELECT team_name, ppt_upload_url, uploaded_at 
FROM codestorm_registrations 
WHERE ppt_upload_url IS NOT NULL
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
- `FINAL_SETUP_SUMMARY.md` - Complete documentation

## ⚡ **Quick Commands**

**Check current setup:**
```powershell
.\quick_setup.ps1
```

**Set environment variables:**
```batch
setup_env.bat
```

## 🎯 **Expected Results**

When someone uploads a PPT:

1. **File uploads to:** `s3://codestorm2026-ppts/codestorm_ppts/{uuid}.pptx`
2. **Public URL:** `https://codestorm2026-ppts.s3.amazonaws.com/codestorm_ppts/{uuid}.pptx`
3. **Database stores:** S3 URL in `ppt_upload_url` field
4. **URL format:** Globally accessible from anywhere

## 🚨 **Common Issues & Fixes**

**"Access Denied" on S3 URL:**
- Check bucket policy is set correctly
- Verify file was uploaded with public-read ACL

**"Bucket not found":**
- Verify bucket name: `codestorm2026-ppts`
- Check you're in correct AWS region

**Upload fails:**
- Check AWS credentials are correct
- Verify IAM user has S3 permissions
- Ensure bucket exists and is accessible

---

## 🎉 **You're Ready!**

Your CodeStorm 2026 registration form now supports:
- ✅ PPT uploads to AWS S3
- ✅ Public URLs stored in `ppt_upload_url` field
- ✅ URLs accessible globally from anywhere
- ✅ All existing registration functionality preserved

**Total setup time: ~10 minutes**

Follow the steps above and your PPT upload system will be **production-ready**! 🚀