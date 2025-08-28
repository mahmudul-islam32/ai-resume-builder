#!/usr/bin/env python3
import requests
import json

def test_cookie_auth():
    base_url = "http://localhost:8000/api/v1"
    session = requests.Session()
    
    print("🍪 Testing Cookie-Based Authentication...")
    
    # Step 1: Register a user
    print("\n1. Registering user...")
    register_data = {
        "email": "cookie@example.com",
        "password": "password123",
        "first_name": "Cookie",
        "last_name": "User"
    }
    
    try:
        response = session.post(
            f"{base_url}/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Registration status: {response.status_code}")
    except Exception as e:
        print(f"   Registration error: {e}")
    
    # Step 2: Login and check cookies
    print("\n2. Logging in and checking cookies...")
    login_data = {
        "email": "cookie@example.com",
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
                print(f"   Cookie: {cookie.name} = {cookie.value[:20]}... (HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}, Secure: {cookie.secure})")
            
            # Verify session_token cookie exists
            session_cookie = cookies.get('session_token')
            refresh_cookie = cookies.get('refresh_token')
            
            if session_cookie:
                print(f"   ✅ Session token cookie found: {session_cookie[:20]}...")
            else:
                print(f"   ❌ Session token cookie NOT found!")
                
            if refresh_cookie:
                print(f"   ✅ Refresh token cookie found: {refresh_cookie[:20]}...")
            else:
                print(f"   ❌ Refresh token cookie NOT found!")
                
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 3: Test protected endpoint with cookies only
    print("\n3. Testing protected endpoint with cookies only...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Profile status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Protected endpoint accessible with cookies!")
            print(f"   User: {data.get('email')}")
        else:
            print(f"   ❌ Protected endpoint failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Protected endpoint error: {e}")
    
    # Step 4: Test without cookies (should fail)
    print("\n4. Testing without cookies (should fail)...")
    new_session = requests.Session()  # Fresh session without cookies
    
    try:
        response = new_session.get(f"{base_url}/users/profile")
        print(f"   Profile status without cookies: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly denied access without cookies!")
        else:
            print(f"   ⚠️ Unexpected response without cookies: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error without cookies: {e}")
    
    # Step 5: Test token refresh
    print("\n5. Testing token refresh...")
    try:
        response = session.post(f"{base_url}/auth/refresh")
        print(f"   Refresh status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Token refresh successful!")
            print(f"   New access token: {data.get('access_token', 'Not found')[:20]}...")
            print(f"   New refresh token: {data.get('refresh_token', 'Not found')[:20]}...")
            
            # Check if cookies were updated
            new_cookies = session.cookies
            new_session_cookie = new_cookies.get('session_token')
            new_refresh_cookie = new_cookies.get('refresh_token')
            
            print(f"   Updated session cookie: {new_session_cookie[:20] if new_session_cookie else 'Not found'}...")
            print(f"   Updated refresh cookie: {new_refresh_cookie[:20] if new_refresh_cookie else 'Not found'}...")
            
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Token refresh error: {e}")
    
    # Step 6: Test logout
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
    
    # Step 7: Test access after logout
    print("\n7. Testing access after logout...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Profile status after logout: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly denied access after logout!")
        else:
            print(f"   ⚠️ Unexpected response after logout: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error after logout: {e}")
    
    print("\n🎉 Cookie-based authentication testing completed!")

if __name__ == "__main__":
    test_cookie_auth()
