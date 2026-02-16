import os
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import platform
import subprocess
import sys

# ======================================================
# Chemin du launcher et config.json
# ======================================================
LAUNCHER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Launcher"))
CONFIG_FILE = os.path.join(LAUNCHER_DIR, "config.json")
dossier_principal = ""

# ======================================================
# Thème sombre
# ======================================================
FOND = "#121212"
BLEU = "#1E88E5"
ROUGE = "#EF5350"
GRIS = "#333333"
ENTREE_BG = "#1E1E1E"
TEXTE = "#E0E0E0"
BOUTON_BG = "#1E1E1E"

# ======================================================
# Charger config.json
# ======================================================
def load_config():
    global dossier_principal
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                dossier_principal = data.get("manga_path", "")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire config.json :\n{e}")
            dossier_principal = ""
    else:
        messagebox.showerror("Erreur", f"Fichier config.json introuvable :\n{CONFIG_FILE}")
        dossier_principal = ""
    # Vérifie que le dossier existe
    if not os.path.exists(dossier_principal):
        messagebox.showerror("Erreur", f"Dossier manga introuvable :\n{dossier_principal}")
        dossier_principal = ""
    return dossier_principal

# ======================================================
# Thème
# ======================================================
def appliquer_theme(widget):
    for element in widget.winfo_children():
        try:
            element.configure(bg=FOND, fg=TEXTE)
        except:
            pass
        if isinstance(element, tk.Entry):
            element.configure(bg=ENTREE_BG, fg=TEXTE, insertbackground=TEXTE)
        if isinstance(element, tk.Button):
            element.configure(bg=BOUTON_BG, fg=TEXTE, activebackground=GRIS, activeforeground=ROUGE)
        appliquer_theme(element)

# ======================================================
# Rafraîchir mangas
# ======================================================
def refresh_mangas():
    manga_listbox.delete(0, tk.END)
    chapter_listbox.delete(0, tk.END)
    if not dossier_principal or not os.path.exists(dossier_principal):
        return

    # Liste des sous-dossiers → chaque sous-dossier = un manga
    mangas = [d for d in os.listdir(dossier_principal) if os.path.isdir(os.path.join(dossier_principal, d))]
    for manga in sorted(mangas):
        manga_listbox.insert(tk.END, manga)

# ======================================================
# Afficher chapitres
# ======================================================
def show_chapters(event):
    chapter_listbox.delete(0, tk.END)
    selection = manga_listbox.curselection()
    if not selection:
        return
    manga_name = manga_listbox.get(selection[0])
    path_chap = os.path.join(dossier_principal, manga_name)
    if not os.path.exists(path_chap):
        return

    # On récupère uniquement les fichiers PDF avec le format Chapitre_[num].pdf
    chapters = [f for f in os.listdir(path_chap)
                if f.lower().endswith(".pdf") and "chapitre_" in f.lower()]

    # Tri par numéro de chapitre
    def extract_number(f):
        try:
            num = f.lower().split("chapitre_")[1].replace(".pdf", "")
            return int(num)
        except:
            return 999999

    chapters.sort(key=extract_number)

    for chap in chapters:
        chapter_listbox.insert(tk.END, chap)

# ======================================================
# Ouvrir PDF
# ======================================================
def open_chapter(event):
    index = chapter_listbox.nearest(event.y)
    if index < 0:
        return
    chapter_name = chapter_listbox.get(index)
    manga_sel = manga_listbox.curselection()
    if not manga_sel:
        return
    manga_name = manga_listbox.get(manga_sel[0])
    file_path = os.path.abspath(os.path.join(dossier_principal, manga_name, chapter_name))
    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Fichier PDF introuvable !")
        return
    url = "file:///" + file_path.replace("\\", "/") if platform.system() == "Windows" else "file://" + file_path
    webbrowser.open_new(url)

# ======================================================
# Curseur main
# ======================================================
def on_chapter_hover(event):
    chapter_listbox.config(cursor="hand2")
def on_chapter_leave(event):
    chapter_listbox.config(cursor="")

