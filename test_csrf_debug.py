import requests

# Test CSRF debug endpoint
base_url = "http://127.0.0.1:8000"

# Get the CSRF debug page
session = requests.Session()
response = session.get(f"{base_url}/csrf-debug/")

print(f"CSRF Debug Page Status: {response.status_code}")
if response.status_code == 200:
    # Check cookies
    print(f"Cookies: {session.cookies}")
    print(f"CSRF Token from cookies: {session.cookies.get('csrftoken')}")
    
    # Try POST with CSRF token
    csrf_token = session.cookies.get('csrftoken')
    if csrf_token:
        data = {'csrfmiddlewaretoken': csrf_token}
        response = session.post(f"{base_url}/csrf-debug/", data=data)
        print(f"POST Response Status: {response.status_code}")
        print(f"POST Response: {response.text[:200]}...")