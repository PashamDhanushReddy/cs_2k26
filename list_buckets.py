import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def create_supabase_headers():
    """Create headers for Supabase API requests"""
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

def list_all_buckets():
    """List all storage buckets in the Supabase project"""
    headers = create_supabase_headers()
    
    # Get list of all buckets
    buckets_url = f"{SUPABASE_URL}/storage/v1/bucket"
    
    try:
        response = requests.get(buckets_url, headers=headers)
        print(f"=== All Storage Buckets ===")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            buckets = response.json()
            if buckets:
                print("Available buckets:")
                for bucket in buckets:
                    print(f"  📁 {bucket.get('name', 'Unknown')} (ID: {bucket.get('id', 'N/A')})")
                    print(f"     Public: {bucket.get('public', 'N/A')}")
                    print(f"     File size limit: {bucket.get('file_size_limit', 'N/A')}")
                    print()
                return buckets
            else:
                print("No buckets found in this project.")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error listing buckets: {str(e)}")
    
    return None

# List all buckets
list_all_buckets()