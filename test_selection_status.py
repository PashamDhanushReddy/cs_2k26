#!/usr/bin/env python3
"""
Test script to verify the selection status update functionality
"""

import requests
import json

def test_selection_status_update():
    """Test the selection status update endpoint"""
    
    # Test data - you'll need to adjust these based on your actual data
    test_data = {
        'registration_id': 'test_registration_id',  # Replace with actual registration ID
        'selection_status': 'selected'
    }
    
    try:
        # Test the endpoint
        response = requests.post(
            'http://127.0.0.1:8000/update-selection-status/',
            data=json.dumps(test_data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Selection status update endpoint is working!")
        else:
            print("❌ Selection status update endpoint returned an error")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_selection_status_update()