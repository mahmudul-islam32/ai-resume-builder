#!/usr/bin/env python3
"""
Test script for Ollama integration through the API.
"""

import requests
import json


def test_cover_letter_generation():
    """Test cover letter generation through the API."""
    print("🧪 Testing Ollama Cover Letter Generation via API")
    print("=" * 50)
    
    # Test data
    test_data = {
        "resume_content": "Experienced software developer with 5 years of experience in Python, JavaScript, and React. Led development of multiple web applications and improved system performance by 40%.",
        "job_description": "We are looking for a skilled software developer to join our team. The ideal candidate should have experience with Python, JavaScript, and modern web frameworks.",
        "company_name": "Tech Corp",
        "job_title": "Software Developer",
        "applicant_name": "John Doe",
        "customization": {
            "tone": "professional",
            "focus_areas": ["technical skills", "leadership"],
            "custom_instructions": "Emphasize the performance improvement achievement"
        }
    }
    
    # Test the customized cover letter endpoint
    print("🔍 Testing customized cover letter generation...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/ai/generate-customized-cover-letter",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Cover letter generated successfully!")
            print(f"📄 Generated cover letter:")
            print("=" * 50)
            print(result.get("content", "No content found"))
            print("=" * 50)
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")


def test_model_configuration():
    """Test model configuration endpoint."""
    print("\n🔧 Testing Model Configuration")
    print("=" * 30)
    
    try:
        # Get available models
        response = requests.get("http://localhost:8000/api/v1/ai/available-models")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Available models: {models['models']}")
            print(f"Current model: {models['current_model']}")
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")


if __name__ == "__main__":
    test_model_configuration()
    test_cover_letter_generation()
