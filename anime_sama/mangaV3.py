import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk

# ----------------- Thème sombre -----------------
FOND = "#040404"
BLEU = "#007ACC"
ROUGE = "#D43F3A"
GRIS = "#222222"
ENTREE_BG = "#222222"
TEXTE = "#FFFFFF"
BOUTON_BG = "#333333"

dossier_principal = ""

# ----------------- Fonctions -----------------
def appliquer_theme(widget):
    """Applique les couleurs à tous les widgets."""
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

def choisir_dossier():
    global dossier_principal
    dossier = filedialog.askdirectory(title="Choisir le dossier principal pour enregistrer le manga")
    if dossier:
        dossier_principal = dossier
        texte_dossier.set(f"Dossier sélectionné : {dossier_principal}")

# ----------------- Pop-up pour pages -----------------
def demander_pages_pour_chapitres(liste_chapitres):
    fen = tk.Toplevel(fenetre)
    fen.title("Pages par chapitre")
    fen.configure(bg=FOND)

    tk.Label(fen, text="Entrer le nombre de pages pour chaque chapitre :",
             bg=FOND, fg=TEXTE, font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(fen, bg=FOND)
    frame.pack(pady=10, padx=10)

    champs = {}
    for chap in liste_chapitres:
        ligne = tk.Frame(frame, bg=FOND)
        ligne.pack(fill="x", pady=5)
        tk.Label(ligne, text=f"Chapitre {chap} :", bg=FOND, fg=TEXTE,
                 font=("Arial", 12)).pack(side="left")
        entry = tk.Entry(ligne, width=10, bg=ENTREE_BG, fg=TEXTE,
                          insertbackground=TEXTE, font=("Arial", 12))
        entry.pack(side="right", padx=5)
        champs[chap] = entry

    result = {}
    def valider():
        for chap in liste_chapitres:
            try:
                val = int(champs[chap].get())
                if val <= 0:
                    raise ValueError
                result[chap] = val
            except:
                messagebox.showerror("Erreur", f"Valeur invalide pour le chapitre {chap}.")
                return
        fen.destroy()

    tk.Button(fen, text="Valider", command=valider,
              bg=BOUTON_BG, fg=TEXTE, font=("Arial", 12)).pack(pady=10)
    fen.grab_set()
    fen.wait_window()
    return result

# ----------------- Téléchargement -----------------
def telecharger_chapitre(url_base, nb_pages, dossier_chapitre, compteur_total, total_pages):
    if not os.path.exists(dossier_chapitre):
        os.makedirs(dossier_chapitre)

    for numero in range(1, nb_pages + 1):
        url_image = url_base.replace("NUM", str(numero))
        nom_fichier = os.path.join(dossier_chapitre, f"page_{numero}.jpg")
        try:
            texte_status.set(f"Téléchargement : {os.path.basename(dossier_chapitre)} page {numero}/{nb_pages}")
            fenetre.update()
            data = requests.get(url_image, headers={"User-Agent": "Mozilla/5.0"}).content
            with open(nom_fichier, "wb") as f:
                f.write(data)
            compteur_total[0] += 1
            progress = (compteur_total[0] / total_pages) * 100
            barre_progression['value'] = progress
            fenetre.update()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de télécharger : {url_image}\n{e}")
            return

def telecharger_manga():
    global dossier_principal
    url_base = entree_url.get().strip()
    titre_manga = entree_titre.get().strip()

    if not titre_manga:
        messagebox.showerror("Erreur", "Vous devez donner un titre pour le manga.")
        return
    if not dossier_principal:
        messagebox.showerror("Erreur", "Vous devez sélectionner un dossier principal.")
        return
    if "NUM" not in url_base or "CHAP" not in url_base:
        messagebox.showerror("Erreur", "Le lien doit contenir 'CHAP' et 'NUM'.")
        return

    dossier_manga = os.path.join(dossier_principal, titre_manga)
    if not os.path.exists(dossier_manga):
        os.makedirs(dossier_manga)

    choix = messagebox.askquestion(
        "Méthode",
        "Voulez-vous définir un intervalle ?\n\n"
        "- OUI : début → fin\n"
        "- NON : début + quantité"
    )

    if choix == "yes":
        chapitre_debut = simpledialog.askinteger("Début", "Chapitre de début :")
        chapitre_fin = simpledialog.askinteger("Fin", "Chapitre de fin :")
        if not chapitre_debut or not chapitre_fin or chapitre_fin < chapitre_debut:
            messagebox.showerror("Erreur", "Intervalle invalide.")
            return
        liste_chapitres = list(range(chapitre_debut, chapitre_fin + 1))
    else:
        chapitre_debut = simpledialog.askinteger("Début", "Chapitre de départ :")
        quantite = simpledialog.askinteger("Quantité", "Nombre de chapitres :")
        if not chapitre_debut or not quantite:
            messagebox.showerror("Erreur", "Valeurs invalides.")
            return
        liste_chapitres = list(range(chapitre_debut, chapitre_debut + quantite))

    pages_par_chapitre = demander_pages_pour_chapitres(liste_chapitres)
    if not pages_par_chapitre:
        return

    total_pages = sum(pages_par_chapitre.values())
    compteur_total = [0]

    for chapitre in liste_chapitres:
        texte_status.set(f"Téléchargement : Chapitre {chapitre}")
        fenetre.update()
        dossier_chapitre = os.path.join(dossier_manga, f"Chapitre_{chapitre}")
        url_chapitre = url_base.replace("CHAP", str(chapitre))
        telecharger_chapitre(url_chapitre, pages_par_chapitre[chapitre],
                             dossier_chapitre, compteur_total, total_pages)

    messagebox.showinfo("Terminé", "Tous les chapitres ont été téléchargés !")
    texte_status.set("Téléchargement terminé.")
    barre_progression['value'] = 0

# ----------------- Interface principale -----------------
fenetre = tk.Tk()
fenetre.title("MANGA DOWNLOADER")

HAUTEUR_IMAGE = 600
LARGEUR_FORMULAIRE = 400
LARGEUR_IMAGE = 600
fenetre.geometry(f"{LARGEUR_FORMULAIRE + LARGEUR_IMAGE}x{HAUTEUR_IMAGE}")
fenetre.configure(bg=FOND)

frame_gauche = tk.Frame(fenetre, bg=FOND, width=LARGEUR_FORMULAIRE, height=HAUTEUR_IMAGE)
frame_gauche.pack(side="left", fill="y", padx=10, pady=10)

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar",
                troughcolor=GRIS,
                background=BLEU,
                bordercolor=FOND)

