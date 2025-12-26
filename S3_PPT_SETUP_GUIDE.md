# 🚀 CodeStorm 2026 S3 PPT Upload Setup Guide

## Overview
Your CodeStorm 2026 registration system now supports AWS S3 file uploads with complete metadata storage in your Neon PostgreSQL database.

## 📋 What This Setup Does
1. **Uploads PPT files to AWS S3** with public access
2. **Stores file metadata** in `codestorm_ppt_files` table
3. **Links files to registrations** via foreign key relationship
4. **Generates accessible URLs** that work globally

## 🔧 Database Schema

### New Table: `codestorm_ppt_files`
```sql
CREATE TABLE codestorm_ppt_files (
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
```

### Updated Table: `codestorm_registrations`
```sql
ALTER TABLE codestorm_registrations 
ADD COLUMN ppt_file_id INTEGER REFERENCES codestorm_ppt_files(id);
```

## 🌍 Environment Variables Required

Add these to your deployment environment:

```bash
# Database (you should already have this)
NEON_DATABASE_URL=postgresql://username:password@host:port/database

# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_STORAGE_BUCKET_NAME=codestorm2026-ppts
AWS_REGION=us-east-1

# Optional: Custom domain (if using CloudFront)
AWS_S3_CUSTOM_DOMAIN=your-cloudfront-domain.com
```

## 📁 File Structure After Upload

When a PPT is uploaded, you'll get:

1. **S3 Storage**: `s3://codestorm2026-ppts/codestorm_ppts/{uuid}.pptx`
2. **Public URL**: `https://codestorm2026-ppts.s3.amazonaws.com/codestorm_ppts/{uuid}.pptx`
3. **Database Record**: Complete metadata in `codestorm_ppt_files` table
4. **Registration Link**: `ppt_file_id` connects to registration

## 🔍 Query Examples

### Get all PPT files with registration data
```sql
SELECT 
    p.team_name,
    p.original_name as ppt_filename,
    p.file_size,
    p.s3_url,
    p.uploaded_at,
    r.idea_title,
    r.idea_theme
FROM codestorm_ppt_files p
JOIN codestorm_registrations r ON p.registration_id = r.id
ORDER BY p.uploaded_at DESC;
```

### Get PPT files by team name
```sql
SELECT * FROM codestorm_ppt_files 
WHERE team_name = 'Your Team Name';
```

### Get total storage used
```sql
SELECT 
    COUNT(*) as total_files,
    SUM(file_size) as total_size_bytes,
    ROUND(SUM(file_size) / (1024.0 * 1024.0), 2) as total_size_mb
FROM codestorm_ppt_files;
```

## 🚀 Deployment Steps

1. **Set Environment Variables**
   ```bash
   export AWS_ACCESS_KEY_ID="your_key"
   export AWS_SECRET_ACCESS_KEY="your_secret"
   export AWS_STORAGE_BUCKET_NAME="codestorm2026-ppts"
   export AWS_REGION="us-east-1"
   ```

2. **Create S3 Bucket** (if not exists)
   - Go to AWS S3 Console
   - Create bucket: `codestorm2026-ppts`
   - Enable public read access
   - Set CORS policy if needed

3. **Run Database Setup**
   ```bash
   python setup_s3_ppt_uploads.py
   ```

4. **Deploy Your Application**
   ```bash
   git push heroku main  # or your deployment method
   ```

## 🧪 Testing

### Test File Upload
1. Go to your registration form
2. Fill out all required fields
3. Upload a PPT file
4. Submit the form
5. Check the database for metadata
6. Verify the S3 URL is accessible

### Test S3 Connectivity
Run the setup script to test S3:
```bash
python setup_s3_ppt_uploads.py
```

## 📊 Monitoring

### Check Upload Success
```sql
SELECT 
    DATE(uploaded_at) as upload_date,
    COUNT(*) as files_uploaded,
    ROUND(SUM(file_size) / (1024.0 * 1024.0), 2) as total_mb
FROM codestorm_ppt_files 
GROUP BY DATE(uploaded_at)
ORDER BY upload_date DESC;
```

### Find Large Files
```sql
SELECT 
    team_name,
    original_name,
    ROUND(file_size / (1024.0 * 1024.0), 2) as size_mb,
    s3_url
FROM codestorm_ppt_files 
WHERE file_size > 5 * 1024 * 1024  -- Files larger than 5MB
ORDER BY file_size DESC;
```

## 🔒 Security Notes

1. **S3 Bucket**: Files are uploaded with `public-read` ACL for global access
2. **File Names**: UUID-based names prevent guessing
3. **Size Limits**: 10MB maximum file size enforced
4. **Database**: Foreign key constraints ensure data integrity

## 🛠️ Troubleshooting

### Common Issues

1. **"AWS S3 credentials not configured"**
   - Check environment variables are set
   - Verify AWS credentials are correct

2. **"Database error storing PPT metadata"**
   - Check NEON_DATABASE_URL is correct
   - Verify table was created successfully

3. **"Error uploading to S3"**
   - Check bucket exists and is accessible
   - Verify AWS credentials have S3 permissions
   - Check bucket CORS policy if needed

### Debug Mode
The application logs detailed information:
- S3 upload status
- Database operations
- File metadata

Check your application logs for detailed error messages.

## 📞 Support

If you encounter issues:
1. Check application logs
2. Verify environment variables
3. Test S3 connectivity with setup script
4. Check database table structure

---

**✅ Your PPT uploads are now ready! Files will be stored in S3 with complete metadata tracking in your Neon database.**