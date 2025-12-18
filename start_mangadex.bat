@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERREUR : python du venv introuvable
    pause
    exit /b
)

if not exist "mangadex\main.py" (
    echo ERREUR : mangadex\gui_pyqt.py introuvable
    pause
    exit /b
)

".venv\Scripts\python.exe" "mangadex\main.py"
