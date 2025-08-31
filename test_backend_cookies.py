#!/usr/bin/env python3
import requests
import json

def test_backend_cookies():
    base_url = "http://localhost:8000/api/v1"
    session = requests.Session()
    
    print("🔧 Testing Backend Cookie Settings...")
    
    # Test 1: Check if backend is running
    print("\n1. Checking backend status...")
    try:
        response = requests.get(f"{base_url.replace('/api/v1', '')}/health")
        print(f"   Backend health: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print("   ❌ Backend health check failed")
            return
    except Exception as e:
        print(f"   ❌ Backend not accessible: {e}")
        return
    
    # Test 2: Register user
    print("\n2. Registering test user...")
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
        print(f"   Registration: {response.status_code}")
    except Exception as e:
        print(f"   Registration error: {e}")
    
    # Test 3: Login and inspect response
    print("\n3. Logging in and inspecting response...")
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
        
        print(f"   Login status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful")
            print(f"   Response body keys: {list(data.keys())}")
            
            # Check cookies in response
            cookies = session.cookies
            print(f"   Cookies in session: {len(cookies)}")
            
            for cookie in cookies:
                print(f"   Cookie: {cookie.name}")
                print(f"     Value: {cookie.value[:20]}...")
                print(f"     Domain: {cookie.domain}")
                print(f"     Path: {cookie.path}")
                print(f"     Secure: {cookie.secure}")
                print(f"     HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
                print(f"     SameSite: {cookie.get_nonstandard_attr('SameSite')}")
                print(f"     Expires: {cookie.expires}")
            
            # Check for required cookies
            session_cookie = cookies.get('session_token')
            refresh_cookie = cookies.get('refresh_token')
            
            if session_cookie:
                print(f"   ✅ session_token cookie found")
            else:
                print(f"   ❌ session_token cookie missing")
                
            if refresh_cookie:
                print(f"   ✅ refresh_token cookie found")
            else:
                print(f"   ❌ refresh_token cookie missing")
                
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test 4: Test authentication with cookies
    print("\n4. Testing authentication with cookies...")
    try:
        response = session.get(f"{base_url}/auth/me")
        print(f"   /auth/me status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Authentication working with cookies")
            print(f"   User: {data.get('email')}")
        else:
            print(f"   ❌ Authentication failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
    
    # Test 5: Test without cookies
    print("\n5. Testing without cookies...")
    new_session = requests.Session()
    
    try:
        response = new_session.get(f"{base_url}/auth/me")
        print(f"   /auth/me without cookies: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly denied without cookies")
        else:
            print(f"   ⚠️ Unexpected response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error without cookies: {e}")
    
    print("\n🎉 Backend cookie testing completed!")

if __name__ == "__main__":
    test_backend_cookies()
