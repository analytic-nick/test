#!/bin/bash

echo "🚀 Starting Focus Group AI..."
echo ""

# Check if .env files exist
if [ ! -f backend/.env ]; then
    echo "⚠️  Backend .env not found. Copying from .env.example..."
    cp backend/.env.example backend/.env
    echo "❗ Please edit backend/.env and add your ANTHROPIC_API_KEY"
    exit 1
fi

if [ ! -f frontend/.env.local ]; then
    echo "⚠️  Frontend .env.local not found. Copying from .env.example..."
    cp frontend/.env.example frontend/.env.local
fi

# Check for Python dependencies
echo "📦 Checking backend dependencies..."
cd backend
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
fi

# Check for Node dependencies
echo "📦 Checking frontend dependencies..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start backend in background
echo ""
echo "🔧 Starting backend on http://localhost:8000..."
cd ../backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready
sleep 3

# Start frontend
echo "🎨 Starting frontend on http://localhost:3000..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Focus Group AI is running!"
echo ""
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
