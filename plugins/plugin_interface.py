import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
JSON_FILE = os.path.join(PLUGINS_DIR, "instance_plugins.json")
TEMP_JSON = os.path.join(PLUGINS_DIR, "temp_link.json")

IMAGE_PATH = os.path.join(BASE_DIR, "image.png")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")

os.makedirs(PLUGINS_DIR, exist_ok=True)

# Python du .venv
if os.name == "nt":
    VENV_PYTHON = os.path.abspath(os.path.join(BASE_DIR, "..", ".venv", "Scripts", "python.exe"))
else:
    VENV_PYTHON = os.path.abspath(os.path.join(BASE_DIR, "..", ".venv", "bin", "python"))

if not os.path.exists(VENV_PYTHON):
    messagebox.showerror("Erreur critique", ".venv introuvable")
    sys.exit(1)

FOND = "#FFD700"
TEXTE = "#000000"
BOUTON_BG = "#FFC107"

def charger_plugins():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

instance_plugins = charger_plugins()

def lancer_plugin(nom):
    if nom not in instance_plugins:
        messagebox.showerror("Erreur", f"Plugin '{nom}' introuvable.")
        return

    fichier = instance_plugins[nom]
    if not os.path.exists(fichier):
        messagebox.showerror("Erreur", f"Fichier introuvable : {fichier}")
        return

    try:
        subprocess.Popen([VENV_PYTHON, fichier])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def actualiser_plugins():
    global instance_plugins
    listbox_plugins.delete(0, tk.END)
    instance_plugins = charger_plugins()
    for nom in sorted(instance_plugins):
        listbox_plugins.insert(tk.END, nom)

def telecharger_plugin():
    lien = entry_lien.get().strip()
    if not lien:
        messagebox.showwarning("Avertissement", "Veuillez entrer un lien GitHub.")
        return

    os.makedirs(PLUGINS_DIR, exist_ok=True)

    with open(TEMP_JSON, "w", encoding="utf-8") as f:
        json.dump({"link": lien}, f, indent=4)

    installer_script = os.path.join(BASE_DIR, "plugins_installer.py")

    try:
        subprocess.Popen([VENV_PYTHON, installer_script, "--link", lien])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

    entry_lien.delete(0, tk.END)
    root.after(3000, actualiser_plugins)

root = tk.Tk()
root.title("Plugins")
root.geometry("900x500")
root.configure(bg=FOND)

if os.path.exists(LOGO_PATH):
    try:
        root.iconphoto(True, tk.PhotoImage(file=LOGO_PATH))
    except:
        pass

frame_main = tk.Frame(root, bg=FOND)
frame_main.pack(fill=tk.BOTH, expand=True)

frame_plugins = tk.Frame(frame_main, bg=FOND)
frame_plugins.pack(side="left", fill=tk.Y, padx=10, pady=10)

tk.Label(frame_plugins, text="Plugins :", font=("Arial", 16, "bold"),
         bg=FOND, fg=TEXTE).pack(pady=5)

listbox_plugins = tk.Listbox(frame_plugins, width=30, height=20,
                             bg="white", fg=TEXTE)
listbox_plugins.pack(pady=5)

listbox_plugins.bind(
    "<Double-Button-1>",
    lambda e: lancer_plugin(listbox_plugins.get(tk.ACTIVE))
)

btn_actualiser = tk.Button(frame_plugins, text="Actualiser",
                           bg=BOUTON_BG, fg=TEXTE,
                           command=actualiser_plugins)
btn_actualiser.pack(pady=5)

frame_lien = tk.Frame(frame_plugins, bg=FOND)
frame_lien.pack(pady=10)

entry_lien = tk.Entry(frame_lien, width=25)
entry_lien.pack(side="left", padx=5)

btn_telecharger = tk.Button(frame_lien, text="Télécharger",
                            bg=BOUTON_BG, fg=TEXTE,
                            command=telecharger_plugin)
btn_telecharger.pack(side="left", padx=5)

frame_image = tk.Frame(frame_main, bg=FOND)
frame_image.pack(side="right", fill=tk.BOTH, expand=True)

if os.path.exists(IMAGE_PATH):
    img_orig = Image.open(IMAGE_PATH)
    img_tk = ImageTk.PhotoImage(img_orig.resize((300, 480)))
    tk.Label(frame_image, image=img_tk, bg=FOND).pack(expand=True)
else:
    tk.Label(frame_image, text="(Aucune image)",
             font=("Arial", 14),
             bg=FOND, fg=TEXTE).pack(expand=True)

actualiser_plugins()
root.mainloop()
