import os
import sys
import requests
import subprocess

# ======================================================
# Dossier principal
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================
# Détecter la version locale
# ======================================================
local_version = 0
LOCAL_VERSION_FILE = None
for f in os.listdir(BASE_DIR):
    if f.upper().startswith("V") and f.lower().endswith(".manga"):
        LOCAL_VERSION_FILE = os.path.join(BASE_DIR, f)
        try:
            local_version = int(f[1:].split(".")[0])  # V1.manga → 1
        except:
            local_version = 0
        break

# ======================================================
# Récupérer update.txt
# ======================================================
UPDATE_URL = "https://raw.githubusercontent.com/romhackman/Manga/main/update.txt"

try:
    response = requests.get(UPDATE_URL)
    response.raise_for_status()
except Exception:
    sys.exit(0)  # pas de update.txt → quitter silencieusement

lines = response.text.strip().splitlines()
if len(lines) < 1:
    sys.exit(0)

# ======================================================
# Version distante
# ======================================================
version_line = lines[0].strip()
if version_line.lower().startswith("update"):
    try:
        remote_version = int(version_line.split(":")[1].strip()[1:])  # Update:V2 → 2
    except:
        remote_version = 0
else:
    sys.exit(0)

# ======================================================
# Vérifier si update nécessaire
# ======================================================
if remote_version <= local_version:
    # Déjà à jour → quitte immédiatement, aucune fenêtre
    sys.exit(0)

# ======================================================
# Ici seulement : importer Tkinter et PIL si update nécessaire
# ======================================================
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# ======================================================
# Chemins images (adapter selon ton arborescence)
# ======================================================
IMAGE_PATH = os.path.join(BASE_DIR, "programme", "update", "image.png")
LOGO_PATH = os.path.join(BASE_DIR, "programme", "update", "logo.png")

# ======================================================
# Couleurs thème
# ======================================================
BG_COLOR = "#e0f2f1"
FG_COLOR = "#004d40"
BUTTON_COLOR = "#26a69a"
BUTTON_HOVER = "#00796b"
TEXT_COLOR = "#ffffff"

# ======================================================
# Statut update
# ======================================================
status = lines[1].strip().lower() if len(lines) > 1 else "stable"
STATUS_ICONS = {"stable": "stable 🟢", "instable": "instable ⚠️", "en test": "en test 🔴"}
status_text = STATUS_ICONS.get(status, status)
file_lines = lines[2:]  # fichiers à télécharger

# ======================================================
# Fenêtre principale
# ======================================================
root = tk.Tk()
root.title("Mise à jour Manga")
root.geometry("700x400")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Logo comme icône
if os.path.exists(LOGO_PATH):
    root.iconphoto(True, tk.PhotoImage(file=LOGO_PATH))

# Frame principale
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Frame gauche
left_frame = tk.Frame(main_frame, bg=BG_COLOR)
left_frame.pack(side="left", fill="y", expand=True, padx=(0,10))

version_label = tk.Label(
    left_frame,
    text=f"Version locale : V{local_version}\nVersion distante : V{remote_version}\nStatut : {status_text}",
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=FG_COLOR,
    justify="left"
)
version_label.pack(pady=20)

progress = ttk.Progressbar(left_frame, length=300, mode="determinate")
progress.pack(pady=10)

# ======================================================
# Fonctions
# ======================================================
def download_files():
    for line in file_lines:
        if "|" not in line:
            continue
        file_url, target_path = [p.strip() for p in line.split("|", 1)]
        if "github.com" in file_url and "blob" in file_url:
            file_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        if target_path.lower() == "racine":
            dest_dir = BASE_DIR
        else:
            parts = [p.strip() for p in target_path.split(">")]
            dest_dir = os.path.join(BASE_DIR, *parts)
        os.makedirs(dest_dir, exist_ok=True)
        filename = os.path.basename(file_url)
        dest_file = os.path.join(dest_dir, filename)
        try:
            r = requests.get(file_url, stream=True)
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(dest_file, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        progress['value'] = downloaded / total * 100
                        root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de télécharger {file_url} :\n{e}")

    # Renommer version
    new_version_file = os.path.join(BASE_DIR, f"V{remote_version}.manga")
    if LOCAL_VERSION_FILE:
        os.replace(LOCAL_VERSION_FILE, new_version_file)
    else:
        with open(new_version_file, "w") as f:
            f.write("")

    messagebox.showinfo("Mise à jour terminée", f"Mise à jour vers V{remote_version} terminée !")
    relancer_launcher()

def relancer_launcher():
    launcher_path = os.path.join(BASE_DIR, "Launcher", "Launcher.py")
    if os.path.exists(launcher_path):
        answer = messagebox.askyesno("Relancer", "Voulez-vous relancer le Launcher maintenant ?")
        if answer:
            subprocess.Popen([sys.executable, launcher_path], cwd=os.path.dirname(launcher_path))
            root.destroy()
    else:
        messagebox.showerror("Erreur", f"Launcher introuvable : {launcher_path}")

# Boutons
btn_frame = tk.Frame(left_frame, bg=BG_COLOR)
btn_frame.pack(pady=20)

update_btn = tk.Button(btn_frame, text="Mettre à jour", bg=BUTTON_COLOR, fg=TEXT_COLOR,
                       activebackground=BUTTON_HOVER, font=("Arial", 12, "bold"),
                       command=download_files)
update_btn.pack(side="left", padx=10)

close_btn = tk.Button(btn_frame, text="Fermer", bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      activebackground=BUTTON_HOVER, font=("Arial", 12, "bold"),
                      command=root.destroy)
close_btn.pack(side="right", padx=10)

# Frame droite (image)
right_frame = tk.Frame(main_frame, bg=BG_COLOR)
right_frame.pack(side="right", fill="both", expand=True)

if os.path.exists(IMAGE_PATH):
    main_img = Image.open(IMAGE_PATH).resize((250, 350))
    main_tk = ImageTk.PhotoImage(main_img)
    tk.Label(right_frame, image=main_tk, bg=BG_COLOR).pack(expand=True)
else:
    tk.Label(right_frame, text="IMAGE", font=("Arial", 18), bg=BG_COLOR, fg=FG_COLOR).pack(expand=True)

# ======================================================
# Lancer interface
# ======================================================
root.mainloop()
