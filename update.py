import os
import sys
import requests
import subprocess
import shutil
import re
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# ======================================================
# LOG
# ======================================================
def log(msg):
    print(f"[UPDATE] {msg}", flush=True)

log("Démarrage du programme de mise à jour")

# ======================================================
# BASE DIR
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log(f"Dossier de base : {BASE_DIR}")

# ======================================================
# VERSION LOCALE
# ======================================================
local_major = 0
local_micro = 0
LOCAL_VERSION_FILE = None

log("Recherche version locale...")
for f in os.listdir(BASE_DIR):
    if f.upper().startswith("V") and f.lower().endswith(".manga"):
        LOCAL_VERSION_FILE = os.path.join(BASE_DIR, f)
        try:
            version_str = f[1:-6]  # retire le V et .manga
            if "." in version_str:
                local_major, local_micro = map(int, version_str.split("."))
            else:
                local_major = int(version_str)
                local_micro = 0
            log(f"Version locale : V{local_major}.{local_micro}")
        except Exception as e:
            log(f"Erreur version locale : {e}")
        break

# ======================================================
# UPDATE.TXT
# ======================================================
UPDATE_URL = "https://raw.githubusercontent.com/romhackman/Manga/main/update.txt"
log("Téléchargement update.txt")
try:
    response = requests.get(UPDATE_URL, timeout=10)
    response.raise_for_status()
except Exception as e:
    log(f"Erreur réseau : {e}")
    sys.exit(0)

lines = response.content.decode("utf-8", errors="ignore").replace("\ufeff", "")
lines = [l.strip() for l in lines.splitlines() if l.strip()]

# ======================================================
# VERSION DISTANTE
# ======================================================
try:
    version_part = lines[0].split(":")[1].strip().lstrip("Vv")
    if "." in version_part:
        remote_major, remote_micro = map(int, version_part.split("."))
    else:
        remote_major = int(version_part)
        remote_micro = 0
    log(f"Version distante : V{remote_major}.{remote_micro}")
except Exception as e:
    log(f"Erreur version distante : {e}")
    sys.exit(0)

# ======================================================
# COMPARAISON
# ======================================================
if (remote_major, remote_micro) <= (local_major, local_micro):
    log("Tout est à jour → arrêt")
    sys.exit(0)

log("Mise à jour DISPONIBLE")

# ======================================================
# STATUT
# ======================================================
raw_status = lines[1] if len(lines) > 1 else "inconnu"
clean_status = re.sub(r"[^a-zA-Z]", "", raw_status).lower()

STATUS = {
    "stable": "stable 🟢",
    "instable": "instable ⚠️",
    "test": "en test 🔴"
}
status_text = STATUS.get(clean_status, "statut inconnu ❓")
log(f"Statut : {status_text}")

# ======================================================
# PARSING DEL ET TELECHARGEMENT
# ======================================================
delete_files = []
download_files_list = []

i = 2
if i < len(lines) and lines[i].lower().startswith("del"):
    log("Zone de suppression détectée")
    i += 1
    while i < len(lines) and lines[i].strip() != "---":
        delete_files.append(lines[i].strip())
        log(f"À supprimer : {lines[i].strip()}")
        i += 1
    i += 1  # saute le ---

download_files_list = lines[i:]
log(f"{len(download_files_list)} fichier(s) à télécharger")

# ======================================================
# Fonction pour résoudre les chemins
# ======================================================
def resolve_path(relative_path):
    parts = [p.strip() for p in relative_path.split(">")]
    return os.path.join(BASE_DIR, *parts)

# ======================================================
# UI
# ======================================================
IMAGE_PATH = os.path.join(BASE_DIR, "programme", "update", "image.png")
LOGO_PATH = os.path.join(BASE_DIR, "programme", "update", "logo.png")

BG_COLOR = "#e0f2f1"
FG_COLOR = "#004d40"
BUTTON_COLOR = "#26a69a"
BUTTON_HOVER = "#00796b"
TEXT_COLOR = "#ffffff"

root = tk.Tk()
root.title("Mise à jour Manga")
root.geometry("700x400")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

