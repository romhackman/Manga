import os
import sys
import requests
import tkinter as tk
from tkinter import messagebox
import subprocess

# ======================================================
# Dossier principal (où se trouve update.py)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================
# URL du fichier update.txt
# ======================================================
UPDATE_URL = "https://raw.githubusercontent.com/romhackman/Manga/main/update.txt"

# ======================================================
# Détecter le fichier de version locale
# ======================================================
LOCAL_VERSION_FILE = None
local_version = "V0"  # valeur par défaut si aucun fichier trouvé

for f in os.listdir(BASE_DIR):
    if f.upper().startswith("V") and f.lower().endswith(".manga"):
        LOCAL_VERSION_FILE = os.path.join(BASE_DIR, f)
        local_version = f.split(".")[0]  # "V2" depuis "V2.manga"
        break

# ======================================================
# Récupérer le contenu de update.txt
# ======================================================
try:
    response = requests.get(UPDATE_URL)
    response.raise_for_status()
except Exception as e:
    messagebox.showerror("Erreur", f"Impossible de récupérer update.txt :\n{e}")
    sys.exit(1)

lines = response.text.strip().splitlines()
if len(lines) < 3:
    messagebox.showerror("Erreur", "update.txt trop court !")
    sys.exit(1)

# ======================================================
# Lire la version et le statut
# ======================================================
# Ligne 1 : version
version_line = lines[0].strip()  # exemple : "update : V3"
if version_line.lower().startswith("update"):
    # Accepte "update : V3" ou "update: V3"
    parts = version_line.split(":", 1)
    if len(parts) < 2:
        messagebox.showerror("Erreur", f"Format de version invalide : {version_line}")
        sys.exit(1)
    remote_version = parts[1].strip()  # récupère "V3"
else:
    messagebox.showerror("Erreur", f"Format de version invalide : {version_line}")
    sys.exit(1)

# Vérifier que c’est bien "V" suivi d’un chiffre
if not remote_version.startswith("V") or not remote_version[1:].isdigit():
    messagebox.showerror("Erreur", f"Version invalide : {remote_version}")
    sys.exit(1)

# Ligne 2 : statut
status = lines[1].strip().lower()  # stable / instable / en test
STATUS_ICONS = {
    "stable": "stable 🟢",
    "instable": "instable ⚠️",
    "en test": "en test 🔴"
}
status_text = STATUS_ICONS.get(status, status)

# Les lignes suivantes sont les fichiers à télécharger
file_lines = lines[2:]

# ======================================================
# Comparer versions
# ======================================================
if remote_version > local_version:
    root = tk.Tk()
    root.withdraw()
    answer = messagebox.askyesno(
        "Mise à jour disponible",
        f"Une nouvelle version est disponible : {remote_version} ({status_text})\n"
        f"Votre version : {local_version}\n\n"
        "Voulez-vous mettre à jour maintenant ?"
    )
    if not answer:
        sys.exit(0)
else:
    print(f"Vous êtes déjà à jour ({local_version}). Statut : {status_text}")
    sys.exit(0)

# ======================================================
# Télécharger tous les fichiers listés
# ======================================================
for line in file_lines:
    if "|" not in line:
        continue
    file_url, target_path = [p.strip() for p in line.split("|", 1)]
    
    # Transformer l'URL github pour avoir le raw
    if "github.com" in file_url and "blob" in file_url:
        file_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    # Calculer chemin final
    if target_path.lower() == "racine":
        dest_dir = BASE_DIR
    else:
        # Supporter plusieurs niveaux : anime_sama > APP
        parts = [p.strip() for p in target_path.split(">")]
        dest_dir = os.path.join(BASE_DIR, *parts)

    os.makedirs(dest_dir, exist_ok=True)  # créer dossiers si nécessaire

    # Nom du fichier
    filename = os.path.basename(file_url)
    dest_file = os.path.join(dest_dir, filename)

    # Télécharger le fichier
    try:
        r = requests.get(file_url, stream=True)
        r.raise_for_status()
        with open(dest_file, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        print(f"{dest_file} téléchargé !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de télécharger {file_url} :\n{e}")

# ======================================================
# Mise à jour terminée
# ======================================================
# Renommer le fichier de version locale pour refléter la nouvelle version
new_version_file = os.path.join(BASE_DIR, remote_version + ".manga")
if LOCAL_VERSION_FILE:
    os.replace(LOCAL_VERSION_FILE, new_version_file)  # V2.manga → V3.manga
else:
    # Aucun fichier de version existant, créer le nouveau
    with open(new_version_file, "w") as f:
        f.write("")  # contenu vide

root = tk.Tk()
root.withdraw()
answer = messagebox.askyesno(
    "Mise à jour terminée",
    f"Mise à jour vers {remote_version} ({status_text}) terminée !\n"
    "Voulez-vous relancer le Launcher maintenant ?"
)

if answer:
    launcher_path = os.path.join(BASE_DIR, "Launcher", "Launcher.py")
    if os.path.exists(launcher_path):
        subprocess.Popen([sys.executable, launcher_path], cwd=os.path.dirname(launcher_path))
    else:
        messagebox.showerror("Erreur", f"Launcher introuvable : {launcher_path}")
