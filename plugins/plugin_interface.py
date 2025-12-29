import os
import json
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ============================
# Dossiers et fichiers
# ============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
JSON_FILE = os.path.join(PLUGINS_DIR, "instance_plugins.json")
TEMP_JSON = os.path.join(PLUGINS_DIR, "temp_link.json")
IMAGE_PATH = os.path.join(BASE_DIR, "image.png")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")

# ============================
# Couleurs et thème
# ============================
FOND = "#FFD700"
TEXTE = "#000000"
BOUTON_BG = "#FFC107"

# ============================
# Créer JSON vide si nécessaire
# ============================
os.makedirs(PLUGINS_DIR, exist_ok=True)
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# ============================
# Lancer un plugin
# ============================
def lancer_plugin(nom):
    if nom in instance_plugins:
        fichier = instance_plugins[nom]
        if os.path.exists(fichier):
            try:
                if fichier.endswith(".py"):
                    subprocess.Popen([sys.executable, fichier])
                else:
                    if os.name != "nt":
                        os.chmod(fichier, 0o755)
                    subprocess.Popen([fichier], shell=True)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer le plugin : {e}")
        else:
            messagebox.showerror("Erreur", f"Fichier introuvable : {fichier}")
    else:
        messagebox.showerror("Erreur", f"Plugin '{nom}' introuvable dans le JSON.")

# ============================
# Charger les plugins
# ============================
def actualiser_plugins():
    global instance_plugins
    listbox_plugins.delete(0, tk.END)
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            instance_plugins = json.load(f)
        for nom in sorted(instance_plugins.keys()):
            listbox_plugins.insert(tk.END, nom)
    else:
        instance_plugins = {}

# ============================
# Télécharger un plugin
# ============================
def telecharger_plugin():
    lien = entry_lien.get().strip()
    if not lien:
        messagebox.showwarning("Avertissement", "Veuillez entrer un lien GitHub.")
        return

    os.makedirs(PLUGINS_DIR, exist_ok=True)
    with open(TEMP_JSON, "w", encoding="utf-8") as f:
        json.dump({"link": lien}, f, indent=4)

    installer_script = os.path.join(BASE_DIR, "plugins_installer.py")
    if os.path.exists(installer_script):
        try:
            subprocess.Popen([sys.executable, installer_script, "--link", lien])
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'installation : {e}")
    else:
        messagebox.showerror("Erreur", "plugins_installer.py introuvable.")

    entry_lien.delete(0, tk.END)
    root.after(3000, actualiser_plugins)  # actualiser après 3 sec

# ============================
# Fenêtre principale
# ============================
root = tk.Tk()
root.title("Plugins")
root.geometry("900x500")
root.configure(bg=FOND)

# Icône
if os.path.exists(LOGO_PATH):
    try:
        root.iconphoto(True, tk.PhotoImage(file=LOGO_PATH))
    except:
        pass

# ----------------- Frame principal -----------------
frame_main = tk.Frame(root, bg=FOND)
frame_main.pack(fill=tk.BOTH, expand=True)

# ----------------- Liste des plugins -----------------
frame_plugins = tk.Frame(frame_main, bg=FOND)
frame_plugins.pack(side="left", fill=tk.Y, padx=10, pady=10)

tk.Label(frame_plugins, text="Plugins :", font=("Arial", 16, "bold"), bg=FOND, fg=TEXTE).pack(pady=5)

listbox_plugins = tk.Listbox(frame_plugins, width=30, height=20, bg="white", fg=TEXTE)
listbox_plugins.pack(pady=5)

def on_double_click(event):
    try:
        selection = listbox_plugins.get(listbox_plugins.curselection()[0])
        lancer_plugin(selection)
    except IndexError:
        pass

listbox_plugins.bind("<Double-Button-1>", on_double_click)

btn_actualiser = tk.Button(frame_plugins, text="Actualiser", bg=BOUTON_BG, fg=TEXTE, command=actualiser_plugins)
btn_actualiser.pack(pady=5)

# ----------------- Zone pour lien GitHub -----------------
frame_lien = tk.Frame(frame_plugins, bg=FOND)
frame_lien.pack(pady=10)

entry_lien = tk.Entry(frame_lien, width=25)
entry_lien.pack(side="left", padx=5)

btn_telecharger = tk.Button(frame_lien, text="Télécharger", bg=BOUTON_BG, fg=TEXTE, command=telecharger_plugin)
btn_telecharger.pack(side="left", padx=5)

# ----------------- Image à droite -----------------
frame_image = tk.Frame(frame_main, bg=FOND)
frame_image.pack(side="right", fill=tk.BOTH, expand=True)

if os.path.exists(IMAGE_PATH):
    img_orig = Image.open(IMAGE_PATH)
    img_tk = ImageTk.PhotoImage(img_orig.resize((300, 480)))
    label_img = tk.Label(frame_image, image=img_tk, bg=FOND)
    label_img.pack(expand=True)
else:
    tk.Label(frame_image, text="(Aucune image)", font=("Arial", 14), bg=FOND, fg=TEXTE).pack(expand=True)

# ----------------- Charger plugins au démarrage -----------------
actualiser_plugins()

root.mainloop()
