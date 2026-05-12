@echo off
:: Claude Code + DeepSeek GUI Launcher
:: This file only launches the GUI. All setup is done inside the GUI.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

python -c "import yaml, requests, rich, click, openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    python -m pip install --quiet -r "%~dp0requirements.txt"
)

python "%~dp0launcher.py"
