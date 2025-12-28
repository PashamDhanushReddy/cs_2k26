#!/usr/bin/env python3
"""
Test script to verify Cloudinary upload
"""

import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', '')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '')

def test_cloudinary_upload():
    """Test uploading a file to Cloudinary"""
    print("=== Testing Cloudinary Upload ===")
    print(f"Cloud Name: {CLOUDINARY_CLOUD_NAME}")
    
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
        print("❌ Missing Cloudinary environment variables. Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET.")
        return False

    # Initialize Cloudinary
    cloudinary.config( 
        cloud_name = CLOUDINARY_CLOUD_NAME, 
        api_key = CLOUDINARY_API_KEY, 
        api_secret = CLOUDINARY_API_SECRET,
        secure = True
    )
    
    # Create a simple test file
    test_filename = "test_upload_cloudinary.txt"
    with open(test_filename, "w") as f:
        f.write("This is a test file for Cloudinary upload functionality.")
    
    try:
        print(f"Uploading {test_filename} to Cloudinary...")
        
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            test_filename, 
            public_id="test_upload_cloudinary_123",
            folder="ppt_submissions_test",
            resource_type="auto"
        )
        
        print(f"Upload response: {response}")
        print(f"✅ Upload successful! URL: {response.get('secure_url')}")
        
        # Cleanup local file
        os.remove(test_filename)
        return True
            
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        # Cleanup local file
        if os.path.exists(test_filename):
            os.remove(test_filename)
        return False

if __name__ == "__main__":
    test_cloudinary_upload()
