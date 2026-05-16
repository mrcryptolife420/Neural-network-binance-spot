@echo off
setlocal
cd /d "%~dp0"
set LIVE_TRADING_ENABLED=false
set KILL_SWITCH=true
set PYTHONPATH=%CD%\src
if exist ".venv\Scripts\python.exe" (
  set PYTHON_EXE=.venv\Scripts\python.exe
) else (
  set PYTHON_EXE=python
)
echo Starting Neural Binance Spot Dashboard V2...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-dashboard.ps1"
if errorlevel 1 (
  echo Failed to start Dashboard V2. Check data\logs and run AI Doctor export.
  pause
  exit /b 1
)
pause
