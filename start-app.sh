#!/bin/bash

# Crucible Full-Stack Start Script
# This script starts both the Python FastAPI backend and the Next.js frontend.

# Get the absolute path of the project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🚀 Starting Crucible Agent Mesh..."

# 1. Start Backend
echo "📡 Starting Backend Server..."
cd "$PROJECT_DIR/backend"
source venv/bin/activate
# Run uvicorn in the background
# Using --reload for development
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# 2. Start Frontend
echo "💻 Starting Frontend App..."
cd "$PROJECT_DIR/frontend"
# Run npm dev in the background
npm run dev &
FRONTEND_PID=$!

echo "✅ Both servers are starting!"
echo "   - Backend: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers."

# Trap SIGINT (Ctrl+C) to kill both background processes
trap "echo '🛑 Stopping Crucible...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

# Wait for background processes
wait
