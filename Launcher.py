
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
# Dossier du projet (portable)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================
# Lancer automatiquement update.py au démarrage
# ======================================================
update_script = os.path.abspath(
    os.path.join(BASE_DIR, "..", "update.py")
)

print("Chemin update.py :", update_script)

if os.path.exists(update_script):
    try:
        subprocess.Popen([sys.executable, update_script], shell=False)
    except Exception as e:
        # La fenêtre principale n'existe pas encore
        print(f"Impossible de lancer update.py : {e}")
else:
    print(f"update.py introuvable : {update_script}")

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

# ======================================================
# Configuration
# ======================================================
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
dossier_principal = ""

# Lien vers la version supérieure
MANGACV2_URL = "https://github.com/romhackman/MangaCV2"

# ======================================================
# Gestion JSON
# ======================================================
def save_config(path):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"manga_path": path}, f, indent=4)


def load_config():
    global dossier_principal

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                dossier_principal = data.get("manga_path", "")
        except (OSError, json.JSONDecodeError):
            dossier_principal = ""

    if not dossier_principal or not os.path.isdir(dossier_principal):
        path = filedialog.askdirectory(
            title=(
                "Aucun dossier manga valide trouvé.\n"
                "Veuillez sélectionner le dossier contenant vos mangas."
            )
        )

        if path:
            dossier_principal = path
        else:
            dossier_principal = os.path.join(BASE_DIR, "Manga")
            os.makedirs(dossier_principal, exist_ok=True)

            messagebox.showinfo(
                "Configuration par défaut",
                f"Aucun dossier sélectionné.\n"
                f"Le dossier utilisé sera :\n{dossier_principal}"
            )

        save_config(dossier_principal)

    return dossier_principal


# ======================================================
# Thème
# ======================================================
def appliquer_theme(widget):
    for element in widget.winfo_children():
        try:
            element.configure(bg=FOND, fg=TEXTE)
        except (tk.TclError, AttributeError):
            pass

        if isinstance(element, tk.Entry):
            element.configure(
                bg=ENTREE_BG,
                fg=TEXTE,
                insertbackground=TEXTE
            )

        if isinstance(element, tk.Button):
            element.configure(
                bg=BOUTON_BG,
                fg=TEXTE,
                activebackground=GRIS,
                activeforeground=ROUGE
            )

        appliquer_theme(element)


# ======================================================
# Passer au niveau supérieur : ouvrir GitHub
# ======================================================
def ouvrir_mangacv2():
    try:
        webbrowser.open(MANGACV2_URL)
    except Exception as e:
        messagebox.showerror(
            "Erreur",
            f"Impossible d'ouvrir le lien GitHub :\n{e}"
        )


# ======================================================
# Popup : Passer au niveau supérieur
# ======================================================
def popup_niveau_superieur():
    popup = tk.Toplevel(fenetre)
    popup.title("Passez au niveau supérieur !")
    popup.geometry("420x220")
    popup.configure(bg=FOND)
    popup.resizable(False, False)
    popup.transient(fenetre)

    # Centrer la popup sur la fenêtre principale
    popup.update_idletasks()

    x = fenetre.winfo_rootx() + (
        fenetre.winfo_width() - 420
    ) // 2

    y = fenetre.winfo_rooty() + (
        fenetre.winfo_height() - 220
    ) // 2

    popup.geometry(f"420x220+{x}+{y}")

    tk.Label(
        popup,
        text="🚀 Passez au niveau supérieur !",
        font=("Arial", 15, "bold"),
        bg=FOND,
        fg=TEXTE
    ).pack(pady=(22, 12))

    tk.Label(
        popup,
        text=(
            "Envie d'aller plus loin ?\n"
            "Découvrez MangaCV2 sur GitHub !"
        ),
        font=("Arial", 11),
        bg=FOND,
        fg=TEXTE,
        justify="center"
    ).pack(pady=5)

    tk.Button(
        popup,
        text="🚀 Découvrir MangaCV2",
        font=("Arial", 11, "bold"),
        bg=BOUTON_BG,
        fg=TEXTE,
        activebackground=GRIS,
        command=ouvrir_mangacv2,
        padx=12,
        pady=5
    ).pack(pady=12)

    tk.Button(
        popup,
        text="Plus tard",
        bg=GRIS,
        fg=TEXTE,
        command=popup.destroy
    ).pack()


