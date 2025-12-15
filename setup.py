import os
import sys
import subprocess
import venv

VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"

def create_venv():
    if not os.path.exists(VENV_DIR):
        print("📦 Création de l'environnement virtuel (.venv)")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("✅ .venv déjà existant")

def install_requirements():
    if not os.path.exists(REQUIREMENTS_FILE):
        print("❌ requirements.txt introuvable")
        sys.exit(1)

    pip_path = (
        os.path.join(VENV_DIR, "Scripts", "pip.exe")
        if os.name == "nt"
        else os.path.join(VENV_DIR, "bin", "pip")
    )

    print("⬇️ Installation des dépendances")
    subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS_FILE])

def main():
    create_venv()
    install_requirements()
    print("🎉 Setup terminé avec succès")

if __name__ == "__main__":
    main()
