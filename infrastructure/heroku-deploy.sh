#!/bin/bash

# Phoenix Knowledge Engine - Heroku Deployment Script
# One-click deployment to Heroku

set -e

echo "🚀 Deploying Phoenix Knowledge Engine to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if we're logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please log in to Heroku first:"
    heroku login
fi

# Get app name
read -p "Enter your Heroku app name (or press Enter for 'phoenix-knowledge-engine'): " app_name
app_name=${app_name:-phoenix-knowledge-engine}

echo "📱 Creating Heroku app: $app_name"

# Create Heroku app
heroku create $app_name --region us

# Set environment variables
echo "🔧 Setting environment variables..."

# Get OpenAI API key
read -p "Enter your OpenAI API key: " openai_key
heroku config:set OPENAI_API_KEY="$openai_key" --app $app_name

# Set other environment variables
heroku config:set DJANGO_SETTINGS_MODULE="phoenix.settings" --app $app_name
heroku config:set DEBUG="False" --app $app_name
heroku config:set ALLOWED_HOSTS="*" --app $app_name
heroku config:set SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" --app $app_name

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini --app $app_name

# Create Procfile
echo "📝 Creating Procfile..."
cat > Procfile << EOF
web: cd backend && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:\$PORT
EOF

# Create runtime.txt
echo "🐍 Setting Python version..."
echo "python-3.11.0" > runtime.txt

# Create requirements.txt for Heroku
echo "📦 Creating Heroku requirements.txt..."
cat > requirements.txt << EOF
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
openai==1.3.0
python-dotenv==1.0.0
psycopg2-binary==2.9.7
gunicorn==21.2.0
whitenoise==6.6.0
celery==5.3.4
redis==5.0.1
EOF

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy Phoenix Knowledge Engine to Heroku" || true
git push heroku main

# Run migrations
echo "🗄️  Running database migrations..."
heroku run python backend/manage.py migrate --app $app_name

# Open the app
echo "🌐 Opening your app..."
heroku open --app $app_name

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app is live at: https://$app_name.herokuapp.com"
echo "📊 Monitor logs with: heroku logs --tail --app $app_name"
echo "🔧 Run commands with: heroku run python backend/manage.py [command] --app $app_name"
echo ""
echo "🎉 Phoenix Knowledge Engine is now live on Heroku!"