# ======================================================
# Choisir le dossier manga
# ======================================================
def choisir_dossier():
    global dossier_principal

    path = filedialog.askdirectory(
        title="Choisir le dossier racine des mangas"
    )

    if path:
        dossier_principal = path
        save_config(dossier_principal)
        refresh_mangas()


# ======================================================
# Rafraîchir la liste des mangas
# ======================================================
def refresh_mangas():
    manga_listbox.delete(0, tk.END)
    chapter_listbox.delete(0, tk.END)

    if not dossier_principal or not os.path.isdir(dossier_principal):
        return

    try:
        mangas = [
            d for d in os.listdir(dossier_principal)
            if os.path.isdir(os.path.join(dossier_principal, d))
        ]
    except OSError as e:
        messagebox.showerror(
            "Erreur",
            f"Impossible de lire le dossier manga :\n{e}"
        )
        return

    for manga in sorted(mangas, key=str.casefold):
        manga_listbox.insert(tk.END, manga)


# ======================================================
# Afficher les chapitres
# ======================================================
def show_chapters(event=None):
    chapter_listbox.delete(0, tk.END)

    selection = manga_listbox.curselection()
    if not selection:
        return

    manga_name = manga_listbox.get(selection[0])
    path_chap = os.path.join(dossier_principal, manga_name)

    if not os.path.isdir(path_chap):
        return

    try:
        chapters = [
            f for f in os.listdir(path_chap)
            if f.lower().endswith(".pdf")
        ]
    except OSError as e:
        messagebox.showerror(
            "Erreur",
            f"Impossible de lire les chapitres :\n{e}"
        )
        return

    def extract_number(filename):
        import re

        numbers = re.findall(r"\d+", filename)
        return int(numbers[-1]) if numbers else float("inf")

    chapters.sort(key=lambda f: (extract_number(f), f.casefold()))

    for chap in chapters:
        chapter_listbox.insert(tk.END, chap)


# ======================================================
# Ouvrir un PDF
# ======================================================
def open_chapter(event):
    # Ouvrir uniquement si l'utilisateur clique sur un élément
    index = chapter_listbox.nearest(event.y)

    if index < 0:
        return

    bbox = chapter_listbox.bbox(index)
    if not bbox or not (
        bbox[1] <= event.y <= bbox[1] + bbox[3]
    ):
        return

    manga_sel = manga_listbox.curselection()
    if not manga_sel:
        return

    chapter_name = chapter_listbox.get(index)
    manga_name = manga_listbox.get(manga_sel[0])

    file_path = os.path.abspath(
        os.path.join(dossier_principal, manga_name, chapter_name)
    )

    if not os.path.isfile(file_path):
        messagebox.showerror(
            "Erreur",
            "Fichier PDF introuvable !"
        )
        return

    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])
    except Exception as e:
        messagebox.showerror(
            "Erreur",
            f"Impossible d'ouvrir le PDF :\n{e}"
        )


# ======================================================
# Curseur main
# ======================================================
def on_chapter_hover(event):
    chapter_listbox.config(cursor="hand2")


def on_chapter_leave(event):
    chapter_listbox.config(cursor="")


# ======================================================
# Lancer un programme portable
# ======================================================
def lancer_script(chemin):
    chemin = os.path.abspath(chemin)

    if os.path.isfile(chemin):
        try:
            subprocess.Popen([sys.executable, chemin])
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de lancer le programme :\n{e}"
            )
    else:
        messagebox.showerror(
            "Erreur",
            f"Le fichier est introuvable :\n{chemin}"
        )


# ======================================================
# Interface
# ======================================================
fenetre = tk.Tk()
fenetre.title("Lecteur de Scan Manga")
fenetre.geometry("900x500")
fenetre.minsize(750, 450)
fenetre.configure(bg=FOND)

# Icône de la fenêtre
try:
    icon_path = os.path.join(BASE_DIR, "logo.png")
    icon_img = tk.PhotoImage(file=icon_path)
    fenetre.iconphoto(True, icon_img)
except (tk.TclError, OSError):
    pass


# ======================================================
# Boutons en haut
# ======================================================
frame_boutons = tk.Frame(fenetre, bg=FOND)
frame_boutons.pack(anchor="nw", padx=5, pady=5)

