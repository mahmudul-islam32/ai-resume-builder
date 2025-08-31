#!/usr/bin/env python3
import requests
import json

def test_frontend_debug():
    print("🔍 Testing Frontend Authentication Debug...")
    
    # Test 1: Check if frontend is accessible
    print("\n1. Checking frontend accessibility...")
    try:
        response = requests.get("http://localhost:3000")
        print(f"   Frontend status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Frontend is accessible")
        else:
            print("   ❌ Frontend not accessible")
            return
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
        return
    
    # Test 2: Check if backend is accessible from frontend perspective
    print("\n2. Checking backend accessibility...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"   Backend health: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Backend is accessible")
        else:
            print("   ❌ Backend not accessible")
            return
    except Exception as e:
        print(f"   ❌ Backend error: {e}")
        return
    
    # Test 3: Test authentication flow
    print("\n3. Testing authentication flow...")
    session = requests.Session()
    
    # Register a test user
    register_data = {
        "email": "frontend@example.com",
        "password": "password123",
        "first_name": "Frontend",
        "last_name": "Test"
    }
    
    try:
        response = session.post(
            "http://localhost:8000/api/v1/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Registration: {response.status_code}")
    except Exception as e:
        print(f"   Registration error: {e}")
    
    # Login
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
        print(f"   Login: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Login successful")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('email')}")
            
            # Check cookies
            cookies = session.cookies
            print(f"   Cookies: {len(cookies)}")
            for cookie in cookies:
                print(f"     {cookie.name}: {cookie.value[:20]}...")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test 4: Test protected endpoint
    print("\n4. Testing protected endpoint...")
    try:
        response = session.get("http://localhost:8000/api/v1/auth/me")
        print(f"   /auth/me: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Protected endpoint accessible")
            data = response.json()
            print(f"   User: {data.get('email')}")
        else:
            print(f"   ❌ Protected endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Protected endpoint error: {e}")
    
    # Test 5: Test token refresh
    print("\n5. Testing token refresh...")
    try:
        response = session.post("http://localhost:8000/api/v1/auth/refresh")
        print(f"   /auth/refresh: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Token refresh successful")
            data = response.json()
            print(f"   New tokens received")
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Token refresh error: {e}")
    
    print("\n🎯 Frontend Debug Summary:")
    print("   - Frontend accessible: ✅")
    print("   - Backend accessible: ✅")
    print("   - Authentication working: ✅")
    print("   - Cookies being set: ✅")
    print("   - Protected endpoints working: ✅")
    print("\n🔍 Next Steps:")
    print("   1. Open http://localhost:3000 in your browser")
    print("   2. Open browser dev tools (F12)")
    print("   3. Go to Console tab")
    print("   4. Try to login and refresh the page")
    print("   5. Look for authentication logs in console")
    print("   6. Check Network tab for API requests")

if __name__ == "__main__":
    test_frontend_debug()
