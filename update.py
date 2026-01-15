import requests
import os
from urllib.parse import urlparse
import tkinter as tk
from tkinter import messagebox
import re  # pour extraire la version

# ---- Config ----
version_file_prefix = "V"
version_file_suffix = ".manga"
update_txt_url = "https://raw.githubusercontent.com/romhackman/Manga/main/update.txt"
root_folder = os.getcwd()  # dossier où se trouve le script

# ---- Fonction pour lire la version locale ----
def get_local_version():
    for file in os.listdir(root_folder):
        if file.startswith(version_file_prefix) and file.endswith(version_file_suffix):
            try:
                return int(file[len(version_file_prefix):-len(version_file_suffix)])
            except:
                pass
    return 0  # pas de version locale

# ---- Fonction pour créer le lien raw ----
def github_raw_url(link):
    parsed = urlparse(link.strip())
    path_parts = parsed.path.split('/')
    if "blob" in path_parts:
        path_parts.pop(path_parts.index("blob"))
    return f"https://raw.githubusercontent.com{'/'.join(path_parts)}"

# ---- Récupérer update.txt ----
response = requests.get(update_txt_url)
if response.status_code != 200:
    print(f"Erreur lors de la récupération de update.txt : {response.status_code}")
    exit()

lines = response.text.splitlines()
if not lines:
    print("update.txt vide")
    exit()

# ---- Extraire la version distante depuis la première ligne ----
first_line = lines[0]
match = re.search(r'V(\d+)', first_line, re.IGNORECASE)
if not match:
    print("Impossible de trouver la version dans update.txt")
    exit()

remote_version = int(match.group(1))
local_version = get_local_version()

print(f"Version locale : V{local_version}")
print(f"Version distante : V{remote_version}")

if remote_version <= local_version:
    print("Vous êtes déjà à jour.")
    exit()

# ---- Pop-up pour proposer la mise à jour ----
root = tk.Tk()
root.withdraw()  # cacher la fenêtre principale
root.attributes("-topmost", True)  # mettre la pop-up au premier plan

update_choice = messagebox.askyesno(
    "Mise à jour disponible",
    f"Une nouvelle version est disponible (V{remote_version}).\nVoulez-vous mettre à jour ?"
)
root.destroy()  # fermer la fenêtre Tkinter principale après la pop-up

if not update_choice:
    print("Mise à jour annulée.")
    exit()

# ---- Télécharger les fichiers ----
for line in lines[1:]:
    line = line.strip()
    if not line or line.startswith("#"):
        continue

    # Séparer le lien et le chemin cible
    if "|" not in line:
        print(f"Ligne invalide (pas de '|') : {line}")
        continue
    link, target_folder = map(str.strip, line.split("|", 1))

    # Chemin complet
    if target_folder.lower() == "racine":
        full_folder_path = root_folder
    else:
        target_folder = target_folder.replace(">", os.sep).replace(" ", "")
        full_folder_path = os.path.join(root_folder, target_folder)
        os.makedirs(full_folder_path, exist_ok=True)

    filename = os.path.basename(urlparse(link).path)
    local_path = os.path.join(full_folder_path, filename)

    # Supprimer l’ancien fichier
    if os.path.exists(local_path):
        os.remove(local_path)
        print(f"Ancien fichier supprimé : {local_path}")

    raw_link = github_raw_url(link)

    print(f"Téléchargement de {raw_link} -> {local_path}")
    try:
        r = requests.get(raw_link, stream=True)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{filename} téléchargé avec succès.\n")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {link}: {e}\n")

# ---- Mettre à jour le fichier de version ----
# Supprimer l’ancien fichier de version
for file in os.listdir(root_folder):
    if file.startswith(version_file_prefix) and file.endswith(version_file_suffix):
        os.remove(os.path.join(root_folder, file))
# Créer le nouveau fichier de version
new_version_file = f"{version_file_prefix}{remote_version}{version_file_suffix}"
open(os.path.join(root_folder, new_version_file), "w").close()
print(f"Mise à jour terminée. Nouvelle version : V{remote_version}")