# -- Widgets --
tk.Label(frame_gauche, text="Titre du manga :", bg=FOND, fg=TEXTE, font=("Arial", 14, "bold")).pack(pady=10)
entree_titre = tk.Entry(frame_gauche, width=40, bg=ENTREE_BG, fg=TEXTE, insertbackground=TEXTE, font=("Arial", 12))
entree_titre.pack(pady=5)

tk.Label(frame_gauche, text="Lien modèle (CHAP / NUM) :", bg=FOND, fg=TEXTE, font=("Arial", 14, "bold")).pack(pady=10)
entree_url = tk.Entry(frame_gauche, width=40, bg=ENTREE_BG, fg=TEXTE, insertbackground=TEXTE, font=("Arial", 12))
entree_url.pack(pady=5)

tk.Button(frame_gauche, text="Choisir le dossier principal", command=choisir_dossier,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial", 12)).pack(pady=15)

texte_dossier = tk.StringVar()
texte_dossier.set("Aucun dossier sélectionné")
tk.Label(frame_gauche, textvariable=texte_dossier, bg=FOND, fg=TEXTE, font=("Arial", 12)).pack(pady=5)

barre_progression = ttk.Progressbar(
    frame_gauche, orient="horizontal", length=350, mode="determinate", style="TProgressbar")
barre_progression.pack(pady=15)

tk.Button(frame_gauche, text="Télécharger le manga", command=telecharger_manga,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial", 12)).pack(pady=15)

texte_status = tk.StringVar()
texte_status.set("En attente…")
tk.Label(frame_gauche, textvariable=texte_status, bg=FOND, fg=TEXTE, font=("Arial", 12)).pack(pady=5)

# -- Image manga --
dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_image = os.path.join(dossier_script, "image.png")  # image dans le même dossier que le script

try:
    image_orig = Image.open(chemin_image)
    image_orig = image_orig.resize((LARGEUR_IMAGE, HAUTEUR_IMAGE), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(image_orig)
    label_image = tk.Label(fenetre, image=image_tk, bg=FOND)
    label_image.image = image_tk  # <-- important pour conserver la référence
    label_image.pack(side="right", fill="y")
except Exception as e:
    tk.Label(fenetre, text=f"(Aucune image)\nErreur : {e}", bg=FOND, fg=TEXTE, font=("Arial", 14)).pack(side="right", fill="y")

appliquer_theme(fenetre)
fenetre.mainloop()
