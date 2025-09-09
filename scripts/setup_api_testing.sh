#!/bin/bash

# Setup script for API testing
# Helps configure OpenAI API key and run tests

set -e

echo "🔧 Setting up Phoenix Knowledge Engine for API testing..."

# Check if we're in the right directory
if [ ! -f "backend/manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file from example..."
    cp backend/env.example backend/.env
fi

# Check if OpenAI API key is configured
API_KEY=$(grep "OPENAI_API_KEY=" backend/.env | cut -d'=' -f2)

if [ "$API_KEY" = "your_openai_api_key_here" ] || [ -z "$API_KEY" ]; then
    echo "🔑 OpenAI API key not configured!"
    echo ""
    echo "Please get your API key from: https://platform.openai.com/api-keys"
    echo "Then edit backend/.env and replace 'your_openai_api_key_here' with your actual key"
    echo ""
    echo "Example:"
    echo "OPENAI_API_KEY=sk-your-actual-key-here"
    echo ""
    read -p "Press Enter when you've updated the .env file..."
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source backend/venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Run database migrations
echo "🗄️  Running database migrations..."
cd backend
python manage.py migrate
cd ..

# Test the configuration
echo "🧪 Testing configuration..."
cd backend
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if api_key and api_key != 'your_openai_api_key_here':
    print('✅ OpenAI API key configured')
else:
    print('❌ OpenAI API key not configured')
    exit(1)
"
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Ready to test with real API calls!"
echo ""
echo "To run the tests:"
echo "  cd backend"
echo "  python test_real_api.py"
echo ""
echo "⚠️  WARNING: This will make real API calls and cost money!"
echo "   Estimated cost: $0.50 - $2.00 for full test suite"
echo ""
