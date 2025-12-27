#!/usr/bin/env python3
"""
Test script to verify Supabase connection and check RLS policies
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://divhwqupyptmuotlzqpn.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpdmh3cXVweXB0bXVvdGx6cXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY3NjMxNDIsImV4cCI6MjA4MjMzOTE0Mn0.byZcoPz1SG6olNX_x17jKoqyVwuUKhPeO_JnDauR4A4')

def test_supabase_connection():
    """Test basic Supabase connection"""
    print("=== Testing Supabase Connection ===")
    print(f"URL: {SUPABASE_URL}")
    print(f"Key: {SUPABASE_KEY[:20]}...")
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Check if we can query the table
    print("\n1. Testing table query...")
    query_url = f"{SUPABASE_URL}/rest/v1/codestorm_registrations?select=*&limit=1"
    
    try:
        response = requests.get(query_url, headers=headers)
        print(f"Query response status: {response.status_code}")
        print(f"Query response: {response.text[:200]}")
        
        if response.status_code == 401:
            print("❌ 401 Unauthorized - RLS policies are likely blocking access")
            return False
        elif response.status_code == 200:
            print("✅ Query successful - RLS policies allow read access")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False
    
    # Test 2: Try a simple insert with minimal data
    print("\n2. Testing table insert...")
    insert_url = f"{SUPABASE_URL}/rest/v1/codestorm_registrations"
    
    test_data = {
        'team_name': 'test_team_123',
        'college': 'Test College',
        'branch': 'CS',
        'year_of_study': '3rd Year',
        'idea_title': 'Test Idea',
        'idea_theme': 'AI/ML',
        'ppt_file_path': 'test.pptx',
        'member1_name': 'Test Member 1',
        'member1_email': 'test1@example.com',
        'member1_phone': '1234567890',
        'member1_roll': 'CS001',
        'is_leader1': True,
        'member2_name': 'Test Member 2',
        'member2_email': 'test2@example.com',
        'member2_phone': '1234567891',
        'member2_roll': 'CS002',
        'is_leader2': False,
        'member3_name': 'Test Member 3',
        'member3_email': 'test3@example.com',
        'member3_phone': '1234567892',
        'member3_roll': 'CS003',
        'is_leader3': False,
        'member4_name': 'Test Member 4',
        'member4_email': 'test4@example.com',
        'member4_phone': '1234567893',
        'member4_roll': 'CS004',
        'is_leader4': False,
    }
    
    try:
        response = requests.post(insert_url, json=test_data, headers=headers)
        print(f"Insert response status: {response.status_code}")
        print(f"Insert response: {response.text[:300]}")
        
        if response.status_code == 401:
            print("❌ 401 Unauthorized - RLS policies are blocking inserts")
            print("\n🔧 SOLUTION: You need to either:")
            print("   1. Disable RLS on the codestorm_registrations table, OR")
            print("   2. Create an RLS policy that allows inserts for the anon role")
            return False
        elif response.status_code == 201:
            print("✅ Insert successful!")
            return True
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Insert failed: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()