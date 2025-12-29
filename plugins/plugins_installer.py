import os
import requests
import zipfile
import io
import subprocess
import sys
import json
import argparse

# ======================================================
# Dossiers et fichiers
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
JSON_FILE = os.path.join(PLUGINS_DIR, "instance_plugins.json")
TEMP_JSON = os.path.join(PLUGINS_DIR, "temp_link.json")
GLOBAL_REQUIREMENTS = os.path.join(BASE_DIR, "requirements.txt")

if not os.path.exists(PLUGINS_DIR):
    os.makedirs(PLUGINS_DIR)

PYTHON = sys.executable

# ======================================================
# Récupérer le lien depuis l'argument ou JSON temp
# ======================================================
parser = argparse.ArgumentParser()
parser.add_argument("--link", help="Lien GitHub du plugin")
args = parser.parse_args()

if args.link:
    lien = args.link.strip()
elif os.path.exists(TEMP_JSON):
    with open(TEMP_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        lien = data.get("link", "").strip()
else:
    print("Aucun lien fourni ni dans le JSON temp. Sortie.")
    exit()

if not lien:
    print("Lien vide. Sortie.")
    exit()

nom_plugin = lien.rstrip("/").split("/")[-1]
dossier_plugin_final = os.path.join(PLUGINS_DIR, nom_plugin)

if os.path.exists(dossier_plugin_final):
    print(f"Le plugin '{nom_plugin}' existe déjà.")
    if os.path.exists(TEMP_JSON):
        os.remove(TEMP_JSON)
    exit()

os.makedirs(dossier_plugin_final, exist_ok=True)

# ======================================================
# Téléchargement du ZIP
# ======================================================
repo_base = "/".join(lien.split("/")[:5])
zip_url = repo_base + "/archive/refs/heads/main.zip"
print(f"Téléchargement du plugin '{nom_plugin}' depuis {zip_url} ...")

try:
    r = requests.get(zip_url)
    r.raise_for_status()
except Exception as e:
    print("Erreur lors du téléchargement :", e)
    if os.path.exists(TEMP_JSON):
        os.remove(TEMP_JSON)
    exit()

# ======================================================
# Extraction du plugin
# ======================================================
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    zip_root = z.namelist()[0].split("/")[0]
    for file_info in z.infolist():
        if file_info.filename.startswith(f"{zip_root}/{nom_plugin}/"):
            relative_path = os.path.relpath(file_info.filename, f"{zip_root}/{nom_plugin}")
            final_path = os.path.join(dossier_plugin_final, relative_path)
            if file_info.is_dir():
                os.makedirs(final_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(final_path), exist_ok=True)
                with z.open(file_info) as source, open(final_path, "wb") as target:
                    target.write(source.read())

print(f"Plugin '{nom_plugin}' installé dans {dossier_plugin_final} !")

# ======================================================
# Installer les dépendances
# ======================================================
plugin_req_file = os.path.join(dossier_plugin_final, "requirements.txt")
global_modules = set()

if os.path.exists(GLOBAL_REQUIREMENTS):
    with open(GLOBAL_REQUIREMENTS, "r", encoding="utf-8") as f:
        global_modules = set(line.strip() for line in f if line.strip() and not line.startswith("#"))

if os.path.exists(plugin_req_file):
    with open(plugin_req_file, "r", encoding="utf-8") as f:
        plugin_modules = set(line.strip() for line in f if line.strip() and not line.startswith("#"))

    missing_modules = plugin_modules - global_modules
    for module in missing_modules:
        print(f"Installation du module {module} ...")
        subprocess.run([PYTHON, "-m", "pip", "install", module])
        global_modules.add(module)

    # Mettre à jour le requirements global
    with open(GLOBAL_REQUIREMENTS, "w", encoding="utf-8") as f:
        for module in sorted(global_modules):
            f.write(module + "\n")

    os.remove(plugin_req_file)

# ======================================================
# Mettre à jour le JSON instance_plugins
# ======================================================
instance_plugins = {}
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        instance_plugins = json.load(f)

main_py = os.path.join(dossier_plugin_final, f"{nom_plugin}.py")
if os.path.exists(main_py):
    instance_plugins[nom_plugin] = main_py
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(instance_plugins, f, indent=4)
    print(f"JSON mis à jour : '{nom_plugin}' -> '{main_py}'")
else:
    print(f"Aucun fichier principal '{nom_plugin}.py' trouvé.")

# ======================================================
# Supprimer le requirements global et le JSON temp
# ======================================================
if os.path.exists(GLOBAL_REQUIREMENTS):
    os.remove(GLOBAL_REQUIREMENTS)

if os.path.exists(TEMP_JSON):
    os.remove(TEMP_JSON)
    print("JSON temp supprimé.")
