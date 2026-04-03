@echo off
echo ==========================================
echo Starting SynapseHR (Direct Native Mode)
echo ==========================================

cd Code

echo Launching FastAPI Backend...
cd backend
:: Open a new terminal window for the backend, install deps, and start the server
start "SynapseHR Backend" cmd /k "pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

echo Launching React Frontend...
cd frontend
:: Open a new terminal window for the frontend, install deps, and start Vite
start "SynapseHR Frontend" cmd /k "npm install && npm run dev"
cd ..

echo.
echo ==========================================
echo Native Launch Triggered!
echo.
echo Frontend (React): http://localhost:5173
echo Backend (FastAPI): http://localhost:8000
echo ==========================================
echo.
echo Waiting a few seconds for the servers to initialize...
timeout /t 5 /nobreak > NUL
start http://localhost:5173
