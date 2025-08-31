#!/usr/bin/env python3
"""
Configuration script for custom model integration.
This script helps you configure your custom model for the AI Resume application.
"""

import json
import os
import sys
from typing import Dict, Any


def create_env_config(model_type: str, config: Dict[str, Any]) -> str:
    """Create environment configuration string."""
    env_lines = [
        "# Custom Model Configuration",
        f"USE_CUSTOM_MODEL=true",
        f"CUSTOM_MODEL_TYPE={model_type}",
        f"CUSTOM_MODEL_CONFIG={json.dumps(config)}"
    ]
    return "\n".join(env_lines)


def get_model_configuration():
    """Get model configuration from user input."""
    print("🤖 Custom Model Configuration")
    print("=" * 40)
    
    model_types = [
        "custom",
        "huggingface_inference", 
        "ollama",
        "cohere",
        "anthropic"
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
        print(f"\n📝 Configuring {model_type} model:")
        config["api_url"] = input("Enter API URL: ").strip()
        config["api_key"] = input("Enter API Key: ").strip()
        config["model_name"] = input("Enter Model Name (optional, default: my-model): ").strip() or "my-model"
    
    elif model_type == "huggingface_inference":
        print(f"\n📝 Configuring {model_type} model:")
        config["model_name"] = input("Enter Hugging Face model name (e.g., gpt2, microsoft/DialoGPT-medium): ").strip()
        config["api_token"] = input("Enter Hugging Face API token: ").strip()
    
    elif model_type == "ollama":
        print(f"\n📝 Configuring {model_type} model:")
        config["model_name"] = input("Enter Ollama model name (e.g., llama2, codellama): ").strip()
        config["api_url"] = input("Enter Ollama API URL (default: http://localhost:11434): ").strip() or "http://localhost:11434"
    
    elif model_type == "cohere":
        print(f"\n📝 Configuring {model_type} model:")
        config["api_key"] = input("Enter Cohere API key: ").strip()
        config["model"] = input("Enter Cohere model name (default: command): ").strip() or "command"
    
    elif model_type == "anthropic":
        print(f"\n📝 Configuring {model_type} model:")
        config["api_key"] = input("Enter Anthropic API key: ").strip()
        config["model"] = input("Enter Anthropic model name (default: claude-3-sonnet-20240229): ").strip() or "claude-3-sonnet-20240229"
    
    return model_type, config


def save_configuration(model_type: str, config: Dict[str, Any]):
    """Save configuration to files."""
    # Create .env configuration
    env_config = create_env_config(model_type, config)
    
    # Save to .env file
    with open(".env", "a") as f:
        f.write(f"\n{env_config}\n")
    
    # Save to config file
    config_data = {
        "model_type": model_type,
        "config": config,
        "env_config": env_config
    }
    
    with open("custom_model_config.json", "w") as f:
        json.dump(config_data, f, indent=2)
    
    print(f"✅ Configuration saved to .env and custom_model_config.json")


def create_api_test_script(model_type: str, config: Dict[str, Any]):
    """Create a test script for the configured model."""
    test_script = f"""#!/usr/bin/env python3
\"\"\"
API test script for {model_type} model.
\"\"\"

import asyncio
import json
import sys
sys.path.append('./backend')

from app.services.model_factory import ModelFactory
from app.core.config import settings

async def test_model():
    # Set up configuration
    settings.use_custom_model = True
    settings.custom_model_type = "{model_type}"
    settings.custom_model_config = {json.dumps(config)}
    
    # Create model
    model = ModelFactory.create_model()
    if not model:
        print("❌ Failed to create model")
        return
    
    # Test availability
    is_available = await model.is_available()
    print(f"Model available: {{is_available}}")
    
    if is_available:
        # Test generation
        prompt = "Write a short professional greeting."
        try:
            response = await model.generate_text(prompt)
            print(f"Generated: {{response[:100]}}...")
        except Exception as e:
            print(f"Generation failed: {{e}}")

if __name__ == "__main__":
    asyncio.run(test_model())
"""
    
    with open(f"test_{model_type}_api.py", "w") as f:
        f.write(test_script)
    
    print(f"✅ Test script created: test_{model_type}_api.py")


def main():
    """Main configuration function."""
    print("🔧 Custom Model Configuration Tool")
    print("=" * 40)
    
    # Get configuration
    model_type, config = get_model_configuration()
    
    print(f"\n📋 Configuration Summary:")
    print(f"Model Type: {model_type}")
    print(f"Configuration: {json.dumps(config, indent=2)}")
    
    # Confirm configuration
    confirm = input(f"\n✅ Save this configuration? (y/n): ").strip().lower()
    if confirm in ['y', 'yes']:
        save_configuration(model_type, config)
        create_api_test_script(model_type, config)
        
        print(f"\n🚀 Next Steps:")
        print(f"1. Restart your application to load the new configuration")
        print(f"2. Run the test script: python test_{model_type}_api.py")
        print(f"3. Test cover letter generation in the application")
        
        if model_type == "ollama":
            print(f"\n📝 For Ollama setup:")
            print(f"1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
            print(f"2. Pull model: ollama pull {config['model_name']}")
            print(f"3. Start Ollama: ollama serve")
        
        elif model_type == "huggingface_inference":
            print(f"\n📝 For Hugging Face setup:")
            print(f"1. Get API token from: https://huggingface.co/settings/tokens")
            print(f"2. Ensure model {config['model_name']} is available")
    
    else:
        print("❌ Configuration cancelled")


if __name__ == "__main__":
    main()
