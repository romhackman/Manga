#!/usr/bin/env python3
import os
import subprocess
import sys

# Chemin du projet et du script à lancer
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")
LAUNCHER_DIR = os.path.join(PROJECT_DIR, "Luncher")
LAUNCHER_FILE = os.path.join(LAUNCHER_DIR, "Luncher.py")
SHORTCUT_FILE = os.path.join(PROJECT_DIR, "launch.sh")

def create_venv():
    if not os.path.exists(VENV_DIR):
        print("Création de l'environnement virtuel...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("Environnement virtuel déjà présent.")

def install_dependencies():
    pip_executable = os.path.join(VENV_DIR, "bin", "pip")
    requirements_file = os.path.join(PROJECT_DIR, "requirements.txt")
    if os.path.exists(requirements_file):
        print("Installation des dépendances...")
        subprocess.run([pip_executable, "install", "-r", requirements_file])
    else:
        print("Pas de requirements.txt trouvé, skipping installation.")

def create_shortcut():
    if not os.path.exists(LAUNCHER_FILE):
        print(f"Erreur : {LAUNCHER_FILE} introuvable.")
        return

    content = f"""#!/usr/bin/env bash
# Script de lancement du Manga Downloader

source "{VENV_DIR}/bin/activate"
python3 "{LAUNCHER_FILE}" "$1"
"""

    with open(SHORTCUT_FILE, "w") as f:
        f.write(content)
    os.chmod(SHORTCUT_FILE, 0o755)
    print(f"Script de lancement créé : {SHORTCUT_FILE}")

if __name__ == "__main__":
    create_venv()
    install_dependencies()
    create_shortcut()
    print("Setup terminé ! Lance le programme avec : ./launch.sh [mangadex|animesama]")
