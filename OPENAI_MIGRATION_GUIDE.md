# OpenAI API Migration Guide

This guide helps you migrate from the old OpenAI API syntax to the new 1.0.0+ syntax.

## What Changed

The OpenAI Python library was updated from version 0.x to 1.x, which introduced breaking changes in the API syntax.

### Old Syntax (0.x)
```python
import openai

# Set API key globally
openai.api_key = "your-api-key"

# Create completion
response = await openai.ChatCompletion.acreate(
    model="gpt-3.5-turbo",
    messages=[...],
    temperature=0.7
)
```

### New Syntax (1.x)
```python
from openai import AsyncOpenAI

# Create client instance
client = AsyncOpenAI(api_key="your-api-key")

# Create completion
response = await client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[...],
    temperature=0.7
)
```

## Migration Steps

### 1. Update Dependencies
```bash
# Update to latest OpenAI version
pip install --upgrade openai

# Or install specific version
pip install openai>=1.0.0
```

### 2. Update Your Code

#### Before (Old Syntax)
```python
import openai

class AIService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
    
    async def generate_text(self, prompt):
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

#### After (New Syntax)
```python
from openai import AsyncOpenAI

class AIService:
    def __init__(self):
        # No need to set API key globally
        pass
    
    async def generate_text(self, prompt):
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### 3. Key Changes

| Old (0.x) | New (1.x) | Notes |
|------------|-----------|-------|
| `openai.ChatCompletion.acreate()` | `client.chat.completions.create()` | Method name changed |
| `openai.api_key = "key"` | `client = AsyncOpenAI(api_key="key")` | API key now per-client |
| `model="gpt-3.5-turbo"` | `model="gpt-3.5-turbo-0125"` | Model names updated |
| Global configuration | Per-client configuration | More flexible |

## Testing Your Migration

### 1. Run the Test Script
```bash
cd backend
python test_openai_integration.py
```

### 2. Check for Common Issues
- **Import errors**: Ensure `openai>=1.0.0` is installed
- **API key errors**: Verify API key is passed to client constructor
- **Model errors**: Use updated model names
- **Method errors**: Use new method names

### 3. Verify Functionality
- Test basic API calls
- Test your AI service methods
- Check error handling

## Environment Setup

### 1. Check Your .env File
```bash
# Ensure this is set
OPENAI_API_KEY=your-actual-api-key-here
```

### 2. Verify Installation
```bash
# Check OpenAI version
pip show openai

# Should show version >= 1.0.0
```

### 3. Test API Key
```bash
# Test with curl (replace with your key)
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.openai.com/v1/models
```

## Troubleshooting

### Common Errors

#### 1. "You tried to access openai.ChatCompletion"
**Solution**: Update to new syntax using `client.chat.completions.create()`

#### 2. "OpenAI API key not configured"
**Solution**: Check your `.env` file and ensure `OPENAI_API_KEY` is set

#### 3. "ImportError: cannot import name 'ChatCompletion'"
**Solution**: Update to new import: `from openai import AsyncOpenAI`

#### 4. "Model not found"
**Solution**: Use updated model names like `gpt-3.5-turbo-0125`

### Debug Steps

1. **Check OpenAI version**:
   ```bash
   pip show openai
   ```

2. **Verify API key**:
   ```bash
   echo $OPENAI_API_KEY
   ```

3. **Test basic connection**:
   ```bash
   python test_openai_integration.py
   ```

4. **Check error logs**:
   Look for specific error messages in your application logs

## Benefits of New API

### 1. Better Performance
- Improved async support
- Better connection pooling
- Optimized request handling

### 2. More Flexible
- Per-client configuration
- Better error handling
- More configuration options

### 3. Future-Proof
- Latest features and models
- Better security
- Ongoing improvements

## Additional Resources

- [OpenAI Python Library Documentation](https://github.com/openai/openai-python)
- [Migration Guide](https://github.com/openai/openai-python/discussions/742)
- [API Reference](https://platform.openai.com/docs/api-reference)
- [Model Updates](https://platform.openai.com/docs/models)

## Support

If you encounter issues after migration:

1. Check this guide for common solutions
2. Run the test script to isolate issues
3. Check OpenAI's official migration guide
4. Verify your API key and credits
5. Check network connectivity

## Quick Fix Summary

```bash
# 1. Update OpenAI library
pip install --upgrade openai

# 2. Update your code to use new syntax
# 3. Test with the provided test script
python test_openai_integration.py

# 4. Restart your application
```

The migration should resolve the "You tried to access openai.ChatCompletion" error and provide you with a more robust and future-proof OpenAI integration.
