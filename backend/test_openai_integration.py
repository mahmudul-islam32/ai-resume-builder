#!/usr/bin/env python3
"""
Test script to verify OpenAI API integration with the new syntax.
Run this script to test if the OpenAI API is working correctly.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openai_integration():
    """Test the OpenAI API integration."""
    try:
        from openai import AsyncOpenAI
        
        # Check if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            print("Please set OPENAI_API_KEY in your .env file")
            return False
        
        print("✅ OpenAI API key found")
        
        # Test the API call
        client = AsyncOpenAI(api_key=api_key)
        print("✅ AsyncOpenAI client created successfully")
        
        # Simple test prompt
        test_prompt = "Hello, please respond with 'OpenAI API is working correctly!'"
        
        print("🔄 Testing API call...")
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API call successful!")
        print(f"📝 Response: {result}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install OpenAI library: pip install openai>=1.0.0")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_ai_service():
    """Test the AI service integration."""
    try:
        # Import the AI service
        import sys
        sys.path.append('.')
        
        from app.services.ai_service import AIService
        
        print("\n🔄 Testing AI Service...")
        
        ai_service = AIService()
        print("✅ AI Service created successfully")
        
        # Test cover letter generation
        test_resume = "Experienced software developer with 5 years in web development."
        test_job = "Senior Frontend Developer position at TechCorp."
        
        print("🔄 Testing cover letter generation...")
        cover_letter = await ai_service.generate_cover_letter(
            test_resume,
            test_job,
            "TechCorp",
            "Senior Frontend Developer",
            "John Doe"
        )
        
        print("✅ Cover letter generated successfully!")
        print(f"📝 Cover Letter Preview: {cover_letter[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Service error: {e}")
        return False

async def main():
    """Main test function."""
    print("🧪 Testing OpenAI API Integration")
    print("=" * 50)
    
    # Test 1: Basic OpenAI API
    print("\n1️⃣ Testing Basic OpenAI API...")
    openai_success = await test_openai_integration()
    
    # Test 2: AI Service
    print("\n2️⃣ Testing AI Service...")
    service_success = await test_ai_service()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   OpenAI API: {'✅ PASS' if openai_success else '❌ FAIL'}")
    print(f"   AI Service: {'✅ PASS' if service_success else '❌ FAIL'}")
    
    if openai_success and service_success:
        print("\n🎉 All tests passed! OpenAI integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Ensure OPENAI_API_KEY is set in your .env file")
        print("   2. Verify OpenAI library is installed: pip install openai>=1.0.0")
        print("   3. Check your internet connection")
        print("   4. Verify your OpenAI API key is valid and has credits")

if __name__ == "__main__":
    asyncio.run(main())
