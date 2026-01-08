import requests

API_URL = "http://127.0.0.1:8000"

def test_auth():
    print("Testing Authentication...")
    
    # 1. Test Login
    login_data = {
        "username": "admin",
        "password": "adminpassword"
    }
    response = requests.post(f"{API_URL}/auth/login", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✓ Login successful")
        
        # 2. Test /auth/me
        headers = {"Authorization": f"Bearer {token}"}
        me_response = requests.get(f"{API_URL}/auth/me", headers=headers)
        if me_response.status_code == 200:
            print(f"✓ /auth/me successful: {me_response.json()['username']} ({me_response.json()['role']})")
        else:
            print(f"✗ /auth/me failed: {me_response.status_code}")
            
        # 3. Test protected endpoint (employees list)
        emp_response = requests.get(f"{API_URL}/api/employees/", headers=headers)
        if emp_response.status_code == 200:
            print(f"✓ Protected endpoint access successful (Admin)")
        else:
            print(f"✗ Protected endpoint access failed: {emp_response.status_code}")
            
    else:
        print(f"✗ Login failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_auth()
