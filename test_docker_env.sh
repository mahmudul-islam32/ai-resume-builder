#!/bin/bash

echo "🐳 Testing Docker Environment Configuration"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found in current directory"
    echo "   Please run this script from the project root directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Step 1: Check .env file
echo "1️⃣ Checking .env file..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
    OPENAI_KEY=$(grep "OPENAI_API_KEY" .env | cut -d'=' -f2)
    if [ "$OPENAI_KEY" != "your-openai-api-key" ]; then
        echo "✅ OPENAI_API_KEY is configured (not placeholder)"
        echo "   Key preview: ${OPENAI_KEY:0:20}..."
    else
        echo "❌ OPENAI_API_KEY still has placeholder value"
    fi
else
    echo "❌ .env file not found"
fi

echo ""

# Step 2: Check Docker containers
echo "2️⃣ Checking Docker containers..."
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose found"
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Docker containers are running"
        
        # Check backend container environment
        echo "🔍 Checking backend container environment..."
        BACKEND_ENV=$(docker-compose exec -T backend env | grep OPENAI_API_KEY || echo "Not found")
        if [ "$BACKEND_ENV" != "Not found" ]; then
            echo "✅ OPENAI_API_KEY found in backend container"
            echo "   Value: ${BACKEND_ENV:0:30}..."
        else
            echo "❌ OPENAI_API_KEY not found in backend container"
        fi
    else
        echo "⚠️  Docker containers are not running"
        echo "   Start them with: docker-compose up -d"
    fi
else
    echo "❌ docker-compose not found"
fi

echo ""

# Step 3: Test environment variable loading
echo "3️⃣ Testing environment variable loading..."
if [ -f ".env" ]; then
    # Source the .env file and check the variable
    export $(cat .env | grep -v '^#' | xargs)
    if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your-openai-api-key" ]; then
        echo "✅ Environment variable loaded correctly"
        echo "   Key preview: ${OPENAI_API_KEY:0:20}..."
    else
        echo "❌ Environment variable not loaded correctly"
    fi
else
    echo "❌ Cannot test environment loading - .env file not found"
fi

echo ""

# Step 4: Docker restart instructions
echo "4️⃣ Docker Restart Instructions:"
echo "   Since you're using Docker, you need to restart containers after changing .env:"
echo ""
echo "   # Stop containers"
echo "   docker-compose down"
echo ""
echo "   # Start containers with new environment"
echo "   docker-compose up -d"
echo ""
echo "   # Check logs for any errors"
echo "   docker-compose logs backend"
echo ""

# Step 5: Quick fix commands
echo "5️⃣ Quick Fix Commands:"
echo "   # Option 1: Restart Docker containers"
echo "   docker-compose down && docker-compose up -d"
echo ""
echo "   # Option 2: Check backend logs"
echo "   docker-compose logs backend"
echo ""
echo "   # Option 3: Test API endpoint"
echo "   curl -X POST http://localhost:8000/ai/generate-customized-cover-letter \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"resume_content\":\"test\",\"job_description\":\"test\",\"company_name\":\"test\",\"job_title\":\"test\",\"applicant_name\":\"test\",\"customization\":{}}'"

echo ""
echo "🔧 Next Steps:"
echo "   1. Ensure your .env file has the correct OPENAI_API_KEY"
echo "   2. Restart Docker containers: docker-compose down && docker-compose up -d"
echo "   3. Check backend logs for any errors"
echo "   4. Test the cover letter generation feature"
