import os
import re
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# -----------------------------
# UTILITAIRES
# -----------------------------
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def creer_pdf(dossier_chapitre, reverse=False, progress_var=None):
    images = []
    fichiers = sorted(os.listdir(dossier_chapitre), key=natural_sort_key, reverse=reverse)

    total = len([f for f in fichiers if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    compteur = 0

    for fichier in fichiers:
        if fichier.lower().endswith((".jpg", ".jpeg", ".png")):
            chemin = os.path.join(dossier_chapitre, fichier)
            try:
                img = Image.open(chemin).convert('RGB')
            except Exception as e:
                print(f"Erreur ouverture image {chemin}: {e}")
                continue
            images.append(img)
            compteur += 1
            if progress_var:
                progress_var.set(int(compteur / total * 100))
                fenetre.update_idletasks()

    if not images:
        return False, "Aucune image valide"

    nom_chapitre = os.path.basename(dossier_chapitre)
    dossier_parent = os.path.dirname(dossier_chapitre)
    chemin_pdf = os.path.join(dossier_parent, f"{nom_chapitre}.pdf")

    try:
        images[0].save(chemin_pdf, save_all=True, append_images=images[1:])
        return True, chemin_pdf
    except Exception as e:
        return False, str(e)

# -----------------------------
# MODES EXISTANTS
# -----------------------------
def mode_normal():
    dossier_chapitre = filedialog.askdirectory(title="Choisir un dossier de chapitre (images)")
    if not dossier_chapitre:
        return

    progress_var.set(0)
    ok, msg = creer_pdf(dossier_chapitre, reverse=True, progress_var=progress_var)
    progress_var.set(0)
    if ok:
        messagebox.showinfo("Succès", f"PDF créé :\n{msg}")
    else:
        messagebox.showerror("Erreur", msg)

def mode_boost():
    dossier_racine = filedialog.askdirectory(title="Choisir le dossier contenant les chapitres")
    if not dossier_racine:
        return

    sous_dossiers = [os.path.join(dossier_racine, d) for d in os.listdir(dossier_racine)
                     if os.path.isdir(os.path.join(dossier_racine, d))]
    if not sous_dossiers:
        messagebox.showerror("Erreur", "Aucun chapitre trouvé.")
        return

    resultats = []
    for dossier in sorted(sous_dossiers, key=natural_sort_key):
        ok, msg = creer_pdf(dossier, reverse=False, progress_var=None)
        resultats.append(f"{os.path.basename(dossier)} → {'OK' if ok else 'Erreur'} ({msg})")

    progress_var.set(0)
    messagebox.showinfo("Terminé", "\n".join(resultats))

def mode_full_pdf():
    dossier_racine = filedialog.askdirectory(title="Choisir le dossier contenant tous les chapitres")
    if not dossier_racine:
        return

    sous_dossiers = sorted(
        [os.path.join(dossier_racine, d) for d in os.listdir(dossier_racine)
         if os.path.isdir(os.path.join(dossier_racine, d)) and d.lower().startswith("chapitre")],
        key=natural_sort_key
    )

    if not sous_dossiers:
        messagebox.showerror("Erreur", "Aucun chapitre trouvé.")
        return

    fichiers_totaux = []
    for dossier in sous_dossiers:
        fichiers = sorted(
            [f for f in os.listdir(dossier) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
            key=natural_sort_key
        )
        for f in fichiers:
            fichiers_totaux.append(os.path.join(dossier, f))

    if not fichiers_totaux:
        messagebox.showerror("Erreur", "Aucune image trouvée dans les chapitres.")
        return

    total_images = len(fichiers_totaux)
    compteur = 0
    toutes_images = []
    progress_var.set(0)

    for chemin in fichiers_totaux:
        try:
            img = Image.open(chemin).convert("RGB")
            toutes_images.append(img)
        except Exception as e:
            print(f"Erreur ouverture image {chemin}: {e}")
        compteur += 1
        progress_var.set(int(compteur / total_images * 100))
        fenetre.update_idletasks()

    if toutes_images:
        chemin_pdf = os.path.join(dossier_racine, "Tout_les_chapitres.pdf")
        try:
            toutes_images[0].save(chemin_pdf, save_all=True, append_images=toutes_images[1:])
            progress_var.set(0)
            messagebox.showinfo("Succès", f"PDF complet créé :\n{chemin_pdf}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    else:
        progress_var.set(0)
        messagebox.showerror("Erreur", "Aucune image valide pour créer le PDF.")

# -----------------------------
# MODE DOUBLE PAGE MANGA (GAUCHE->DROITE)
# -----------------------------
def mode_double_page():
    dossier = filedialog.askdirectory(title="Choisir un dossier (images)")
    if not dossier:
        return

    fichiers = sorted(os.listdir(dossier), key=natural_sort_key)
    pages = []
    buffer = []

    total = len([f for f in fichiers if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    compteur = 0

    for f in fichiers:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            buffer.append(os.path.join(dossier, f))
        if len(buffer) == 2:
            try:
                img_gauche = Image.open(buffer[0]).convert("RGB")
                img_droite = Image.open(buffer[1]).convert("RGB")
                largeur = img_gauche.width + img_droite.width
                hauteur = max(img_gauche.height, img_droite.height)
                combine = Image.new("RGB", (largeur, hauteur))
                combine.paste(img_gauche, (0, 0))
                combine.paste(img_droite, (img_gauche.width, 0))
                pages.append(combine)
            except Exception as e:
                print(f"Erreur double page {buffer}: {e}")
            buffer = []
            compteur += 2
            progress_var.set(int(compteur / total * 100))
            fenetre.update_idletasks()

    if len(buffer) == 1:
        try:
            pages.append(Image.open(buffer[0]).convert("RGB"))
            compteur += 1
            progress_var.set(int(compteur / total * 100))
        except Exception as e:
            print(f"Erreur dernière image {buffer[0]}: {e}")

    if not pages:
        messagebox.showerror("Erreur", "Aucune image valide trouvée.")
        return

    sortie = os.path.join(os.path.dirname(dossier), f"{os.path.basename(dossier)}_double.pdf")
    pages[0].save(sortie, save_all=True, append_images=pages[1:])
    progress_var.set(0)
    messagebox.showinfo("Succès", f"PDF double pages manga créé :\n{sortie}")

# -----------------------------
# MODE DOUBLE PAGE MANGA DROITE->GAUCHE
# -----------------------------
def mode_double_page_droite_gauche():
    dossier = filedialog.askdirectory(title="Choisir un dossier (images)")
    if not dossier:
        return

    fichiers = sorted(os.listdir(dossier), key=natural_sort_key)
    pages = []
    buffer = []

    total = len([f for f in fichiers if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    compteur = 0

    for f in fichiers:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            buffer.append(os.path.join(dossier, f))
        if len(buffer) == 2:
            try:
                # Inversion pour lecture droite->gauche
                img_droite = Image.open(buffer[0]).convert("RGB")
                img_gauche = Image.open(buffer[1]).convert("RGB")
                largeur = img_gauche.width + img_droite.width
                hauteur = max(img_gauche.height, img_droite.height)
                combine = Image.new("RGB", (largeur, hauteur))
                combine.paste(img_gauche, (0, 0))
                combine.paste(img_droite, (img_gauche.width, 0))
                pages.append(combine)
            except Exception as e:
                print(f"Erreur double page {buffer}: {e}")
            buffer = []
            compteur += 2
            progress_var.set(int(compteur / total * 100))
            fenetre.update_idletasks()

    if len(buffer) == 1:
        try:
            pages.append(Image.open(buffer[0]).convert("RGB"))
            compteur += 1
            progress_var.set(int(compteur / total * 100))
        except Exception as e:
            print(f"Erreur dernière image {buffer[0]}: {e}")

    if not pages:
        messagebox.showerror("Erreur", "Aucune image valide trouvée.")
        return

    sortie = os.path.join(os.path.dirname(dossier), f"{os.path.basename(dossier)}_double_RL.pdf")
    pages[0].save(sortie, save_all=True, append_images=pages[1:])
    progress_var.set(0)
    messagebox.showinfo("Succès", f"PDF double pages droite->gauche créé :\n{sortie}")

# -----------------------------
# INTERFACE
# -----------------------------
fenetre = tk.Tk()
fenetre.title("Créer un PDF style Manga")
fenetre.geometry("500x520")

tk.Label(fenetre, text="Choisissez un mode", font=("Arial", 14, "bold")).pack(pady=15)
tk.Button(fenetre, text="Mode normal : PDF pour 1 chapitre", command=mode_normal).pack(pady=5)
tk.Button(fenetre, text="Mode boosté : PDF pour tous les chapitres", command=mode_boost).pack(pady=5)
tk.Button(fenetre, text="Mode Full PDF : 1 PDF pour tous les chapitres", command=mode_full_pdf).pack(pady=5)

tk.Label(fenetre, text="Mode avancé", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(fenetre, text="Mode double pages (GAUCHE->DROITE)", command=mode_double_page).pack(pady=5)
tk.Button(fenetre, text="Mode double pages (DROITE->GAUCHE)", command=mode_double_page_droite_gauche).pack(pady=5)

# Barre de progression
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(fenetre, maximum=100, variable=progress_var)
progress_bar.pack(pady=20, fill='x', padx=20)

try:
    logo = tk.PhotoImage(file="logo.png")
    fenetre.iconphoto(False, logo)
except:
    pass

fenetre.mainloop()