# ======================================================
# Lancer un programme (PORTABLE)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def lancer_script(chemin):
    if os.path.exists(chemin):
        subprocess.Popen([sys.executable, chemin])
    else:
        messagebox.showerror("Erreur", f"Le fichier est introuvable :\n{chemin}")

def lancer_mangaV3():
    lancer_script(os.path.join(BASE_DIR, "mangaV3.py"))

def lancer_pdfV2():
    lancer_script(os.path.abspath(os.path.join(BASE_DIR, "..", "programme", "pdfV2.py")))

def lancer_share():
    lancer_script(os.path.join(BASE_DIR, "shareV2.py"))

def lancer_APP():
    lancer_script(os.path.join(BASE_DIR, "APP", "APPV5.py"))

def lancer_State_Extra():
    lancer_script(os.path.join(BASE_DIR, "APP", "State_Scan", "State_Extra.py"))

# ======================================================
# Interface
# ======================================================
fenetre = tk.Tk()
fenetre.title("Lecteur de Scan Manga")
fenetre.geometry("900x500")
fenetre.configure(bg=FOND)

# Icône
try:
    icon_path = os.path.join(BASE_DIR, "logo.png")
    icon_img = tk.PhotoImage(file=icon_path)
    fenetre.iconphoto(True, icon_img)
except:
    pass

# ----------------- Boutons haut gauche -----------------
frame_boutons = tk.Frame(fenetre, bg=FOND)
frame_boutons.pack(anchor="nw", padx=5, pady=5)
tk.Button(frame_boutons, text="MangaV3", command=lancer_mangaV3).pack(side="left", padx=2)
tk.Button(frame_boutons, text="pdfV2", command=lancer_pdfV2).pack(side="left", padx=2)
tk.Button(frame_boutons, text="ShareV2", command=lancer_share).pack(side="left", padx=2)
tk.Button(frame_boutons, text="APPV5", command=lancer_APP).pack(side="left", padx=2)
tk.Button(frame_boutons, text="State & Extra", command=lancer_State_Extra).pack(side="left", padx=2)

# ----------------- Frame principale -----------------
frame_main = tk.Frame(fenetre, bg=FOND)
frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ----------------- Listes -----------------
frame_listes = tk.Frame(frame_main, bg=FOND)
frame_listes.pack(side="left", fill=tk.Y)
tk.Label(frame_listes, text="Mangas :", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_listes, text="Chapitres :", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)

manga_listbox = tk.Listbox(frame_listes, width=25, height=20, bg=ENTREE_BG, fg=TEXTE,
                           selectbackground=BLEU, selectforeground=TEXTE)
manga_listbox.grid(row=1, column=0, padx=5, pady=5)
manga_listbox.bind("<<ListboxSelect>>", show_chapters)

chapter_listbox = tk.Listbox(frame_listes, width=25, height=20, bg=ENTREE_BG, fg=TEXTE,
                             selectbackground=BLEU, selectforeground=TEXTE)
chapter_listbox.grid(row=1, column=1, padx=5, pady=5)
chapter_listbox.bind("<Button-1>", open_chapter)
chapter_listbox.bind("<Motion>", on_chapter_hover)
chapter_listbox.bind("<Leave>", on_chapter_leave)

tk.Button(frame_listes, text="Actualiser", command=refresh_mangas).grid(row=2, column=0, columnspan=2, pady=10)

# ----------------- Image -----------------
frame_image = tk.Frame(frame_main, bg=FOND)
frame_image.pack(side="right", fill=tk.BOTH, expand=True, padx=10)

try:
    image_path = os.path.join(BASE_DIR, "image.png")
    image_orig = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image_orig.resize((300, 480)))
    tk.Label(frame_image, image=image_tk, bg=FOND).pack(expand=True)
except:
    tk.Label(frame_image, text="(Aucune image)", font=("Arial", 14), fg=TEXTE, bg=FOND).pack(expand=True)

# ======================================================
# Lancement
# ======================================================
appliquer_theme(fenetre)
load_config()
refresh_mangas()
fenetre.mainloop()

