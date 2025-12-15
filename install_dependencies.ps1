# Chemin du projet
$PROJECT_FOLDER = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VENV_PATH = Join-Path $PROJECT_FOLDER ".venv"
$REQ_FILE = Join-Path $PROJECT_FOLDER "requirements.txt"

# Crée le .venv si inexistant
if (-Not (Test-Path $VENV_PATH)) {
    python -m venv $VENV_PATH
}

# Installer pip et dépendances
$PYTHON_EXE = Join-Path $VENV_PATH "Scripts\python.exe"
& $PYTHON_EXE -m pip install --upgrade pip setuptools wheel

if (Test-Path $REQ_FILE) {
    & $PYTHON_EXE -m pip install -r $REQ_FILE
    Write-Host "✅ Dépendances installées avec succès !"
} else {
    Write-Host "⚠ requirements.txt introuvable. Les dépendances n'ont pas été installées."
}

Write-Host "Installation terminée. Vous pouvez maintenant déplacer le dossier manuellement."
