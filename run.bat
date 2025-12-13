@echo off
REM -------------------------------
REM Lancement automatique de lecture.py
REM -------------------------------

REM Récupère le chemin du script pour gérer les chemins relatifs
SET SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Vérifie si l'environnement virtuel existe
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo Erreur : environnement virtuel .venv non trouve !
    pause
    exit /b
)

REM Active l'environnement virtuel
call .venv\Scripts\activate.bat

REM Vérifie si lecture.py existe
IF NOT EXIST "lecture.py" (
    echo Erreur : lecture.py non trouve !
    pause
    deactivate
    exit /b
)

REM Lance lecture.py
python "lecture.py"

REM Désactive l'environnement virtuel
deactivate

echo -------------------------------
echo Programme termine !
pause
