#!/usr/bin/env python3
"""
Simple test script for Ollama generation (bypassing availability check).
"""

import asyncio
import sys
sys.path.append('./backend')

from app.services.my_custom_model import OllamaModel


async def test_ollama_generation():
    """Test Ollama text generation directly."""
    print("🧪 Testing Ollama Generation")
    print("=" * 40)
    
    # Create Ollama model instance
    model = OllamaModel(
        model_name="llama2",
        api_url="http://localhost:11434"
    )
    
    # Test basic text generation directly
    print("🔍 Testing basic text generation...")
    test_prompt = "Write a short professional greeting."
    print(f"📝 Prompt: {test_prompt}")
    
    try:
        response = await model.generate_text(test_prompt, max_tokens=100)
        print(f"✅ Generated text ({len(response)} characters):")
        print(f"📄 {response}")
    except Exception as e:
        print(f"❌ Text generation failed: {str(e)}")
        return
    
    # Test cover letter generation
    print("\n🔍 Testing cover letter generation...")
    cover_letter_prompt = """
    You are an expert cover letter writer. Create a compelling, personalized cover letter based on the following information:

    APPLICANT NAME: John Doe
    JOB TITLE: Software Developer
    COMPANY: Tech Corp

    RESUME CONTENT:
    Experienced software developer with 5 years of experience in Python, JavaScript, and React. Led development of multiple web applications and improved system performance by 40%.

    JOB DESCRIPTION:
    We are looking for a skilled software developer to join our team. The ideal candidate should have experience with Python, JavaScript, and modern web frameworks.

    Create a professional cover letter that:
    - Is addressed to the hiring manager
    - Shows enthusiasm for the specific role and company
    - Highlights relevant experience from the resume
    - Demonstrates knowledge of the company/role
    - Is concise (3-4 paragraphs)
    - Has a professional tone
    - Includes a strong opening and closing

    Return only the cover letter text, properly formatted.
    """
    
    try:
        cover_letter = await model.generate_text(cover_letter_prompt, max_tokens=500)
        print(f"✅ Cover letter generation successful!")
        print(f"📄 Generated cover letter:")
        print("=" * 50)
        print(cover_letter)
        print("=" * 50)
    except Exception as e:
        print(f"❌ Cover letter generation failed: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_ollama_generation())
