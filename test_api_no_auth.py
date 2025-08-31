#!/usr/bin/env python3
import requests
import json

# Test the API endpoints with secure cookie authentication
def test_api_endpoints():
    base_url = "http://localhost:8000/api/v1"
    
    # Create a session to handle cookies
    session = requests.Session()
    
    print("🧪 Testing API endpoints with secure cookie authentication...")
    
    # First, try to login to get cookies
    print("\n1. Testing Login...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        login_response = session.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {login_response.status_code}")
        if login_response.status_code == 200:
            print("   ✅ Login successful!")
            response_data = login_response.json()
            print(f"   Access token: {response_data.get('access_token', 'Not found')[:20]}...")
            print(f"   Refresh token: {response_data.get('refresh_token', 'Not found')[:20]}...")
            print(f"   User: {response_data.get('user', {}).get('email', 'Not found')}")
        else:
            print(f"   ❌ Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: ATS Scoring
    print("\n2. Testing ATS Scoring...")
    ats_request = {
        "resume_text": "Software Engineer with 5 years experience in Python, JavaScript, React, and Node.js. Strong background in web development and cloud technologies.",
        "job_description": "We are looking for a Software Engineer with experience in Python, JavaScript, and React. Knowledge of cloud technologies is a plus."
    }
    
    try:
        response = session.post(
            f"{base_url}/ats/score-resume",
            json=ats_request,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ ATS scoring works!")
        else:
            print(f"   ❌ ATS scoring failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get Resumes
    print("\n3. Testing Get Resumes...")
    try:
        response = session.get(f"{base_url}/resumes/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Get resumes works!")
        else:
            print(f"   ❌ Get resumes failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Get Job Postings
    print("\n4. Testing Get Job Postings...")
    try:
        response = session.get(f"{base_url}/jobs/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Get job postings works!")
        else:
            print(f"   ❌ Get job postings failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Get Applications
    print("\n5. Testing Get Applications...")
    try:
        response = session.get(f"{base_url}/applications/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Get applications works!")
        else:
            print(f"   ❌ Get applications failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Get Interviews
    print("\n6. Testing Get Interviews...")
    try:
        response = session.get(f"{base_url}/interviews/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Get interviews works!")
        else:
            print(f"   ❌ Get interviews failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Get User Profile
    print("\n7. Testing Get User Profile...")
    try:
        response = session.get(f"{base_url}/users/profile")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Get user profile works!")
        else:
            print(f"   ❌ Get user profile failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Dashboard Stats
    print("\n8. Testing Dashboard Stats...")
    try:
        response = session.get(f"{base_url}/applications/stats/dashboard")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard stats works!")
        else:
            print(f"   ❌ Dashboard stats failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 9: Token Refresh
    print("\n9. Testing Token Refresh...")
    try:
        response = session.post(f"{base_url}/auth/refresh")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Token refresh works!")
            response_data = response.json()
            print(f"   New access token: {response_data.get('access_token', 'Not found')[:20]}...")
            print(f"   New refresh token: {response_data.get('refresh_token', 'Not found')[:20]}...")
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 10: Logout
    print("\n10. Testing Logout...")
    try:
        response = session.post(f"{base_url}/auth/logout")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Logout works!")
        else:
            print(f"   ❌ Logout failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api_endpoints()
