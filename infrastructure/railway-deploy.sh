#!/bin/bash

# Phoenix Knowledge Engine - Railway Deployment Script
# One-click deployment to Railway

set -e

echo "🚀 Deploying Phoenix Knowledge Engine to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    echo "   or visit: https://docs.railway.app/develop/cli"
    exit 1
fi

# Check if we're logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Please log in to Railway first:"
    railway login
fi

echo "📱 Creating Railway project..."

# Initialize Railway project
railway init

# Set environment variables
echo "🔧 Setting environment variables..."

# Get OpenAI API key
read -p "Enter your OpenAI API key: " openai_key
railway variables set OPENAI_API_KEY="$openai_key"

# Set other environment variables
railway variables set DJANGO_SETTINGS_MODULE="phoenix.settings"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="*"
railway variables set SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"

# Add PostgreSQL service
echo "🗄️  Adding PostgreSQL database..."
railway add postgresql

# Create railway.json
echo "📝 Creating railway.json..."
cat > railway.json << EOF
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:\$PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create nixpacks.toml
echo "📝 Creating nixpacks.toml..."
cat > nixpacks.toml << EOF
[phases.setup]
nixPkgs = ["python311", "pip"]

[phases.install]
cmds = ["cd backend && pip install -r requirements.txt"]

[phases.build]
cmds = ["cd backend && python manage.py collectstatic --noinput"]

[start]
cmd = "cd backend && python manage.py migrate && python manage.py runserver 0.0.0.0:\$PORT"
EOF

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

# Get the deployment URL
echo "🌐 Getting deployment URL..."
url=$(railway domain)

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app is live at: https://$url"
echo "📊 Monitor logs with: railway logs"
echo "🔧 Run commands with: railway run python backend/manage.py [command]"
echo ""
echo "🎉 Phoenix Knowledge Engine is now live on Railway!"
