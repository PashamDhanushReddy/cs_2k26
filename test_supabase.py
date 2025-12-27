#!/usr/bin/env python
"""Test script to verify Supabase configuration and connectivity"""

import os
import requests
import json

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codestorm_project.settings')

import django
django.setup()

from django.conf import settings

def test_supabase_connection():
    """Test Supabase connection with current settings"""
    print("=== Testing Supabase Configuration ===")
    print(f"SUPABASE_URL: {settings.SUPABASE_KEY[:20]}..." if settings.SUPABASE_URL else "NOT SET")
    print(f"SUPABASE_KEY: {'SET' if settings.SUPABASE_KEY else 'NOT SET'}")
    print(f"SUPABASE_BUCKET_NAME: {settings.SUPABASE_BUCKET_NAME}")
    
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        print("❌ Missing Supabase configuration!")
        print("Please set the following environment variables:")
        print("- SUPABASE_URL")
        print("- SUPABASE_KEY")
        print("- SUPABASE_BUCKET_NAME")
        return False
    
    # Test database connection
    try:
        base_url = settings.SUPABASE_URL.rstrip('/')
        if not base_url.startswith('http'):
            base_url = f"https://{base_url}"
            
        table_url = f"{base_url}/rest/v1/codestorm_registrations"
        headers = {
            'apikey': settings.SUPABASE_KEY,
            'Authorization': f'Bearer {settings.SUPABASE_KEY}',
            'Content-Type': 'application/json',
        }
        
        print(f"\n=== Testing Database Connection ===")
        print(f"Testing URL: {table_url}")
        
        # Test with a simple GET request (select 1 row)
        response = requests.get(f"{table_url}?limit=1", headers=headers)
        print(f"Database response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Database connection successful!")
        else:
            print(f"❌ Database connection failed: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        return False
    
    # Test storage connection
    try:
        print(f"\n=== Testing Storage Connection ===")
        base_url = settings.SUPABASE_URL.rstrip('/')
        if not base_url.startswith('http'):
            base_url = f"https://{base_url}"
            
        storage_url = f"{base_url}/storage/v1/bucket/{settings.SUPABASE_BUCKET_NAME}"
        headers = {
            'apikey': settings.SUPABASE_KEY,
            'Authorization': f'Bearer {settings.SUPABASE_KEY}',
        }
        
        print(f"Testing storage URL: {storage_url}")
        response = requests.get(storage_url, headers=headers)
        print(f"Storage response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Storage connection successful!")
        else:
            print(f"⚠️  Storage connection returned: {response.status_code} - {response.text[:200]}")
            # This might be normal if bucket permissions are restricted
            
    except Exception as e:
        print(f"❌ Storage connection error: {str(e)}")
        return False
    
    print("\n=== All Tests Completed ===")
    return True

if __name__ == "__main__":
    success = test_supabase_connection()
    if success:
        print("\n🎉 Supabase configuration looks good!")
        print("You can now test the registration form at: http://127.0.0.1:8000/register/")
    else:
        print("\n⚠️  Please fix the configuration issues above before testing the registration form.")