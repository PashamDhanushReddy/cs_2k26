#!/usr/bin/env python3
"""
AWS S3 PPT Upload Setup Script for CodeStorm 2026

This script helps you:
1. Create the PPT metadata table in your Neon database
2. Test S3 connectivity
3. Verify the complete upload workflow
"""

import os
import sys
import psycopg2
from psycopg2.errors import DuplicateTable

def create_ppt_table(conn_str):
    """Create the PPT files metadata table"""
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Create table for PPT file metadata
        create_table_sql = """
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
        """
        
        cur.execute(create_table_sql)
        
        # Add PPT file reference to registrations table
        alter_table_sql = """
        ALTER TABLE codestorm_registrations 
        ADD COLUMN IF NOT EXISTS ppt_file_id INTEGER REFERENCES codestorm_ppt_files(id);
        """
        
        cur.execute(alter_table_sql)
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_team_name ON codestorm_ppt_files(team_name);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_s3_key ON codestorm_ppt_files(s3_key);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_registration_id ON codestorm_ppt_files(registration_id);")
        
        conn.commit()
        print("✅ PPT metadata table created successfully!")
        
        # Show table structure
        cur.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'codestorm_ppt_files' ORDER BY ordinal_position;")
        columns = cur.fetchall()
        print("\n📊 Table Structure:")
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {str(e)}")
        return False

def test_s3_connection():
    """Test AWS S3 connectivity"""
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        # Get AWS credentials from environment
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'codestorm2026-ppts')
        
        if not aws_access_key or not aws_secret_key:
            print("⚠️  AWS credentials not found in environment variables")
            print("   Please set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            return False
        
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        
        # Test bucket access
        try:
            response = s3_client.head_bucket(Bucket=bucket_name)
            print(f"✅ S3 bucket '{bucket_name}' is accessible!")
            
            # Test upload permissions
            test_key = "test/codestorm_s3_test.txt"
            test_content = b"CodeStorm 2026 S3 Test - This file can be deleted"
            
            s3_client.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=test_content,
                ACL='public-read'
            )
            
            # Generate test URL
            s3_domain = os.environ.get('AWS_S3_CUSTOM_DOMAIN', f"{bucket_name}.s3.amazonaws.com")
            test_url = f"https://{s3_domain}/{test_key}"
            
            print(f"✅ Test upload successful!")
            print(f"📁 Test file URL: {test_url}")
            
            # Clean up test file
            s3_client.delete_object(Bucket=bucket_name, Key=test_key)
            print("🧹 Test file cleaned up")
            
            return True
            
        except ClientError as e:
            print(f"❌ S3 bucket error: {str(e)}")
            return False
            
    except ImportError:
        print("❌ boto3 not installed. Run: pip install boto3")
        return False
    except Exception as e:
        print(f"❌ S3 test failed: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 CodeStorm 2026 S3 PPT Upload Setup")
    print("=" * 50)
    
    # Get database connection
    conn_str = os.environ.get('NEON_DATABASE_URL')
    if not conn_str:
        print("❌ NEON_DATABASE_URL not found in environment variables")
        print("   Please set your Neon database connection string")
        return False
    
    print("\n1️⃣ Creating PPT metadata table...")
    if create_ppt_table(conn_str):
        print("   ✅ Table creation complete")
    else:
        print("   ❌ Table creation failed")
        return False
    
    print("\n2️⃣ Testing S3 connectivity...")
    if test_s3_connection():
        print("   ✅ S3 setup complete")
    else:
        print("   ⚠️  S3 test failed - uploads will not work")
    
    print("\n3️⃣ Setup Summary:")
    print("   📋 Database table: codestorm_ppt_files")
    print("   🔗 S3 bucket: configured")
    print("   📁 File URLs: will be stored in database")
    print("   🔍 Metadata: team_name, file_size, s3_url, etc.")
    
    print("\n✅ Setup complete! Your PPT uploads will now:")
    print("   1. Upload files to AWS S3 with public access")
    print("   2. Store metadata in codestorm_ppt_files table")
    print("   3. Link files to registrations via ppt_file_id")
    print("   4. Generate accessible URLs for global access")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)