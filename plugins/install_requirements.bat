@echo off
cd /d %~dp0

set VENV_PYTHON=..\..\.venv\Scripts\python.exe

if not exist "%VENV_PYTHON%" (
    echo ERREUR : .venv introuvable
    exit /b 1
)

if not exist requirements.txt (
    echo Aucun requirements.txt
    exit /b 0
)

"%VENV_PYTHON%" -m pip install -r requirements.txt
