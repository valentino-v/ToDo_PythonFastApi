#!/bin/bash

# 🚀 ToDo API Quick Start Script

echo "📋 ToDo API - FastAPI Quick Start"
echo "================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    echo ""
    echo "🚀 Starting ToDo API server..."
    echo "📍 API will be available at: http://localhost:8000"
    echo "📚 Interactive docs at: http://localhost:8000/docs"
    echo "📖 Alternative docs at: http://localhost:8000/redoc"
    echo ""
    echo "Press CTRL+C to stop the server"
    echo ""
    
    # Start the server
    python app.py
else
    echo "❌ Tests failed. Please check the errors above."
    exit 1
fi