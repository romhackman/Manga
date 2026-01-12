@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERREUR : python du venv introuvable
    pause
    exit /b
)

if not exist "Launcher\Launcher.py" (
    echo ERREUR : Launcher.py introuvable
    pause
    exit /b
)

".venv\Scripts\python.exe" "Launcher\Launcher.py"
