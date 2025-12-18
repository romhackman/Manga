@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERREUR : python du venv introuvable
    pause
    exit /b
)

if not exist "anime_sama\lecture.py" (
    echo ERREUR : anime_sama\lecture.py introuvable
    pause
    exit /b
)

".venv\Scripts\python.exe" "anime_sama\lecture.py"
