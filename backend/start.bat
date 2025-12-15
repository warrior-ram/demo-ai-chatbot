@echo off
REM Startup script for the backend server (Windows)

echo ========================================
echo  AI Customer Support Chatbot Backend
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\installed
    echo Dependencies installed
    echo.
) else (
    echo Dependencies already installed
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo .env file not found. Creating from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your DEEPSEEK_API_KEY
    echo Get a free API key at: https://platform.deepseek.com
    echo.
    pause
    notepad .env
)

REM Check if database is seeded
if not exist "chatbot.db" (
    echo.
    set /p SEED="Database not found. Seed with sample data? (y/n): "
    if /i "%SEED%"=="y" (
        python seed_data.py
    )
)

echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
