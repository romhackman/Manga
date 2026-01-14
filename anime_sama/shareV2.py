import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil

# ----------------- Thème sombre -----------------
FOND = "#040404"
TEXTE = "#FFFFFF"
ENTREE_BG = "#222222"
BOUTON_BG = "#333333"
ROUGE = "#D43F3A"

chapitres = []
dossier_temp = None
MAX_PAGES_POSSIBLE = 1000  # pour la recherche binaire

# ----------------- Fonctions -----------------
def creer_lien_anime(titre):
    titre = titre.lower().strip()
    remplacants = {"é":"e","è":"e","ê":"e","ë":"e","à":"a","â":"a",
                   "î":"i","ï":"i","ô":"o","ö":"o","ù":"u","û":"u","ü":"u","'":""}
    for k,v in remplacants.items():
        titre = titre.replace(k,v)
    titre = titre.replace("  "," ").replace(" ","-")
    return f"https://anime-sama.si/catalogue/{titre}/scan/vf/"

def maj_liste_chapitres():
    liste.delete(0, tk.END)
    for chap in sorted(chapitres):
        liste.insert(tk.END, f"Chapitre {chap}")

def ajouter_chapitres_depuis_entry(event=None):
    texte = entree_chapitres.get().strip()
    if not texte:
        return
    for part in texte.replace(',', ' ').split():
        try:
            numero = int(part)
            if numero > 0 and numero not in chapitres:
                chapitres.append(numero)
        except:
            continue
    maj_liste_chapitres()
    entree_chapitres.delete(0, tk.END)

# ----------------- Optimisation recherche binaire -----------------
def page_existe(titre_url, chapitre, page):
    url_img = f"https://anime-sama.si/s2/scans/{titre_url}/{chapitre}/{page}.jpg"
    try:
        r = requests.head(url_img, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        return r.status_code == 200
    except:
        return False

def compter_pages_chapitre_binaire(titre_url, chapitre):
    low, high = 1, MAX_PAGES_POSSIBLE
    last_valid = 0
    while low <= high:
        mid = (low + high) // 2
        if page_existe(titre_url, chapitre, mid):
            last_valid = mid
            low = mid + 1
        else:
            high = mid - 1
    # Sauvegarde dans le dossier temporaire
    if dossier_temp:
        with open(os.path.join(dossier_temp, f"Chapitre_{chapitre}.txt"), "w") as f:
            f.write(f"{last_valid} pages")
    return chapitre, last_valid

def trouver_pages_tous():
    global dossier_temp
    titre = entree_titre.get().strip()
    if not titre:
        messagebox.showerror("Erreur", "Entrez le nom de l'anime.")
        return
    if not chapitres:
        messagebox.showerror("Erreur", "Ajoutez au moins un chapitre.")
        return

    # Création du dossier temporaire
    dossier_temp = f"{titre}_Temp"
    if not os.path.exists(dossier_temp):
        os.makedirs(dossier_temp)

    titre_url = urllib.parse.quote(titre)
    resultats = []

    # Parallélisation par chapitre
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(compter_pages_chapitre_binaire, titre_url, chap): chap for chap in chapitres}
        for future in as_completed(futures):
            chap, nb = future.result()
            resultats.append((chap, nb))

    # Tri et affichage
    resultats.sort(key=lambda x: x[0])
    message = "\n".join([f"Chapitre {chap} : {nb} pages" for chap, nb in resultats])
    messagebox.showinfo("Nombre de pages", message)

def supprimer_dossier():
    global dossier_temp
    if dossier_temp and os.path.exists(dossier_temp):
        if messagebox.askyesno("Supprimer le dossier ?", f"Voulez-vous supprimer le dossier '{dossier_temp}' ?"):
            shutil.rmtree(dossier_temp)
            messagebox.showinfo("Supprimé", f"Dossier '{dossier_temp}' supprimé.")
            dossier_temp = None
    else:
        messagebox.showwarning("Aucun dossier", "Aucun dossier temporaire à supprimer.")

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

tk.Label(frame_gauche, text="Nom de l'anime :", bg=FOND, fg=TEXTE, font=("Arial",14,"bold")).pack()
entree_titre = tk.Entry(frame_gauche, width=30, bg=ENTREE_BG, fg=TEXTE, font=("Arial",12))
entree_titre.pack(pady=10)

tk.Button(frame_gauche, text="Ouvrir le lien Anime-sama", command=ouvrir_lien,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial",12)).pack(pady=10)

tk.Label(frame_gauche, text="Chapitres (séparés par , ou espace) :",
         bg=FOND, fg=TEXTE, font=("Arial",12,"bold")).pack(pady=5)

entree_chapitres = tk.Entry(frame_gauche, width=30, bg=ENTREE_BG, fg=TEXTE, font=("Arial",12))
entree_chapitres.pack(pady=5)
entree_chapitres.bind("<Return>", ajouter_chapitres_depuis_entry)

tk.Button(frame_gauche, text="Ajouter les chapitres",
          command=ajouter_chapitres_depuis_entry,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial",12)).pack(pady=5)

tk.Label(frame_gauche, text="Chapitres ajoutés :", bg=FOND, fg=TEXTE, font=("Arial",14,"bold")).pack(pady=10)
liste = tk.Listbox(frame_gauche, width=30, height=10, font=("Arial",12), bg=ENTREE_BG, fg=TEXTE)
liste.pack()

tk.Button(frame_gauche, text="Trouver le nombre de pages (tous)", command=trouver_pages_tous,
          bg=BOUTON_BG, fg=TEXTE, font=("Arial",14,"bold")).pack(pady=15)

tk.Button(frame_gauche, text="Supprimer le dossier temporaire", command=supprimer_dossier,
          bg=ROUGE, fg=TEXTE, font=("Arial",12,"bold")).pack(pady=10)

frame_image = tk.Frame(fenetre, bg=FOND)
frame_image.pack(side="right", padx=10)

# --- Chargement de l'image depuis le même dossier que le script ---
dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_image = os.path.join(dossier_script, "image.png")

try:
    image_orig = Image.open(chemin_image)
    image_tk = ImageTk.PhotoImage(image_orig.resize((400,580)))
    label_image = tk.Label(frame_image, image=image_tk, bg=FOND)
    label_image.image = image_tk  # garder la référence
    label_image.pack()
except Exception as e:
    tk.Label(frame_image, text=f"(Aucune image)\nErreur : {e}", font=("Arial",14), bg=FOND, fg=TEXTE).pack()

fenetre.mainloop()
