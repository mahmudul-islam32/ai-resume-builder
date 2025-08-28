#!/usr/bin/env python3
"""
Test script to test the ATS endpoint with authentication
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_ats_endpoint():
    """Test the ATS endpoint with proper authentication"""
    
    # Step 1: Register a test user
    print("1. Registering test user...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 200:
        print("✅ User registered successfully")
    elif response.status_code == 422:
        print("⚠️  User might already exist, trying to login...")
    else:
        print(f"❌ Registration failed: {response.status_code} - {response.text}")
        return
    
    # Step 2: Login to get token
    print("2. Logging in...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return
    
    token_data = response.json()
    access_token = token_data["access_token"]
    print("✅ Login successful")
    
    # Step 3: Test ATS endpoint with authentication
    print("3. Testing ATS endpoint...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    ats_request = {
        "resume_text": """
        SOFTWARE ENGINEER
        
        EXPERIENCE
        Senior Software Engineer | TechCorp | 2020-2023
        - Developed and maintained Python-based web applications using Django and Flask
        - Implemented REST APIs and microservices architecture
        - Used PostgreSQL and Redis for data storage and caching
        - Deployed applications using Docker and AWS (EC2, S3, Lambda)
        - Collaborated with cross-functional teams using Agile methodologies
        
        SKILLS
        Programming: Python, JavaScript, SQL, HTML, CSS
        Frameworks: Django, Flask, React, Node.js, Express
        Databases: PostgreSQL, Redis, MySQL
        Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
        """,
        "job_description": """
        Senior Software Engineer
        
        We are looking for a Senior Software Engineer to join our team. You will be responsible for developing scalable web applications and APIs.
        
        Requirements:
        - 5+ years of experience in software development
        - Strong proficiency in Python and JavaScript
        - Experience with Django, Flask, or similar frameworks
        - Knowledge of PostgreSQL and Redis
        - Experience with AWS cloud services
        - Familiarity with Docker and containerization
        - Experience with REST APIs and microservices
        - Strong problem-solving and communication skills
        """,
        "job_title": "Senior Software Engineer"
    }
    
    response = requests.post(f"{BASE_URL}/ats/score-resume", json=ats_request, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ ATS endpoint working!")
        print(f"Overall Score: {result['overall_score']}%")
        print(f"Keyword Score: {result['keyword_score']}%")
        print(f"Semantic Score: {result['semantic_score']}%")
        print(f"Format Score: {result['format_score']}%")
        print(f"Experience Score: {result['experience_score']}%")
        print(f"Confidence: {result['confidence']}%")
        
        print("\nSuggestions:")
        for suggestion in result['suggestions'][:3]:
            print(f"  • {suggestion}")
            
    else:
        print(f"❌ ATS endpoint failed: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_ats_endpoint()
