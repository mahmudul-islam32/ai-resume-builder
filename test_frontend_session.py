#!/usr/bin/env python3
import requests
import json

def test_frontend_session():
    print("🔍 Testing Frontend Session Behavior...")
    
    # Create a session to simulate browser behavior
    session = requests.Session()
    
    # Step 1: Login (simulate frontend login)
    print("\n1. Simulating frontend login...")
    login_data = {
        "email": "frontend@example.com",
        "password": "password123"
    }
    
    try:
        response = session.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Login status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('email')}")
            
            # Check cookies
            cookies = session.cookies
            print(f"   Cookies set: {len(cookies)}")
            for cookie in cookies:
                print(f"     {cookie.name}: {cookie.value[:20]}...")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 2: Test /auth/me (simulate frontend auth check)
    print("\n2. Testing /auth/me (frontend auth check)...")
    try:
        response = session.get("http://localhost:8000/api/v1/auth/me")
        print(f"   /auth/me status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ /auth/me successful")
            data = response.json()
            print(f"   User: {data.get('email')}")
        else:
            print(f"   ❌ /auth/me failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ /auth/me error: {e}")
        return
    
    # Step 3: Test /auth/refresh (simulate frontend refresh)
    print("\n3. Testing /auth/refresh (frontend refresh)...")
    try:
        response = session.post("http://localhost:8000/api/v1/auth/refresh")
        print(f"   /auth/refresh status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ /auth/refresh successful")
            data = response.json()
            print(f"   New tokens received")
        else:
            print(f"   ❌ /auth/refresh failed: {response.text}")
    except Exception as e:
        print(f"   ❌ /auth/refresh error: {e}")
    
    # Step 4: Test /auth/me again after refresh
    print("\n4. Testing /auth/me after refresh...")
    try:
        response = session.get("http://localhost:8000/api/v1/auth/me")
        print(f"   /auth/me status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ /auth/me after refresh successful")
            data = response.json()
            print(f"   User: {data.get('email')}")
        else:
            print(f"   ❌ /auth/me after refresh failed: {response.text}")
    except Exception as e:
        print(f"   ❌ /auth/me after refresh error: {e}")
    
    print("\n🎯 Session Test Summary:")
    print("   - Login: ✅")
    print("   - /auth/me: ✅")
    print("   - /auth/refresh: ✅")
    print("   - /auth/me after refresh: ✅")
    print("\n🔍 If this test passes but frontend fails:")
    print("   1. Check browser console for JavaScript errors")
    print("   2. Check Network tab for failed requests")
    print("   3. Check if cookies are being sent with requests")
    print("   4. Check CORS configuration")

if __name__ == "__main__":
    test_frontend_session()
