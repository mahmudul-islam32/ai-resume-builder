# Custom Model Integration Guide

This guide explains how to integrate your own AI model for cover letter generation in the AI Resume application.

## Overview

The application now supports multiple AI model providers for cover letter generation:
- **OpenAI** (default)
- **Anthropic Claude**
- **Hugging Face Models**
- **Local LLM Models** (Ollama, llama.cpp, etc.)
- **Custom Models**

## Quick Start

### 1. Environment Configuration

Add the following environment variables to your `.env` file:

```bash
# Enable custom model
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=anthropic  # or "huggingface", "local", "custom"

# Model-specific configuration
CUSTOM_MODEL_CONFIG={"api_key": "your-api-key", "model": "claude-3-sonnet-20240229"}
```

### 2. API Configuration

Use the API endpoints to configure your model:

```bash
# Get available models
GET /api/v1/ai/available-models

# Configure a model
POST /api/v1/ai/configure-model
{
  "model_type": "anthropic",
  "config": {
    "api_key": "your-api-key",
    "model": "claude-3-sonnet-20240229"
  }
}
```

## Model Types and Configuration

### 1. Anthropic Claude

```python
# Configuration
{
  "model_type": "anthropic",
  "config": {
    "api_key": "your-anthropic-api-key",
    "model": "claude-3-sonnet-20240229"
  }
}
```

**Requirements:**
```bash
pip install anthropic
```

### 2. Hugging Face Models

```python
# Configuration
{
  "model_type": "huggingface",
  "config": {
    "model_name": "gpt2",
    "api_token": "your-hf-token"  # Optional
  }
}
```

**Requirements:**
```bash
pip install transformers torch
```

### 3. Local LLM Models (Ollama)

```python
# Configuration
{
  "model_type": "local",
  "config": {
    "model_path": "llama2",
    "api_url": "http://localhost:11434"
  }
}
```

**Requirements:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Start Ollama service
ollama serve
```

### 4. Custom Models

For custom model implementations, create your own class:

```python
# backend/app/services/my_custom_model.py
from app.services.custom_model_service import CustomModelInterface

class MyCustomModel(CustomModelInterface):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    async def is_available(self) -> bool:
        # Check if your model service is available
        return True
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        # Implement your model's text generation
        import aiohttp
        
        payload = {
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 2000),
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/generate",
                json=payload,
                headers=headers
            ) as response:
                result = await response.json()
                return result["generated_text"]
```

Then update the ModelFactory:

```python
# In backend/app/services/model_factory.py
elif model_type == "custom":
    from app.services.my_custom_model import MyCustomModel
    return MyCustomModel(
        api_url=config.get("api_url"),
        api_key=config.get("api_key")
    )
```

## Implementation Details

### Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Service    │───▶│  Model Factory   │───▶│ Custom Models   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Cover Letter    │    │ Model Selection  │    │ Model Interface │
│ Generation      │    │ & Validation     │    │ Implementation  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Components

1. **CustomModelInterface**: Abstract base class for all model implementations
2. **CustomModelService**: Service layer that handles prompt building and model interaction
3. **ModelFactory**: Factory pattern for creating model instances
4. **AIService**: Main service that orchestrates model selection and fallback

### Prompt Engineering

The system uses carefully crafted prompts for cover letter generation:

```python
prompt = f"""
You are an expert cover letter writer. Create a compelling, personalized cover letter based on the following information:

APPLICANT NAME: {applicant_name}
JOB TITLE: {job_title}
COMPANY: {company_name}

RESUME CONTENT:
{resume_content}

JOB DESCRIPTION:
{job_description}

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
```

## Testing Your Model

### 1. Unit Tests

Create tests for your model implementation:

```python
# test_my_custom_model.py
import pytest
from app.services.my_custom_model import MyCustomModel

@pytest.mark.asyncio
async def test_my_custom_model():
    model = MyCustomModel("http://localhost:8000", "test-key")
    
    # Test availability
    assert await model.is_available() == True
    
    # Test text generation
    prompt = "Write a short cover letter for a software developer position."
    response = await model.generate_text(prompt)
    assert len(response) > 0
    assert "cover letter" in response.lower()
```

### 2. Integration Tests

Test the full integration:

```python
# test_custom_model_integration.py
import pytest
from app.services.ai_service import AIService

@pytest.mark.asyncio
async def test_custom_model_cover_letter():
    # Configure custom model
    settings.use_custom_model = True
    settings.custom_model_type = "custom"
    settings.custom_model_config = {
        "api_url": "http://localhost:8000",
        "api_key": "test-key"
    }
    
    ai_service = AIService()
    
    # Test cover letter generation
    cover_letter = await ai_service.generate_cover_letter(
        resume_content="Experienced software developer...",
        job_description="We are looking for a developer...",
        company_name="Tech Corp",
        job_title="Software Developer",
        applicant_name="John Doe"
    )
    
    assert len(cover_letter) > 0
    assert "Tech Corp" in cover_letter
```

## Performance Considerations

### 1. Response Time

- **Local Models**: May be slower but no API latency
- **Cloud APIs**: Faster but dependent on network
- **Custom Models**: Depends on your implementation

### 2. Cost Optimization

- Use appropriate model sizes for your use case
- Implement caching for repeated requests
- Consider batch processing for multiple cover letters

### 3. Error Handling

The system includes comprehensive error handling:

```python
try:
    response = await self.model.generate_text(prompt, **model_kwargs)
    return response.strip()
except Exception as e:
    # Log the error
    print(f"❌ Custom model error: {str(e)}")
    
    # Fallback to OpenAI or mock response
    if settings.openai_api_key:
        return await self._call_openai(prompt)
    else:
        return await self._mock_cover_letter_response(...)
```

## Security Considerations

### 1. API Key Management

- Store API keys securely in environment variables
- Use different keys for development and production
- Rotate keys regularly

### 2. Input Validation

- Validate all inputs before sending to your model
- Sanitize user-provided content
- Implement rate limiting

### 3. Output Validation

- Validate model outputs before returning to users
- Implement content filtering if necessary
- Log suspicious or inappropriate content

## Troubleshooting

### Common Issues

1. **Model Not Available**
   - Check if your model service is running
   - Verify API keys and endpoints
   - Check network connectivity

2. **Poor Quality Output**
   - Adjust prompt engineering
   - Tune model parameters (temperature, max_tokens)
   - Consider using a different model

3. **Performance Issues**
   - Implement caching
   - Use async/await properly
   - Consider model optimization

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Best Practices

1. **Start Simple**: Begin with a basic implementation and iterate
2. **Test Thoroughly**: Test with various inputs and edge cases
3. **Monitor Performance**: Track response times and error rates
4. **Document Changes**: Keep track of prompt and model changes
5. **Version Control**: Version your model configurations and prompts

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify your model configuration
3. Test your model independently
4. Review the example implementations

## Example Configurations

### Complete .env Example

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_resume

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Custom Model Configuration
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=anthropic
CUSTOM_MODEL_CONFIG={"api_key": "sk-ant-api03-...", "model": "claude-3-sonnet-20240229"}

# Fallback OpenAI (optional)
OPENAI_API_KEY=sk-...

# Development
DEVELOPMENT_MODE=true
COOKIE_SECURE=false
```

### Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - USE_CUSTOM_MODEL=true
      - CUSTOM_MODEL_TYPE=local
      - CUSTOM_MODEL_CONFIG={"model_path": "llama2", "api_url": "http://ollama:11434"}
    depends_on:
      - ollama
  
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
```

This guide should help you successfully integrate your own model for cover letter generation. Start with a simple implementation and gradually add more sophisticated features as needed.
