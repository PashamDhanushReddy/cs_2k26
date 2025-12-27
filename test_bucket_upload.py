#!/usr/bin/env python3
"""
Test script to verify Supabase storage bucket upload
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://divhwqupyptmuotlzqpn.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpdmh3cXVweXB0bXVvdGx6cXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY3NjMxNDIsImV4cCI6MjA4MjMzOTE0Mn0.byZcoPz1SG6olNX_x17jKoqyVwuUKhPeO_JnDauR4A4')
SUPABASE_BUCKET_NAME = os.getenv('SUPABASE_BUCKET_NAME', 'codestorm-ppt')

def test_bucket_upload():
    """Test uploading a file to Supabase storage bucket"""
    print("=== Testing Supabase Storage Upload ===")
    print(f"URL: {SUPABASE_URL}")
    print(f"Bucket: {SUPABASE_BUCKET_NAME}")
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/octet-stream'
    }
    
    # Create a simple test file content
    test_content = b"This is a test PPT file content for testing upload functionality."
    file_path = "test_ppt_upload_123.pptx"
    
    # Upload to Supabase storage
    storage_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET_NAME}/ppt_submissions/{file_path}"
    
    try:
        print(f"Uploading to: {storage_url}")
        response = requests.post(storage_url, data=test_content, headers=headers)
        
        print(f"Upload response status: {response.status_code}")
        print(f"Upload response: {response.text[:300]}")
        
        if response.status_code == 201:
            print("✅ Upload successful!")
            return True
        elif response.status_code == 400 and "Bucket not found" in response.text:
            print("❌ Bucket not found")
            return False
        elif response.status_code == 401:
            print("❌ 401 Unauthorized - Check bucket policies")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

if __name__ == "__main__":
    test_bucket_upload()