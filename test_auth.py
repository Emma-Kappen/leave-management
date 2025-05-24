import urllib.request
import urllib.parse
import json
import os
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_auth():
    # Read users.json to get credentials
    with open(os.path.join('backend', 'users.json'), 'r') as f:
        users = json.load(f)
    
    # Test student login
    student_id = "1CS21CS001"
    student_password = users[student_id]
    
    print(f"Testing student login with ID: {student_id} and password: {student_password}")
    
    # Create request data
    data = json.dumps({"user_id": student_id, "password": student_password}).encode('utf-8')
    
    # Create request
    req = urllib.request.Request(
        "http://127.0.0.1:5000/auth/login",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        # Send request
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            print(f"Student login response status: {response.status}")
            print(f"Student login response body: {response_data}")
    except urllib.error.HTTPError as e:
        print(f"Student login error: {e.code} - {e.reason}")
        response_data = e.read().decode('utf-8')
        print(f"Error response: {response_data}")
    except Exception as e:
        print(f"Error: {e}")

    # Print the path to users.json to verify it's correct
    print(f"\nPath to users.json: {os.path.abspath(os.path.join('backend', 'users.json'))}")
    
    # Print the content of users.json
    print("\nContent of users.json:")
    print(json.dumps(users, indent=2))

if __name__ == "__main__":
    test_auth()