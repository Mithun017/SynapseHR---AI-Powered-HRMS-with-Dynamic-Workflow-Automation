@echo off
echo ==========================================
echo Starting SynapseHR Environment...
echo ==========================================

cd Code
echo Pulling down old containers...
docker-compose down

echo Building and starting the stack...
docker-compose up -d --build

echo.
echo ==========================================
echo System is booting!
echo.
echo Frontend (React): http://localhost:5173
echo Backend (FastAPI): http://localhost:8000
echo ==========================================
echo.
echo Waiting a few seconds for services to start...
timeout /t 5 /nobreak > NUL
start http://localhost:5173
pause
