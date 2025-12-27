#!/usr/bin/env python3
"""
Test script to verify PPT link functionality in admin dashboard
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs_admin.settings')
django.setup()

from dashboard.views import admin_dashboard

def test_ppt_links():
    """Test that PPT links are properly included in the admin dashboard data"""
    try:
        # Mock request object
        class MockRequest:
            def __init__(self):
                self.method = 'GET'
        
        request = MockRequest()
        
        # Call the admin dashboard view
        response = admin_dashboard(request)
        
        # Check if the response contains PPT link data
        if hasattr(response, 'context_data'):
            registrations = response.context_data.get('registrations', [])
            
            print(f"Found {len(registrations)} registrations")
            
            # Check first few registrations for PPT links
            for i, reg in enumerate(registrations[:3]):
                print(f"\nRegistration {i+1}:")
                print(f"  Team Name: {reg.get('team_name', 'N/A')}")
                print(f"  PPT File Path: {reg.get('ppt_file_path', 'Not found')}")
                
                # Check if PPT link is present and valid
                ppt_path = reg.get('ppt_file_path', '')
                if ppt_path:
                    print(f"  ✓ PPT link found: {ppt_path}")
                else:
                    print(f"  ✗ No PPT link found")
                    
        else:
            print("No context data found in response")
            
    except Exception as e:
        print(f"Error testing PPT links: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing PPT links in admin dashboard...")
    test_ppt_links()
    print("\nTest completed!")