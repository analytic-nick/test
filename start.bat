@echo off
echo Starting Focus Group AI...
echo.
cd /d "%~dp0"

REM Check if .env files exist
if not exist backend\.env (
    echo Backend .env not found. Copying from .env.example...
    copy backend\.env.example backend\.env
    echo Please edit backend\.env and add your ANTHROPIC_API_KEY
    pause
    exit /b
)

if not exist frontend\.env.local (
    echo Frontend .env.local not found. Copying from .env.example...
    copy frontend\.env.example frontend\.env.local
)

REM Start backend
echo Starting backend on http://localhost:8000...
cd backend
start "Backend" cmd /k python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Wait a moment
timeout /t 3 /nobreak > nul

REM Start frontend
echo Starting frontend on http://localhost:3000...
cd ..\frontend
start "Frontend" cmd /k npm run dev

echo.
echo Focus Group AI is running!
echo.
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo.
echo Close the terminal windows to stop the servers
pause
