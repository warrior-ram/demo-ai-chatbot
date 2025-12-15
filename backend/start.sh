#!/bin/bash
# Startup script for the backend server

echo "🚀 Starting AI Customer Support Chatbot Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed" ]; then
    echo "📚 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your DEEPSEEK_API_KEY"
    echo "   Get a free API key at: https://platform.deepseek.com"
    echo ""
    read -p "Press Enter to open .env file, or Ctrl+C to exit..."
    ${EDITOR:-nano} .env
fi

# Check if database is seeded
if [ ! -f "chatbot.db" ]; then
    echo ""
    echo "🌱 Database not found. Would you like to seed with sample data?"
    read -p "Seed database? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python seed_data.py
    fi
fi

echo ""
echo "🎯 Starting FastAPI server..."
echo "📡 Server will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
