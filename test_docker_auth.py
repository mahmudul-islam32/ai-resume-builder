#!/usr/bin/env python3
import requests
import json
import time

def test_docker_auth():
    base_url = "http://localhost:8000/api/v1"
    session = requests.Session()
    
    print("🐳 Testing Docker Authentication...")
    
    # Test 1: Check if backend is running
    print("\n1. Checking backend status...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"   Backend health: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print("   ❌ Backend health check failed")
            return
    except Exception as e:
        print(f"   ❌ Backend not accessible: {e}")
        print("   Make sure Docker containers are running with: docker-compose up")
        return
    
    # Test 2: Register user
    print("\n2. Registering test user...")
    register_data = {
        "email": "docker@example.com",
        "password": "password123",
        "first_name": "Docker",
        "last_name": "User"
    }
    
    try:
        response = session.post(
            f"{base_url}/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Registration: {response.status_code}")
        if response.status_code == 400:
            print("   ⚠️ User might already exist, continuing...")
    except Exception as e:
        print(f"   Registration error: {e}")
    
    # Test 3: Login and check cookies
    print("\n3. Logging in and checking cookies...")
    login_data = {
        "email": "docker@example.com",
        "password": "password123"
    }
    
    try:
        response = session.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Login status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   Response includes tokens: {bool(data.get('access_token'))}")
            print(f"   Response includes user: {bool(data.get('user'))}")
            
            # Check cookies
            cookies = session.cookies
            print(f"   Total cookies: {len(cookies)}")
            
            for cookie in cookies:
                print(f"   Cookie: {cookie.name}")
                print(f"     Value: {cookie.value[:20]}...")
                print(f"     Secure: {cookie.secure}")
                print(f"     HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
                print(f"     SameSite: {cookie.get_nonstandard_attr('SameSite')}")
            
            # Check for required cookies
            session_cookie = cookies.get('session_token')
            refresh_cookie = cookies.get('refresh_token')
            
            if session_cookie:
                print(f"   ✅ session_token cookie found")
                if not session_cookie.secure:
                    print(f"   ✅ Cookie is NOT secure (good for HTTP development)")
                else:
                    print(f"   ⚠️ Cookie is secure (might not work with HTTP)")
            else:
                print(f"   ❌ session_token cookie missing")
                
            if refresh_cookie:
                print(f"   ✅ refresh_token cookie found")
                if not refresh_cookie.secure:
                    print(f"   ✅ Cookie is NOT secure (good for HTTP development)")
                else:
                    print(f"   ⚠️ Cookie is secure (might not work with HTTP)")
            else:
                print(f"   ❌ refresh_token cookie missing")
                
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test 4: Test protected endpoint with cookies
    print("\n4. Testing protected endpoint with cookies...")
    try:
        response = session.get(f"{base_url}/auth/me")
        print(f"   /auth/me status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Authentication working with cookies!")
            print(f"   User: {data.get('email')}")
        else:
            print(f"   ❌ Authentication failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
    
    # Test 5: Test token refresh
    print("\n5. Testing token refresh...")
    try:
        response = session.post(f"{base_url}/auth/refresh")
        print(f"   Refresh status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Token refresh successful!")
            print(f"   New access token: {data.get('access_token', 'Not found')[:20]}...")
            
            # Check if cookies were updated
            new_cookies = session.cookies
            new_session_cookie = new_cookies.get('session_token')
            print(f"   Updated session cookie: {new_session_cookie[:20] if new_session_cookie else 'Not found'}...")
            
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Token refresh error: {e}")
    
    # Test 6: Test logout
    print("\n6. Testing logout...")
    try:
        response = session.post(f"{base_url}/auth/logout")
        print(f"   Logout status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Logout successful!")
            
            # Check if cookies were cleared
            remaining_cookies = session.cookies
            print(f"   Remaining cookies after logout: {len(remaining_cookies)}")
            
            if len(remaining_cookies) == 0:
                print(f"   ✅ All cookies cleared!")
            else:
                print(f"   ⚠️ Cookies still present: {[c.name for c in remaining_cookies]}")
                
        else:
            print(f"   ❌ Logout failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    print("\n🎉 Docker authentication testing completed!")
    print("\n📋 Summary:")
    print("   - If cookies are NOT secure: Authentication should work with HTTP")
    print("   - If cookies are secure: Authentication will only work with HTTPS")
    print("   - Make sure DEVELOPMENT_MODE=true is set in Docker environment")

if __name__ == "__main__":
    test_docker_auth()
