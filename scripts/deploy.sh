#!/bin/bash

# Phoenix Knowledge Engine - Deployment Script
# Simplified deployment for MVP

set -e

echo "🚀 Deploying Phoenix Knowledge Engine MVP..."

# Check if we're in the right directory
if [ ! -f "backend/manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

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

# Check environment variables
echo "🔍 Checking environment variables..."
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from example..."
    cp backend/env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

# Run database migrations
echo "🗄️  Running database migrations..."
cd backend
python manage.py migrate
cd ..

# Collect static files
echo "📁 Collecting static files..."
cd backend
python manage.py collectstatic --noinput
cd ..

# Run tests
echo "🧪 Running tests..."
cd backend
python manage.py test tests.test_simplified_system --verbosity=2
cd ..

echo "✅ Deployment preparation complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit backend/.env with your OpenAI API key"
echo "2. Start the backend: cd backend && python manage.py runserver"
echo "3. Start the frontend: cd frontend && npm start"
echo "4. Visit http://localhost:3000 to test the application"
echo ""
echo "📊 Monitor costs with: python backend/budget_monitor.py"
echo "🔧 Run tests with: python backend/manage.py test"
echo ""
echo "🚀 Phoenix Knowledge Engine MVP is ready!"
