import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET_NAME = os.getenv('SUPABASE_BUCKET_NAME')

def create_supabase_headers():
    """Create headers for Supabase API requests"""
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

def test_storage_connection():
    """Test different storage bucket name formats"""
    headers = create_supabase_headers()
    
    # Test different bucket name formats
    bucket_names = [
        'codestorm-ppt',
        'codestorm-ppt/',
        'codestorm-ppt/',
        'codestorm_ppt',
        'codestorm.ppt'
    ]
    
    print("=== Testing Storage Bucket Names ===")
    for bucket_name in bucket_names:
        storage_url = f"{SUPABASE_URL}/storage/v1/bucket/{bucket_name}"
        try:
            response = requests.get(storage_url, headers=headers)
            print(f"Bucket '{bucket_name}': Status {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ Found bucket: {response.json()}")
                return bucket_name
            elif response.status_code == 404:
                print(f"  ❌ Bucket not found")
            else:
                print(f"  ⚠️  Response: {response.text}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    return None

# Run the test
test_storage_connection()