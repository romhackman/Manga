@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERREUR : python du venv introuvable
    pause
    exit /b
)

if not exist "Luncher\Luncher.py" (
    echo ERREUR : Luncher.py introuvable
    pause
    exit /b
)

".venv\Scripts\python.exe" "Luncher\Luncher.py"