tk.Button(
    frame_boutons,
    text="⚙️",
    command=choisir_dossier
).pack(side="left", padx=2)

tk.Button(
    frame_boutons,
    text="🧩",
    command=lambda: lancer_script(
        os.path.join(BASE_DIR, "..", "plugins", "plugin_interface.py")
    )
).pack(side="left", padx=2)

tk.Button(
    frame_boutons,
    text="pdfV2",
    command=lambda: lancer_script(
        os.path.join(BASE_DIR, "..", "programme", "pdfV2.py")
    )
).pack(side="left", padx=2)

tk.Button(
    frame_boutons,
    text="AnimeSama",
    command=lambda: [
        lancer_script(
            os.path.join(BASE_DIR, "..", "anime_sama", "lecture.py")
        ),
        lancer_script(
            os.path.join(
                BASE_DIR, "..", "anime_sama", "APP",
                "scraper_domaine.py"
            )
        )
    ]
).pack(side="left", padx=2)

tk.Button(
    frame_boutons,
    text="Mangadex",
    command=lambda: lancer_script(
        os.path.join(BASE_DIR, "..", "mangadex", "main.py")
    )
).pack(side="left", padx=2)

# Nouveau bouton : niveau supérieur
tk.Button(
    frame_boutons,
    text="🚀 Niveau supérieur",
    command=ouvrir_mangacv2,
    font=("Arial", 9, "bold"),
    bg="#F0C75E",
    fg="#000000",
    activebackground="#FFD978",
    padx=6
).pack(side="left", padx=5)


# ======================================================
# Zone principale
# ======================================================
frame_main = tk.Frame(fenetre, bg=FOND)
frame_main.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


# ======================================================
# Listes des mangas et chapitres
# ======================================================
frame_listes = tk.Frame(frame_main, bg=FOND)
frame_listes.pack(side="left", fill=tk.Y)

tk.Label(
    frame_listes,
    text="Mangas :",
    font=("Arial", 12, "bold"),
    bg=FOND,
    fg=TEXTE
).grid(row=0, column=0, padx=5, pady=5)

tk.Label(
    frame_listes,
    text="Chapitres :",
    font=("Arial", 12, "bold"),
    bg=FOND,
    fg=TEXTE
).grid(row=0, column=1, padx=5, pady=5)

manga_listbox = tk.Listbox(
    frame_listes,
    width=25,
    height=20,
    bg=ENTREE_BG,
    fg=TEXTE,
    selectbackground=BLEU,
    selectforeground="#FFFFFF"
)
manga_listbox.grid(row=1, column=0, padx=5, pady=5)
manga_listbox.bind("<<ListboxSelect>>", show_chapters)

chapter_listbox = tk.Listbox(
    frame_listes,
    width=25,
    height=20,
    bg=ENTREE_BG,
    fg=TEXTE,
    selectbackground=BLEU,
    selectforeground="#FFFFFF"
)
chapter_listbox.grid(row=1, column=1, padx=5, pady=5)
chapter_listbox.bind("<Button-1>", open_chapter)
chapter_listbox.bind("<Motion>", on_chapter_hover)
chapter_listbox.bind("<Leave>", on_chapter_leave)

tk.Button(
    frame_listes,
    text="Actualiser",
    command=refresh_mangas
).grid(row=2, column=0, columnspan=2, pady=10)


# ======================================================
# Image à droite
# ======================================================
frame_image = tk.Frame(frame_main, bg=FOND)
frame_image.pack(
    side="right",
    fill=tk.BOTH,
    expand=True,
    padx=10
)

try:
    image_path = os.path.join(BASE_DIR, "image.png")

    image_orig = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image_orig.resize((300, 480)))

    image_label = tk.Label(
        frame_image,
        image=image_tk,
        bg=FOND
    )
    image_label.image = image_tk
    image_label.pack(expand=True)

except (OSError, tk.TclError):
    tk.Label(
        frame_image,
        text="(Aucune image)",
        font=("Arial", 14),
        bg=FOND,
        fg=TEXTE
    ).pack(expand=True)


# ======================================================
# Lancement
# ======================================================
load_config()
refresh_mangas()

# Afficher la popup une seconde après l'ouverture
fenetre.after(1000, popup_niveau_superieur)

fenetre.mainloop()
