# Custom Model Quick Start Guide

This guide will help you quickly set up and use your own custom model for cover letter generation.

## 🚀 Quick Setup (5 minutes)

### Step 1: Run the Configuration Script

```bash
python configure_custom_model.py
```

This interactive script will:
- Ask you to select your model type
- Collect your API credentials
- Save the configuration to your `.env` file
- Create a test script for your model

### Step 2: Test Your Model

```bash
python test_custom_model.py
```

This will test your model's availability and text generation capabilities.

### Step 3: Restart Your Application

```bash
# If using Docker
docker-compose restart backend

# If running locally
cd backend
python -m uvicorn app.main:app --reload
```

## 📋 Supported Model Types

### 1. **Custom API** (Most Flexible)
```bash
# For any API that accepts text generation requests
Model Type: custom
API URL: https://your-api.com/generate
API Key: your-api-key
```

### 2. **Hugging Face Inference API**
```bash
# For Hugging Face hosted models
Model Type: huggingface_inference
Model Name: gpt2 (or any HF model)
API Token: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. **Ollama** (Local Models)
```bash
# For local models using Ollama
Model Type: ollama
Model Name: llama2 (or codellama, mistral, etc.)
API URL: http://localhost:11434
```

### 4. **Cohere**
```bash
# For Cohere's text generation models
Model Type: cohere
API Key: your-cohere-api-key
Model: command (or command-light)
```

### 5. **Anthropic Claude**
```bash
# For Claude models
Model Type: anthropic
API Key: sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Model: claude-3-sonnet-20240229
```

## 🔧 Manual Configuration

If you prefer to configure manually, add this to your `.env` file:

```bash
# Enable custom model
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=your_model_type

# Model-specific configuration
CUSTOM_MODEL_CONFIG={"api_key": "your-key", "model": "your-model"}
```

## 🧪 Testing Your Setup

### Test 1: Basic Functionality
```bash
python test_custom_model.py
```

### Test 2: API Integration
```bash
# Test the API endpoint
curl -X GET http://localhost:8000/api/v1/ai/available-models
```

### Test 3: Cover Letter Generation
Use the web interface to generate a cover letter - it should now use your custom model!

## 🐛 Troubleshooting

### Model Not Available
```bash
# Check if your model service is running
curl http://your-api-url/health

# Check API keys
echo $YOUR_API_KEY
```

### Poor Quality Output
- Adjust the prompt in `backend/app/services/custom_model_service.py`
- Try different model parameters (temperature, max_tokens)
- Consider using a different model

### API Errors
- Check your API endpoint and credentials
- Verify network connectivity
- Check API rate limits

## 📝 Example Configurations

### Example 1: Local Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Start Ollama
ollama serve

# Configure
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=ollama
CUSTOM_MODEL_CONFIG={"model_name": "llama2", "api_url": "http://localhost:11434"}
```

### Example 2: Hugging Face Setup
```bash
# Get API token from https://huggingface.co/settings/tokens

# Configure
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=huggingface_inference
CUSTOM_MODEL_CONFIG={"model_name": "gpt2", "api_token": "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
```

### Example 3: Custom API Setup
```bash
# Configure your own API
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=custom
CUSTOM_MODEL_CONFIG={"api_url": "https://your-api.com/generate", "api_key": "your-key", "model_name": "your-model"}
```

## 🔄 Switching Between Models

You can easily switch between models by updating your configuration:

```bash
# Switch to OpenAI (default)
USE_CUSTOM_MODEL=false

# Switch to Anthropic
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=anthropic
CUSTOM_MODEL_CONFIG={"api_key": "your-anthropic-key"}

# Switch to Ollama
USE_CUSTOM_MODEL=true
CUSTOM_MODEL_TYPE=ollama
CUSTOM_MODEL_CONFIG={"model_name": "llama2"}
```

## 📊 Monitoring

Check the application logs to see which model is being used:

```bash
# Docker logs
docker-compose logs backend

# Local logs
tail -f backend/app.log
```

You should see messages like:
```
🔍 Using custom model for cover letter generation
✅ Custom model generated successfully
```

## 🎯 Next Steps

1. **Optimize Prompts**: Customize the prompts in `custom_model_service.py`
2. **Add Caching**: Implement response caching for better performance
3. **Monitor Usage**: Track API calls and costs
4. **A/B Testing**: Compare different models for quality

## 🆘 Need Help?

1. Check the logs for error messages
2. Test your model independently first
3. Verify your API credentials and endpoints
4. Review the example implementations in `backend/app/services/my_custom_model.py`

Your custom model should now be working! 🎉
