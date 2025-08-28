#!/usr/bin/env python3
import requests
import json

# Test the ATS scoring endpoint with secure cookie authentication
def test_ats_scoring():
    base_url = "http://localhost:8000/api/v1"
    
    # Create a session to handle cookies
    session = requests.Session()
    
    # First, try to login to get cookies
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        # Try to login
        login_response = session.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Login response status: {login_response.status_code}")
        print(f"Login response: {login_response.text}")
        
        if login_response.status_code == 200:
            print("✅ Login successful!")
            login_data = login_response.json()
            print(f"Access token: {login_data.get('access_token', 'Not found')[:20]}...")
            print(f"Refresh token: {login_data.get('refresh_token', 'Not found')[:20]}...")
            print(f"User: {login_data.get('user', {}).get('email', 'Not found')}")
            
            # Test ATS scoring with session cookies
            ats_request = {
                "resume_text": "Software Engineer with 5 years experience in Python, JavaScript, React, and Node.js. Strong background in web development and cloud technologies.",
                "job_description": "We are looking for a Software Engineer with experience in Python, JavaScript, and React. Knowledge of cloud technologies is a plus."
            }
            
            ats_response = session.post(
                f"{base_url}/ats/score-resume",
                json=ats_request,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"ATS response status: {ats_response.status_code}")
            print(f"ATS response: {ats_response.text}")
            
            if ats_response.status_code == 200:
                print("✅ ATS scoring successful!")
            else:
                print("❌ ATS scoring failed!")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ats_scoring()
