#!/usr/bin/env python3
import requests
import json

def test_auth():
    base_url = "http://localhost:8000/api/v1"
    session = requests.Session()
    
    print("🔐 Testing Authentication System...")
    
    # Test 1: Register a new user
    print("\n1. Testing Registration...")
    register_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = session.post(
            f"{base_url}/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Registration successful!")
        else:
            print(f"   ⚠️ Registration response: {response.text}")
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
    
    # Test 2: Login
    print("\n2. Testing Login...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = session.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful!")
            data = response.json()
            print(f"   Access token: {data.get('access_token', 'Not found')[:20]}...")
            print(f"   Refresh token: {data.get('refresh_token', 'Not found')[:20]}...")
            print(f"   User email: {data.get('user', {}).get('email', 'Not found')}")
            
            # Check cookies
            cookies = session.cookies
            print(f"   Session cookie: {'session_token' in cookies}")
            print(f"   Refresh cookie: {'refresh_token' in cookies}")
            
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test 3: Access protected endpoint
    print("\n3. Testing Protected Endpoint...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Protected endpoint accessible!")
            data = response.json()
            print(f"   User: {data.get('email', 'Not found')}")
        else:
            print(f"   ❌ Protected endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Protected endpoint error: {e}")
    
    # Test 4: Token refresh
    print("\n4. Testing Token Refresh...")
    try:
        response = session.post(f"{base_url}/auth/refresh")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Token refresh successful!")
            data = response.json()
            print(f"   New access token: {data.get('access_token', 'Not found')[:20]}...")
            print(f"   New refresh token: {data.get('refresh_token', 'Not found')[:20]}...")
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Token refresh error: {e}")
    
    # Test 5: Logout
    print("\n5. Testing Logout...")
    try:
        response = session.post(f"{base_url}/auth/logout")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Logout successful!")
        else:
            print(f"   ❌ Logout failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    # Test 6: Try to access protected endpoint after logout
    print("\n6. Testing Protected Endpoint After Logout...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly denied access after logout!")
        else:
            print(f"   ⚠️ Unexpected response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 Authentication testing completed!")

if __name__ == "__main__":
    test_auth()
