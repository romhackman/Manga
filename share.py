import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import urllib.parse

# ----------------- Thème -----------------
FOND = "#fbbeaf"
BLEU = "#007ACC"
ROUGE = "#D43F3A"
GRIS = "#E0CFC7"
ENTREE_BG = "#F5D1C1"
TEXTE = "#000000"
BOUTON_BG = "#E6A38C"

chapitres = []

# ----------------- Fonctions -----------------
def creer_lien_anime(titre):
    titre = titre.lower().strip()
    remplacants = {"é":"e","è":"e","ê":"e","ë":"e","à":"a","â":"a",
                   "î":"i","ï":"i","ô":"o","ö":"o","ù":"u","û":"u","ü":"u","'":""}
    for k,v in remplacants.items():
        titre = titre.replace(k,v)
    titre = titre.replace("  "," ").replace(" ","-")
    return f"https://anime-sama.eu/catalogue/{titre}/scan/vf/"

def maj_liste_chapitres():
    liste.delete(0, tk.END)
    for chap in sorted(chapitres):
        liste.insert(tk.END, f"Chapitre {chap}")

def ajouter_chapitres_depuis_entry(event=None):
    """Récupère le texte de l'Entry, sépare les chapitres et ajoute à la liste"""
    texte = entree_chapitres.get().strip()
    if not texte:
        return
    # Séparer par virgules ou espaces
    for part in texte.replace(',', ' ').split():
        try:
            numero = int(part)
            if numero > 0 and numero not in chapitres:
                chapitres.append(numero)
        except:
            continue
    maj_liste_chapitres()
    entree_chapitres.delete(0, tk.END)  # vide l'entry après ajout

def trouver_pages_tous():
    titre = entree_titre.get().strip()
    if not titre:
        messagebox.showerror("Erreur", "Entrez le nom de l'anime.")
        return
    if not chapitres:
        messagebox.showerror("Erreur", "Ajoutez au moins un chapitre.")
        return

    titre_url = urllib.parse.quote(titre)  # encode les espaces et apostrophes
    resultats = ""

    for chapitre in sorted(chapitres):
        nb_pages = 0
        while True:
            url_img = f"https://anime-sama.eu/s2/scans/{titre_url}/{chapitre}/{nb_pages+1}.jpg"
            try:
                r = requests.head(url_img, headers={"User-Agent": "Mozilla/5.0"})
            except:
                break
            if r.status_code == 200:
                nb_pages += 1
            else:
                break
        resultats += f"Chapitre {chapitre} : {nb_pages} pages\n"

    messagebox.showinfo("Nombre de pages", resultats)

def ouvrir_lien():
    import webbrowser
    titre = entree_titre.get().strip()
    if not titre:
        messagebox.showerror("Erreur", "Entrez d'abord un anime.")
        return
    webbrowser.open(creer_lien_anime(titre))

# ----------------- Interface -----------------
fenetre = tk.Tk()
fenetre.title("ANIME – Page Finder")
fenetre.geometry("900x600")
fenetre.configure(bg=FOND)


tk.Label(fenetre, text="Anime Page Finder", bg=FOND, fg=TEXTE, font=("Arial",20,"bold")).pack(pady=10)

frame_gauche = tk.Frame(fenetre, bg=FOND)
frame_gauche.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Nom de l'anime
tk.Label(frame_gauche, text="Nom de l'anime :", bg=FOND, fg=TEXTE, font=("Arial",14,"bold")).pack()
entree_titre = tk.Entry(frame_gauche, width=30, bg=ENTREE_BG, fg=TEXTE, font=("Arial",12))
entree_titre.pack(pady=10)

tk.Button(frame_gauche, text="Ouvrir le lien Anime-sama", command=ouvrir_lien,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial",12)).pack(pady=10)

# Ajouter plusieurs chapitres
tk.Label(frame_gauche, text="Chapitres (séparés par , ou espace) :",
         bg=FOND, fg=TEXTE, font=("Arial",12,"bold")).pack(pady=5)

entree_chapitres = tk.Entry(frame_gauche, width=30, bg=ENTREE_BG, fg=TEXTE, font=("Arial",12))
entree_chapitres.pack(pady=5)
entree_chapitres.bind("<Return>", ajouter_chapitres_depuis_entry)  # Entrée clavier

tk.Button(frame_gauche, text="Ajouter les chapitres",
          command=ajouter_chapitres_depuis_entry,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial",12)).pack(pady=5)

# Liste des chapitres
tk.Label(frame_gauche, text="Chapitres ajoutés :", bg=FOND, fg=TEXTE, font=("Arial",14,"bold")).pack(pady=10)
liste = tk.Listbox(frame_gauche, width=30, height=10, font=("Arial",12))
liste.pack()

# Bouton compter les pages
tk.Button(frame_gauche, text="Trouver le nombre de pages (tous)", command=trouver_pages_tous,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial",14,"bold")).pack(pady=15)

# Image/logo
frame_image = tk.Frame(fenetre, bg=FOND)
frame_image.pack(side="right", padx=10)
try:
    image_orig = Image.open("image.png")
    image_tk = ImageTk.PhotoImage(image_orig.resize((400,580)))
    tk.Label(frame_image, image=image_tk, bg=FOND).pack()
except:
    tk.Label(frame_image, text="(Aucune image)", font=("Arial",14), bg=FOND).pack()

fenetre.mainloop()
