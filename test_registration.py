import requests

# Test registration form submission
base_url = "http://127.0.0.1:8000"

# Get the registration page to obtain CSRF token
session = requests.Session()
response = session.get(f"{base_url}/register/")

print(f"Registration Page Status: {response.status_code}")
if response.status_code == 200:
    # Extract CSRF token from cookies
    csrf_token = session.cookies.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")
    
    # Test form submission
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'team_name': 'Test Team',
        'college': 'Test College',
        'branch': 'CSE',
        'year_of_study': '3',
        'idea_title': 'Test Idea',
        'idea_theme': 'Generative AI & LLM Applications',
        'member1_name': 'Test Member 1',
        'member1_email': 'test1@example.com',
        'member1_phone': '1234567890',
        'member1_roll': 'CS001',
        'is_leader1': 'on',
        'member2_name': 'Test Member 2',
        'member2_email': 'test2@example.com',
        'member2_phone': '1234567891',
        'member2_roll': 'CS002',
        'member3_name': 'Test Member 3',
        'member3_email': 'test3@example.com',
        'member3_phone': '1234567892',
        'member3_roll': 'CS003',
        'member4_name': 'Test Member 4',
        'member4_email': 'test4@example.com',
        'member4_phone': '1234567893',
        'member4_roll': 'CS004',
    }
    
    # Test without file first (will fail validation but should not fail CSRF)
    response = session.post(f"{base_url}/register/", data=data)
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ CSRF verification passed!")
        # Check if it's a validation error (expected without file)
        if 'PPT file upload is required' in response.text:
            print("✅ Form validation working correctly")
        else:
            print("Response contains:", response.text[:200])
    else:
        print("❌ CSRF or other error:")
        print(response.text[:500])
else:
    print(f"Failed to get registration page: {response.status_code}")