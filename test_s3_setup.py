# Test script to verify your S3 PPT upload setup
# This script will help you test the AWS S3 configuration

import os
import sys

def test_environment():
    """Test if all required environment variables are set"""
    print("🔍 Testing Environment Variables:")
    print("-" * 40)
    
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_REGION',
        'NEON_DATABASE_URL'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive data
            if 'SECRET' in var or 'PASSWORD' in var:
                display_value = value[:4] + "****" + value[-4:] if len(value) > 8 else "****"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    return all_set

def test_s3_upload():
    """Test S3 upload functionality"""
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        print("\n🚀 Testing S3 Upload:")
        print("-" * 40)
        
        # Get configuration
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'codestorm2026-ppts')
        region = os.environ.get('AWS_REGION', 'us-east-1')
        
        if not all([aws_access_key, aws_secret_key]):
            print("❌ AWS credentials not found")
            return False
        
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        # Test bucket access
        print(f"Testing bucket: {bucket_name}")
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' is accessible")
        
        # Test file upload
        test_content = b"CodeStorm 2026 Test File - This can be deleted"
        test_key = "test/codestorm_test_upload.txt"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content,
            ACL='public-read',
            ContentType='text/plain'
        )
        
        # Generate URL
        s3_domain = os.environ.get('AWS_S3_CUSTOM_DOMAIN', f"{bucket_name}.s3.amazonaws.com")
        file_url = f"https://{s3_domain}/{test_key}"
        
        print(f"✅ Test upload successful!")
        print(f"📁 File URL: {file_url}")
        
        # Test public access
        import urllib.request
        try:
            with urllib.request.urlopen(file_url) as response:
                content = response.read()
                if content == test_content:
                    print("✅ Public access verified!")
                else:
                    print("⚠️  Content mismatch")
        except Exception as e:
            print(f"⚠️  Public access test failed: {e}")
        
        # Clean up
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        print("✅ Test file cleaned up")
        
        return True
        
    except ImportError:
        print("❌ boto3 not installed. Install with: pip install boto3")
        return False
    except ClientError as e:
        print(f"❌ S3 error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        import psycopg2
        
        print("\n🗄️ Testing Database Connection:")
        print("-" * 40)
        
        conn_str = os.environ.get('NEON_DATABASE_URL')
        if not conn_str:
            print("❌ NEON_DATABASE_URL not set")
            return False
        
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Test table existence
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'codestorm_ppt_files'
        """)
        
        if cur.fetchone():
            print("✅ codestorm_ppt_files table exists")
            
            # Show sample data
            cur.execute("SELECT COUNT(*) FROM codestorm_ppt_files")
            count = cur.fetchone()[0]
            print(f"📊 Current PPT files: {count}")
            
        else:
            print("⚠️ codestorm_ppt_files table not found")
            print("   Run: python setup_s3_ppt_uploads.py")
        
        cur.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 CodeStorm 2026 S3 PPT Upload Test")
    print("=" * 50)
    
    # Test environment
    env_ok = test_environment()
    
    if not env_ok:
        print("\n❌ Environment setup incomplete!")
        print("Please set all required environment variables.")
        return False
    
    # Test S3
    s3_ok = test_s3_upload()
    
    # Test database
    db_ok = test_database()
    
    print("\n📋 Test Summary:")
    print("-" * 50)
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"S3 Upload: {'✅' if s3_ok else '❌'}")
    print(f"Database: {'✅' if db_ok else '❌'}")
    
    if all([env_ok, s3_ok, db_ok]):
        print("\n🎉 All tests passed! Your S3 PPT upload is ready!")
        print("\nNext steps:")
        print("1. Deploy your application")
        print("2. Test with actual PPT file upload")
        print("3. Verify URL accessibility")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
    
    return all([env_ok, s3_ok, db_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)