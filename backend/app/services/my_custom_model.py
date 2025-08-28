from typing import Optional
import aiohttp
import json
import asyncio
from app.services.custom_model_service import CustomModelInterface


class MyCustomModel(CustomModelInterface):
    """
    Example custom model implementation.
    
    This is a template for creating your own model integration.
    Replace the implementation with your actual model's API calls.
    """
    
    def __init__(self, api_url: str, api_key: str, model_name: str = "my-model"):
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self._session = None
    
    async def is_available(self) -> bool:
        """Check if your model service is available."""
        try:
            # Test the connection to your model service
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/health",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
        except Exception as e:
            print(f"❌ Model availability check failed: {str(e)}")
            return False
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using your custom model.
        
        Args:
            prompt: The input prompt for text generation
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
            
        Returns:
            Generated text from your model
        """
        try:
            # Prepare the request payload for your model
            payload = {
                "prompt": prompt,
                "max_tokens": kwargs.get("max_tokens", 2000),
                "temperature": kwargs.get("temperature", 0.7),
                "model": self.model_name,
                # Add any other parameters your model expects
                "stream": False
            }
            
            # Set up headers (adjust based on your API requirements)
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make the API call to your model
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/generate",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Extract the generated text from your model's response
                        # Adjust this based on your model's response format
                        generated_text = result.get("generated_text", "")
                        
                        if not generated_text:
                            # Try alternative response formats
                            generated_text = result.get("text", "")
                            generated_text = result.get("content", "")
                            generated_text = result.get("response", "")
                        
                        if not generated_text:
                            raise Exception("No generated text found in model response")
                        
                        return generated_text
                    else:
                        error_text = await response.text()
                        raise Exception(f"Model API error: {response.status} - {error_text}")
                        
        except asyncio.TimeoutError:
            raise Exception("Model request timed out")
        except Exception as e:
            raise Exception(f"Custom model error: {str(e)}")
    
    async def close(self):
        """Clean up resources if needed."""
        if self._session:
            await self._session.close()


# Example implementations for different model types

class HuggingFaceInferenceModel(CustomModelInterface):
    """Example implementation for Hugging Face Inference API."""
    
    def __init__(self, model_name: str, api_token: str):
        self.model_name = model_name
        self.api_token = api_token
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    
    async def is_available(self) -> bool:
        """Check if the Hugging Face model is available."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except Exception:
            return False
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Hugging Face Inference API."""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": kwargs.get("max_tokens", 500),
                    "temperature": kwargs.get("temperature", 0.7),
                    "do_sample": True
                }
            }
            
            headers = {"Authorization": f"Bearer {self.api_token}"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Handle different response formats
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get("generated_text", "")
                        elif isinstance(result, dict):
                            return result.get("generated_text", "")
                        else:
                            return str(result)
                    else:
                        error_text = await response.text()
                        raise Exception(f"Hugging Face API error: {response.status} - {error_text}")
                        
        except Exception as e:
            raise Exception(f"Hugging Face model error: {str(e)}")


class OllamaModel(CustomModelInterface):
    """Example implementation for Ollama local models."""
    
    def __init__(self, model_name: str, api_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.api_url = api_url
    
    async def is_available(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Check if Ollama is running and get available models
                async with session.get(f"{self.api_url}/api/tags") as response:
                    if response.status != 200:
                        return False
                
                # Check if the specific model is available
                models_response = await response.json()
                available_models = [model["name"] for model in models_response.get("models", [])]
                
                # Check if our model is available (with or without :latest suffix)
                model_found = any(
                    model_name.startswith(self.model_name) 
                    for model_name in available_models
                )
                
                return model_found
                
        except Exception as e:
            print(f"❌ Ollama availability check failed: {str(e)}")
            return False
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Ollama."""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 2000)
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error: {response.status} - {error_text}")
                        
        except Exception as e:
            raise Exception(f"Ollama model error: {str(e)}")


class CohereModel(CustomModelInterface):
    """Example implementation for Cohere models."""
    
    def __init__(self, api_key: str, model: str = "command"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.cohere.ai/v1/generate"
    
    async def is_available(self) -> bool:
        """Check if Cohere API is available."""
        return bool(self.api_key)
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Cohere API."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": kwargs.get("max_tokens", 2000),
                "temperature": kwargs.get("temperature", 0.7),
                "k": 0,
                "stop_sequences": [],
                "return_likelihoods": "NONE"
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        generations = result.get("generations", [])
                        if generations:
                            return generations[0].get("text", "")
                        else:
                            raise Exception("No generation found in response")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Cohere API error: {response.status} - {error_text}")
                        
        except Exception as e:
            raise Exception(f"Cohere model error: {str(e)}")
