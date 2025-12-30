@echo off
cd /d "%~dp0"

echo ===============================
echo Installation du programme
echo ===============================
echo.

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR : Python n'est pas installe ou pas dans le PATH
    echo Telecharge-le sur https://www.python.org
    pause
    exit /b
)

:: Vérifier que setup.py existe
if not exist "setup.py" (
    echo ERREUR : setup.py introuvable
    pause
    exit /b
)

:: Lancer le setup
echo Lancement de setup_win.py...
python setup_win.py

echo.
echo Installation terminee.
pause


