#!/usr/bin/env python3
"""
Test script for custom model integration.
Use this to test your custom model before integrating it into the main application.
"""

import asyncio
import json
import os
from typing import Optional

# Add the backend directory to Python path
import sys
sys.path.append('./backend')

from app.services.my_custom_model import MyCustomModel, HuggingFaceInferenceModel, OllamaModel, CohereModel
from app.services.custom_model_service import CustomModelService


async def test_model_availability(model):
    """Test if the model is available."""
    print(f"🔍 Testing model availability...")
    is_available = await model.is_available()
    print(f"✅ Model available: {is_available}")
    return is_available


async def test_text_generation(model, prompt: str):
    """Test text generation with the model."""
    print(f"🔍 Testing text generation...")
    print(f"📝 Prompt: {prompt[:100]}...")
    
    try:
        response = await model.generate_text(prompt, max_tokens=500, temperature=0.7)
        print(f"✅ Generated text ({len(response)} characters):")
        print(f"📄 {response[:200]}...")
        return response
    except Exception as e:
        print(f"❌ Text generation failed: {str(e)}")
        return None


async def test_cover_letter_generation(model_type: str, config: dict):
    """Test cover letter generation with the custom model."""
    print(f"\n🚀 Testing cover letter generation with {model_type}")
    print(f"⚙️  Configuration: {json.dumps(config, indent=2)}")
    
    # Create model instance
    if model_type == "custom":
        model = MyCustomModel(**config)
    elif model_type == "huggingface_inference":
        model = HuggingFaceInferenceModel(**config)
    elif model_type == "ollama":
        model = OllamaModel(**config)
    elif model_type == "cohere":
        model = CohereModel(**config)
    else:
        print(f"❌ Unknown model type: {model_type}")
        return
    
    # Test availability
    if not await test_model_availability(model):
        print(f"❌ Model {model_type} is not available")
        return
    
    # Test basic text generation
    test_prompt = "Write a short professional greeting."
    basic_response = await test_text_generation(model, test_prompt)
    
    if not basic_response:
        print(f"❌ Basic text generation failed for {model_type}")
        return
    
    # Test cover letter generation
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
    
    print(f"\n📝 Testing cover letter generation...")
    cover_letter = await test_text_generation(model, cover_letter_prompt)
    
    if cover_letter:
        print(f"✅ Cover letter generation successful!")
        print(f"📄 Generated cover letter:")
        print("=" * 50)
        print(cover_letter)
        print("=" * 50)
    else:
        print(f"❌ Cover letter generation failed")


def get_model_config():
    """Get model configuration from user input."""
    print("🤖 Custom Model Test Configuration")
    print("=" * 40)
    
    model_types = [
        "custom",
        "huggingface_inference", 
        "ollama",
        "cohere"
    ]
    
    print("Available model types:")
    for i, model_type in enumerate(model_types, 1):
        print(f"  {i}. {model_type}")
    
    while True:
        try:
            choice = int(input(f"\nSelect model type (1-{len(model_types)}): ")) - 1
            if 0 <= choice < len(model_types):
                model_type = model_types[choice]
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    config = {}
    
    if model_type == "custom":
        config["api_url"] = input("Enter API URL: ").strip()
        config["api_key"] = input("Enter API Key: ").strip()
        config["model_name"] = input("Enter Model Name (optional, default: my-model): ").strip() or "my-model"
    
    elif model_type == "huggingface_inference":
        config["model_name"] = input("Enter Hugging Face model name (e.g., gpt2): ").strip()
        config["api_token"] = input("Enter Hugging Face API token: ").strip()
    
    elif model_type == "ollama":
        config["model_name"] = input("Enter Ollama model name (e.g., llama2): ").strip()
        config["api_url"] = input("Enter Ollama API URL (default: http://localhost:11434): ").strip() or "http://localhost:11434"
    
    elif model_type == "cohere":
        config["api_key"] = input("Enter Cohere API key: ").strip()
        config["model"] = input("Enter Cohere model name (default: command): ").strip() or "command"
    
    return model_type, config


async def main():
    """Main test function."""
    print("🧪 Custom Model Integration Test")
    print("=" * 40)
    
    # Get model configuration
    model_type, config = get_model_config()
    
    # Test the model
    await test_cover_letter_generation(model_type, config)
    
    print(f"\n✅ Test completed for {model_type}")


if __name__ == "__main__":
    asyncio.run(main())
