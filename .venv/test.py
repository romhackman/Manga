import os
import re
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ----------------- Thème harmonisé -----------------
FOND = "#fbbeaf"
BLEU = "#007ACC"
ROUGE = "#D43F3A"
GRIS = "#E0CFC7"
ENTREE_BG = "#F5D1C1"
TEXTE = "#000000"
BOUTON_BG = "#E6A38C"


# ----------------- Fonctions utilitaires -----------------
def appliquer_theme(widget):
    for element in widget.winfo_children():
        try:
            element.configure(bg=FOND, fg=TEXTE)
        except:
            pass

        if isinstance(element, tk.Button):
            element.configure(
                bg=BOUTON_BG,
                fg=TEXTE,
                activebackground=GRIS,
                activeforeground=ROUGE
            )

        appliquer_theme(element)


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


# ----------------- Création PDF pour 1 dossier -----------------
def creer_pdf(dossier_chapitre):
    images = []
    fichiers = sorted(os.listdir(dossier_chapitre), key=natural_sort_key)

    for fichier in fichiers:
        if fichier.lower().endswith((".jpg", ".jpeg", ".png")):
            chemin = os.path.join(dossier_chapitre, fichier)
            img = Image.open(chemin).convert('RGB')
            images.append(img)

    if not images:
        return False, "Aucune image trouvée"

    nom_chapitre = os.path.basename(dossier_chapitre)
    dossier_parent = os.path.dirname(dossier_chapitre)
    chemin_pdf = os.path.join(dossier_parent, f"{nom_chapitre}.pdf")

    try:
        images[0].save(chemin_pdf, save_all=True, append_images=images[1:])
        return True, chemin_pdf
    except Exception as e:
        return False, str(e)


# ----------------- MODES -----------------
def mode_normal():
    dossier_chapitre = filedialog.askdirectory(title="Choisir un dossier contenant des images")
    if not dossier_chapitre:
        return

    ok, msg = creer_pdf(dossier_chapitre)
    if ok:
        messagebox.showinfo("Succès", f"PDF créé :\n{msg}")
    else:
        messagebox.showerror("Erreur", msg)


def mode_boost():
    dossier_racine = filedialog.askdirectory(title="Choisir un dossier contenant plusieurs chapitres")
    if not dossier_racine:
        return

    sous_dossiers = [os.path.join(dossier_racine, d) for d in os.listdir(dossier_racine)
                     if os.path.isdir(os.path.join(dossier_racine, d))]

    if not sous_dossiers:
        messagebox.showerror("Erreur", "Aucun dossier de chapitre trouvé.")
        return

    resultats = []
    for dossier in sorted(sous_dossiers, key=natural_sort_key):
        ok, msg = creer_pdf(dossier)
        resultats.append(f"{os.path.basename(dossier)} → {'OK' if ok else 'Erreur'} ({msg})")

    messagebox.showinfo("Terminé", "\n".join(resultats))


def mode_full_pdf():
    dossier_racine = filedialog.askdirectory(title="Choisir un dossier contenant plusieurs chapitres")
    if not dossier_racine:
        return

    sous_dossiers = [os.path.join(dossier_racine, d) for d in os.listdir(dossier_racine)
                     if os.path.isdir(os.path.join(dossier_racine, d))]

    if not sous_dossiers:
        messagebox.showerror("Erreur", "Aucun chapitre trouvé.")
        return

    toutes_images = []

    for dossier in sorted(sous_dossiers, key=natural_sort_key):
        fichiers = sorted(os.listdir(dossier), key=natural_sort_key)
        for fichier in fichiers:
            if fichier.lower().endswith((".jpg", ".jpeg", ".png")):
                chemin = os.path.join(dossier, fichier)
                img = Image.open(chemin).convert('RGB')
                toutes_images.append(img)

    if not toutes_images:
        messagebox.showerror("Erreur", "Aucune image trouvée.")
        return

    chemin_pdf = os.path.join(dossier_racine, "Tous_les_chapitres.pdf")

    try:
        toutes_images[0].save(chemin_pdf, save_all=True, append_images=toutes_images[1:])
        messagebox.showinfo("Succès", f"PDF complet créé :\n{chemin_pdf}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


# ----------------- Interface -----------------
fenetre = tk.Tk()
fenetre.title("IMAGE → PDF MAKER")
fenetre.configure(bg=FOND)

HAUTEUR_IMAGE = 1536
LARGEUR_FORMULAIRE = 450
LARGEUR_IMAGE = 1024
fenetre.geometry(f"{LARGEUR_FORMULAIRE + LARGEUR_IMAGE}x{HAUTEUR_IMAGE}")

# Logo
try:
    logo = tk.PhotoImage(file="logo.png")
    fenetre.iconphoto(False, logo)
except:
    pass

# ---- Colonne de gauche ----
frame_left = tk.Frame(fenetre, bg=FOND, width=LARGEUR_FORMULAIRE, height=HAUTEUR_IMAGE)
frame_left.pack(side="left", fill="y", padx=10, pady=10)

tk.Label(frame_left, text="Convertisseur d'images en PDF",
         bg=FOND, fg=TEXTE, font=("Arial", 18, "bold")).pack(pady=20)

tk.Button(frame_left, text="Mode normal : PDF pour 1 dossier",
          command=mode_normal, font=("Arial", 14)).pack(pady=15, fill="x")

tk.Button(frame_left, text="Mode boosté : PDF pour plusieurs dossiers",
          command=mode_boost, font=("Arial", 14)).pack(pady=15, fill="x")

tk.Button(frame_left, text="Mode Full PDF : 1 PDF global",
          command=mode_full_pdf, font=("Arial", 14)).pack(pady=15, fill="x")

# ---- Image de droite ----
frame_right = tk.Frame(fenetre, bg=FOND)
frame_right.pack(side="right", fill="both", expand=True)

try:
    img = Image.open("image.png")

    # Redimension automatique pour rentrer dans la zone
    max_width = LARGEUR_IMAGE
    ratio = max_width / img.width
    new_size = (max_width, int(img.height * ratio))

    img = img.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    label_image = tk.Label(frame_right, image=img_tk, bg=FOND)
    label_image.pack(fill="both", expand=True)

except Exception as e:
    tk.Label(frame_right, text="Aucune image (image.png) trouvée",
             bg=FOND, fg=TEXTE, font=("Arial", 16)).pack(pady=20)

appliquer_theme(fenetre)
fenetre.mainloop()