if os.path.exists(LOGO_PATH):
    root.iconphoto(True, tk.PhotoImage(file=LOGO_PATH))

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame, bg=BG_COLOR)
left_frame.pack(side="left", fill="y", expand=True, padx=(0, 10))

def fmt(ma, mi):
    return f"V{ma}.{mi}" if mi else f"V{ma}"

tk.Label(
    left_frame,
    text=f"Version locale : {fmt(local_major, local_micro)}\n"
         f"Version distante : {fmt(remote_major, remote_micro)}\n"
         f"Statut : {status_text}",
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=FG_COLOR,
    justify="left"
).pack(pady=20)

progress = ttk.Progressbar(left_frame, length=300)
progress.pack(pady=10)

# ======================================================
# UPDATE PROCESS
# ======================================================
def run_update():
    log("Début mise à jour")

    # ======= SUPPRESSION =======
    log("Début suppression des fichiers et dossiers")
    for relative_path in delete_files:
        full_path = resolve_path(relative_path)
        log(f"Suppression demandée : {full_path}")

        if os.path.exists(full_path):
            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    log(f"✔ Fichier supprimé : {full_path}")
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    log(f"✔ Dossier supprimé : {full_path}")
                else:
                    log(f"⚠️ Type inconnu (ni fichier ni dossier) : {full_path}")
            except Exception as e:
                log(f"❌ Erreur lors de la suppression de {full_path} : {e}")
        else:
            log(f"⚠️ Introuvable : {full_path}")

    # ======= TELECHARGEMENT =======
    for line in download_files_list:
        if "|" not in line:
            continue

        file_url, target_path = [p.strip() for p in line.split("|", 1)]
        if "github.com" in file_url and "blob" in file_url:
            file_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        dest_dir = BASE_DIR if target_path.lower() == "racine" else os.path.join(
            BASE_DIR, *[p.strip() for p in target_path.split(">")]
        )
        os.makedirs(dest_dir, exist_ok=True)

        dest_file = os.path.join(dest_dir, os.path.basename(file_url))
        log(f"Téléchargement : {dest_file}")

        r = requests.get(file_url, stream=True)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done = 0

        with open(dest_file, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
                done += len(chunk)
                if total > 0:
                    progress["value"] = done / total * 100
                    root.update_idletasks()

    # ======= VERSION =======
    new_file = os.path.join(BASE_DIR, f"V{remote_major}.{remote_micro}.manga")
    if LOCAL_VERSION_FILE:
        os.replace(LOCAL_VERSION_FILE, new_file)
    else:
        open(new_file, "w").close()

    log("Mise à jour terminée")
    messagebox.showinfo("Succès", "Mise à jour terminée")
    relancer_launcher()

def relancer_launcher():
    launcher = os.path.join(BASE_DIR, "Launcher", "Launcher.py")
    if os.path.exists(launcher):
        if messagebox.askyesno("Relancer", "Relancer le Launcher ?"):
            subprocess.Popen([sys.executable, launcher], cwd=os.path.dirname(launcher))
            root.destroy()

btns = tk.Frame(left_frame, bg=BG_COLOR)
btns.pack(pady=20)

tk.Button(btns, text="Mettre à jour", bg=BUTTON_COLOR, fg=TEXT_COLOR,
          activebackground=BUTTON_HOVER, font=("Arial", 12, "bold"),
          command=run_update).pack(side="left", padx=10)

tk.Button(btns, text="Fermer", bg=BUTTON_COLOR, fg=TEXT_COLOR,
          activebackground=BUTTON_HOVER, font=("Arial", 12, "bold"),
          command=root.destroy).pack(side="right", padx=10)

right_frame = tk.Frame(main_frame, bg=BG_COLOR)
right_frame.pack(side="right", fill="both", expand=True)

if os.path.exists(IMAGE_PATH):
    img = Image.open(IMAGE_PATH).resize((250, 350))
    img_tk = ImageTk.PhotoImage(img)
    tk.Label(right_frame, image=img_tk, bg=BG_COLOR).pack(expand=True)

log("Interface affichée")
root.mainloop()
log("Programme terminé")
