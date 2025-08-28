#!/usr/bin/env python3
import requests
import json
import time

def test_persistent_auth():
    base_url = "http://localhost:8000/api/v1"
    session = requests.Session()
    
    print("🔐 Testing Persistent Authentication...")
    
    # Step 1: Register and Login
    print("\n1. Registering and Logging in...")
    register_data = {
        "email": "persistent@example.com",
        "password": "password123",
        "first_name": "Persistent",
        "last_name": "User"
    }
    
    try:
        # Register
        response = session.post(
            f"{base_url}/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Registration status: {response.status_code}")
        
        # Login
        login_data = {
            "email": "persistent@example.com",
            "password": "password123"
        }
        
        response = session.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Login status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   Access token: {data.get('access_token', 'Not found')[:20]}...")
            print(f"   User: {data.get('user', {}).get('email', 'Not found')}")
            
            # Check cookies
            cookies = session.cookies
            print(f"   Session cookie: {'session_token' in cookies}")
            print(f"   Refresh cookie: {'refresh_token' in cookies}")
            
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 2: Test multiple API calls with same session
    print("\n2. Testing multiple API calls with same session...")
    
    endpoints = [
        "/users/profile",
        "/resumes/",
        "/jobs/",
        "/applications/",
        "/interviews/"
    ]
    
    for endpoint in endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}")
            print(f"   {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ {endpoint} accessible")
            else:
                print(f"   ❌ {endpoint} failed: {response.text}")
        except Exception as e:
            print(f"   ❌ {endpoint} error: {e}")
    
    # Step 3: Test token refresh
    print("\n3. Testing token refresh...")
    try:
        response = session.post(f"{base_url}/auth/refresh")
        print(f"   Refresh status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Token refresh successful!")
            print(f"   New access token: {data.get('access_token', 'Not found')[:20]}...")
            print(f"   New refresh token: {data.get('refresh_token', 'Not found')[:20]}...")
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Token refresh error: {e}")
    
    # Step 4: Test API calls after refresh
    print("\n4. Testing API calls after token refresh...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Profile after refresh: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Profile accessible after refresh")
        else:
            print(f"   ❌ Profile failed after refresh: {response.text}")
    except Exception as e:
        print(f"   ❌ Profile error after refresh: {e}")
    
    # Step 5: Test session persistence (simulate page refresh)
    print("\n5. Testing session persistence (simulating page refresh)...")
    
    # Create a new session but with the same cookies
    new_session = requests.Session()
    for cookie in session.cookies:
        new_session.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)
    
    try:
        response = new_session.get(f"{base_url}/users/profile")
        print(f"   Profile with new session: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Session persists across requests!")
            data = response.json()
            print(f"   User: {data.get('email', 'Not found')}")
        else:
            print(f"   ❌ Session not persistent: {response.text}")
    except Exception as e:
        print(f"   ❌ Session persistence error: {e}")
    
    # Step 6: Test logout
    print("\n6. Testing logout...")
    try:
        response = session.post(f"{base_url}/auth/logout")
        print(f"   Logout status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Logout successful!")
        else:
            print(f"   ❌ Logout failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    # Step 7: Test access after logout
    print("\n7. Testing access after logout...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Profile after logout: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ Correctly denied access after logout!")
        else:
            print(f"   ⚠️ Unexpected response after logout: {response.text}")
    except Exception as e:
        print(f"   ❌ Error after logout: {e}")
    
    print("\n🎉 Persistent authentication testing completed!")

if __name__ == "__main__":
    test_persistent_auth()
