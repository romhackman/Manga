import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser
import platform
import subprocess
import sys

# ======================================================
# Dossier du projet (portable pour tout le monde)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================
# Thème
# ======================================================
FOND = "#fbbeaf"
BLEU = "#007ACC"
ROUGE = "#D43F3A"
GRIS = "#E0CFC7"
ENTREE_BG = "#F5D1C1"
TEXTE = "#000000"
BOUTON_BG = "#E6A38C"

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
dossier_principal = ""

# ======================================================
# Gestion JSON
# ======================================================
def load_config():
    global dossier_principal
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                dossier_principal = data.get("manga_path", "")
        except:
            dossier_principal = ""
    return dossier_principal


def save_config(path):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"manga_path": path}, f, indent=4)


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
            element.configure(
                bg=BOUTON_BG,
                fg=TEXTE,
                activebackground=GRIS,
                activeforeground=ROUGE
            )

        appliquer_theme(element)


# ======================================================
# Choisir dossier
# ======================================================
def choisir_dossier():
    global dossier_principal
    path = filedialog.askdirectory(title="Choisir le dossier racine des mangas")
    if path:
        dossier_principal = path
        texte_dossier.set(f"Dossier sélectionné : {dossier_principal}")
        save_config(dossier_principal)
        refresh_mangas()


# ======================================================
# Rafraîchir mangas
# ======================================================
def refresh_mangas():
    manga_listbox.delete(0, tk.END)
    chapter_listbox.delete(0, tk.END)

    if not dossier_principal or not os.path.exists(dossier_principal):
        return

    mangas = [
        d for d in os.listdir(dossier_principal)
        if os.path.isdir(os.path.join(dossier_principal, d))
    ]

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

    chapters = [f for f in os.listdir(path_chap) if f.lower().endswith(".pdf")]

    def extract_number(f):
        try:
            return int(f.split("_")[1].replace(".pdf", ""))
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

    file_path = os.path.abspath(
        os.path.join(dossier_principal, manga_name, chapter_name)
    )

    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Fichier PDF introuvable !")
        return

    if platform.system() == "Windows":
        url = "file:///" + file_path.replace("\\", "/")
    else:
        url = "file://" + file_path

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
def lancer_script(chemin):
    if os.path.exists(chemin):
        subprocess.Popen([sys.executable, chemin])
    else:
        messagebox.showerror("Erreur", f"Le fichier est introuvable :\n{chemin}")


# ======================================================
# Interface
# ======================================================
fenetre = tk.Tk()
fenetre.title("Lecteur de Scan Manga")
fenetre.geometry("900x500")
fenetre.configure(bg=FOND)

# Icône de la fenêtre
try:
    icon_path = os.path.join(BASE_DIR, "logo.png")
    icon_img = tk.PhotoImage(file=icon_path)
    fenetre.iconphoto(True, icon_img)
except:
    pass


# ----------------- Boutons haut gauche (ordre personnalisé) -----------------
frame_boutons = tk.Frame(fenetre, bg=FOND)
frame_boutons.pack(anchor="nw", padx=5, pady=5)

# Configuration
tk.Button(frame_boutons, text="⚙️", command=choisir_dossier).pack(side="left", padx=2)

# PDF
tk.Button(frame_boutons, text="pdfV2",
          command=lambda: lancer_script(os.path.join(BASE_DIR, "..", "programme", "pdfV2.py"))
         ).pack(side="left", padx=2)

# Sites
tk.Button(frame_boutons, text="AnimeSama",
          command=lambda: lancer_script(os.path.join(BASE_DIR, "..", "anime_sama", "lecture.py"))
         ).pack(side="left", padx=2)
tk.Button(frame_boutons, text="Mangadex",
          command=lambda: lancer_script(os.path.join(BASE_DIR, "..", "mangadex", "main.py"))
         ).pack(side="left", padx=2)


# ----------------- Frame principale -----------------
frame_main = tk.Frame(fenetre, bg=FOND)
frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ----------------- Listes -----------------
frame_listes = tk.Frame(frame_main, bg=FOND)
frame_listes.pack(side="left", fill=tk.Y)

tk.Label(frame_listes, text="Mangas :", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_listes, text="Chapitres :", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)

manga_listbox = tk.Listbox(frame_listes, width=25, height=20)
manga_listbox.grid(row=1, column=0, padx=5, pady=5)
manga_listbox.bind("<<ListboxSelect>>", show_chapters)

chapter_listbox = tk.Listbox(frame_listes, width=25, height=20)
chapter_listbox.grid(row=1, column=1, padx=5, pady=5)
chapter_listbox.bind("<Button-1>", open_chapter)
chapter_listbox.bind("<Motion>", on_chapter_hover)
chapter_listbox.bind("<Leave>", on_chapter_leave)

tk.Button(frame_listes, text="Actualiser", command=refresh_mangas)\
    .grid(row=2, column=0, columnspan=2, pady=10)

texte_dossier = tk.StringVar(value="Aucun dossier sélectionné")
tk.Label(frame_listes, textvariable=texte_dossier, font=("Arial", 12))\
    .grid(row=3, column=0, columnspan=2, pady=5)

# ----------------- Image -----------------
frame_image = tk.Frame(frame_main, bg=FOND)
frame_image.pack(side="right", fill=tk.BOTH, expand=True, padx=10)

try:
    image_path = os.path.join(BASE_DIR, "image.png")
    image_orig = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image_orig.resize((300, 480)))
    tk.Label(frame_image, image=image_tk, bg=FOND).pack(expand=True)
except:
    tk.Label(frame_image, text="(Aucune image)", font=("Arial", 14)).pack(expand=True)

# ======================================================
# Lancement
# ======================================================
appliquer_theme(fenetre)
load_config()

if dossier_principal:
    texte_dossier.set(f"Dossier sélectionné : {dossier_principal}")
    refresh_mangas()

fenetre.mainloop()
