import os
import subprocess
import sys

# Chemins
VENV_DIR = ".venv"
PYTHON_VENV = os.path.join(VENV_DIR, "Scripts", "python.exe")
PIP_VENV = os.path.join(VENV_DIR, "Scripts", "pip.exe")

def run(cmd):
    """Exécute une commande shell et arrête le script si erreur"""
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ ERREUR lors de l'exécution : {cmd}")
        sys.exit(1)

def update_python_tools():
    """Met à jour pip, setuptools et wheel du Python global"""
    print("🔄 Mise à jour de pip, setuptools et wheel global...")
    run(f'"{sys.executable}" -m pip install --upgrade pip setuptools wheel')

def create_venv():
    """Crée le venv si absent"""
    if not os.path.exists(PYTHON_VENV):
        print("📦 Création du venv...")
        run(f'"{sys.executable}" -m venv {VENV_DIR}')
    else:
        print("✅ Venv déjà existant")

def update_venv_tools():
    """Met à jour pip, setuptools et wheel dans le venv"""
    print("🔄 Mise à jour de pip, setuptools et wheel dans le venv...")
    run(f'"{PYTHON_VENV}" -m pip install --upgrade pip setuptools wheel')

def install_requirements():
    """Installe les packages depuis requirements.txt dans le venv"""
    print("📥 Installation des dépendances...")
    run(f'"{PIP_VENV}" install -r requirements.txt')

def test_imports():
    """Teste si tous les modules sont installés"""
    print("🔍 Vérification des modules...")
    modules = [
        "bs4", "certifi", "charset_normalizer", "fpdf",
        "idna", "pdf2image", "PIL", "fitz",
        "requests", "soupsieve", "typing_extensions",
        "urllib3", "wget"
    ]

    for module in modules:
        try:
            run(f'"{PYTHON_VENV}" -c "import {module}"')
            print(f"  ✔ {module}")
        except subprocess.CalledProcessError:
            print(f"  ❌ ERREUR module : {module}")
            return

    print("\n🎉 Tout est correctement installé !")

if __name__ == "__main__":
    print("🚀 Début du setup")
    
    # 1️⃣ Mise à jour Python global (optionnel mais recommandé)
    update_python_tools()
    
    # 2️⃣ Création du venv
    create_venv()
    
    # 3️⃣ Mise à jour pip dans le venv
    update_venv_tools()
    
    # 4️⃣ Installation des dépendances
    install_requirements()
    
    # 5️⃣ Test des modules installés
    test_imports()
    
    input("\nAppuie sur Entrée pour quitter...")
