#!/bin/bash

echo "🔑 Fixing OpenAI API Key Configuration"
echo "======================================"

# Check if we're in the right directory
if [ ! -f ".env" ]; then
    echo "❌ .env file not found in current directory"
    echo "   Please run this script from the project root directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Step 1: Check current .env file
echo "1️⃣ Checking current .env configuration..."
if grep -q "OPENAI_API_KEY=your-openai-api-key" .env; then
    echo "⚠️  Found placeholder API key in .env file"
    echo "   Current value: OPENAI_API_KEY=your-openai-api-key"
else
    echo "✅ .env file appears to be properly configured"
fi

echo ""

# Step 2: Show what needs to be changed
echo "2️⃣ Required changes:"
echo "   Replace: OPENAI_API_KEY=your-openai-api-key"
echo "   With:   OPENAI_API_KEY=YOUR_ACTUAL_API_KEY_HERE"
echo ""
echo "   ⚠️  IMPORTANT: Replace YOUR_ACTUAL_API_KEY_HERE with your real OpenAI API key"
echo "   🔗 Get your API key from: https://platform.openai.com/api-keys"

echo ""

# Step 3: Provide manual fix instructions
echo "3️⃣ Manual Fix Instructions:"
echo "   Please edit your .env file and update the OPENAI_API_KEY line:"
echo ""
echo "   📝 Edit .env file:"
echo "      nano .env"
echo "      # OR"
echo "      code .env"
echo "      # OR"
echo "      vim .env"
echo ""
echo "   🔄 Change this line:"
echo "      OPENAI_API_KEY=your-openai-api-key"
echo "   📝 To this:"
echo "      OPENAI_API_KEY=YOUR_ACTUAL_API_KEY_HERE"

echo ""

# Step 4: Verification
echo "4️⃣ After fixing, verify with:"
echo "   grep OPENAI_API_KEY .env"
echo "   # Should show your actual API key (not the placeholder)"

echo ""

# Step 5: Test the fix
echo "5️⃣ Test the fix:"
echo "   cd backend"
echo "   python test_openai_integration.py"

echo ""
echo "🔧 Quick Fix Commands:"
echo "   # Option 1: Manual edit"
echo "   nano .env"
echo ""
echo "   # Option 2: Verify the fix"
echo "   grep OPENAI_API_KEY .env"
echo ""
echo "   # Option 3: Test the configuration"
echo "   cd backend && python test_openai_integration.py"

echo ""
echo "⚠️  SECURITY REMINDER:"
echo "   - Never commit API keys to git"
echo "   - Use .env files for local development"
echo "   - Use environment variables in production"
echo "   - Keep your API keys secure and private"
