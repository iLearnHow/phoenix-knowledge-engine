#!/bin/bash

# Phoenix Knowledge Engine Development Server Startup Script

set -e

echo "🚀 Starting Phoenix Knowledge Engine development servers..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
echo "📦 Starting backend server..."
cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "📦 Starting frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Servers started!"
echo ""
echo "Access the application at:"
echo "- Frontend: http://localhost:3000"
echo "- API: http://localhost:8000"
echo "- Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for processes
wait
