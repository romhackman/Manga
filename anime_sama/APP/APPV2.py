import os
import requests
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------- Thème sombre -----------------
FOND = "#040404"
BLEU = "#007ACC"
ROUGE = "#D43F3A"
GRIS = "#222222"
ENTREE_BG = "#222222"
TEXTE = "#FFFFFF"
BOUTON_BG = "#333333"

# ----------------- Données globales -----------------
chapitres = []
pages_trouvees = {}
titre_anime = ""
dossier_temp = None
MAX_PAGES_POSSIBLE = 1000  # Pour recherche binaire
THREADS = 10

# ----------------- FINDER -----------------
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
    texte = entree_chapitres.get().strip()
    if not texte:
        return
    for part in texte.replace(",", " ").split():
        try:
            numero = int(part)
            if numero > 0 and numero not in chapitres:
                chapitres.append(numero)
        except:
            continue
    maj_liste_chapitres()
    entree_chapitres.delete(0, tk.END)

# ----------------- RECHERCHE OPTIMISÉE -----------------
def page_existe(titre_url, chapitre, page):
    url_img = f"https://anime-sama.eu/s2/scans/{titre_url}/{chapitre}/{page}.jpg"
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
    if dossier_temp:
        with open(os.path.join(dossier_temp, f"Chapitre_{chapitre}.txt"), "w") as f:
            f.write(f"{last_valid} pages")
    return chapitre, last_valid

def trouver_pages_tous():
    global pages_trouvees, titre_anime, dossier_temp
    titre = entree_titre.get().strip()
    if not titre:
        messagebox.showerror("Erreur", "Entrez le nom de l'anime.")
        return
    if not chapitres:
        messagebox.showerror("Erreur", "Ajoutez au moins un chapitre.")
        return

    titre_anime = titre
    pages_trouvees = {}

    dossier_temp = f"{titre_anime}_Temp"
    os.makedirs(dossier_temp, exist_ok=True)

    titre_url = urllib.parse.quote(titre)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(compter_pages_chapitre_binaire, titre_url, chap): chap for chap in chapitres}
        for future in as_completed(futures):
            chap, nb = future.result()
            pages_trouvees[chap] = nb

    afficher_resultats()
    remplir_downloader()
    resultats_str = "\n".join([f"Chapitre {chap} : {nb} pages" for chap, nb in sorted(pages_trouvees.items())])
    messagebox.showinfo("Nombre de pages", resultats_str)

def afficher_resultats():
    box_result.delete(0, tk.END)
    for chap, pages in sorted(pages_trouvees.items()):
        box_result.insert(tk.END, f"Chapitre {chap} : {pages} pages")

# ----------------- DOWNLOADER -----------------
def remplir_downloader():
    entry_titre_dl.delete(0, tk.END)
    entry_titre_dl.insert(0, titre_anime)

    entry_url_dl.delete(0, tk.END)
    entry_url_dl.insert(0, f"https://anime-sama.eu/s2/scans/{urllib.parse.quote(titre_anime)}/CHAP/NUM.jpg")

    box_dl.delete(0, tk.END)
    for chap, pages in sorted(pages_trouvees.items()):
        box_dl.insert(tk.END, f"Chapitre {chap} ({pages} pages)")

def choisir_dossier():
    dossier = filedialog.askdirectory()
    if dossier:
        dossier_destination.set(dossier)

def telecharger():
    if not pages_trouvees:
        messagebox.showerror("Erreur", "Aucune donnée Finder.")
        return
    dossier = dossier_destination.get()
    if not dossier:
        messagebox.showerror("Erreur", "Choisissez un dossier.")
        return

    base = entry_url_dl.get()
    total = sum(pages_trouvees.values())
    fait = 0

    dossier_manga = os.path.join(dossier, titre_anime)
    os.makedirs(dossier_manga, exist_ok=True)

    for chap, pages in sorted(pages_trouvees.items()):
        dossier_chap = os.path.join(dossier_manga, f"Chapitre_{chap}")
        os.makedirs(dossier_chap, exist_ok=True)
        for i in range(1, pages + 1):
            url = base.replace("CHAP", str(chap)).replace("NUM", str(i))
            try:
                data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).content
            except:
                continue
            with open(os.path.join(dossier_chap, f"page_{i}.jpg"), "wb") as f:
                f.write(data)
            fait += 1
            progress['value'] = (fait / total) * 100
            fenetre.update()

    messagebox.showinfo("Terminé", "Téléchargement terminé.")
    progress['value'] = 0

# ----------------- SUPPRESSION DOSSIER -----------------
def supprimer_dossier():
    global dossier_temp
    if dossier_temp and os.path.exists(dossier_temp):
        if messagebox.askyesno("Supprimer dossier ?", f"Supprimer '{dossier_temp}' ?"):
            import shutil
            shutil.rmtree(dossier_temp)
            messagebox.showinfo("Supprimé", f"Dossier '{dossier_temp}' supprimé.")
            dossier_temp = None
    else:
        messagebox.showwarning("Aucun dossier", "Aucun dossier temporaire trouvé.")

# ----------------- INTERFACE -----------------
fenetre = tk.Tk()
fenetre.title("Anime-sama Finder & Downloader")
fenetre.geometry("1100x650")
fenetre.configure(bg=FOND)

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background=FOND, borderwidth=0)
style.configure("TNotebook.Tab", background=BOUTON_BG, foreground=TEXTE)
style.map("TNotebook.Tab", background=[("selected", BLEU)])

tabs = ttk.Notebook(fenetre)
tabs.pack(fill="both", expand=True)

# ===== ONGLET FINDER =====
finder = tk.Frame(tabs, bg=FOND)
tabs.add(finder, text="🔍 Finder")

tk.Label(finder, text="Nom de l'anime :", bg=FOND, fg=TEXTE).pack(pady=5)
entree_titre = tk.Entry(finder, width=30, bg=ENTREE_BG, fg=TEXTE)
entree_titre.pack()

tk.Label(finder, text="Chapitres (séparés par espace ou ,) :", bg=FOND, fg=TEXTE).pack(pady=5)
entree_chapitres = tk.Entry(finder, width=30, bg=ENTREE_BG, fg=TEXTE)
entree_chapitres.pack()
entree_chapitres.bind("<Return>", ajouter_chapitres_depuis_entry)

tk.Button(finder, text="Ajouter chapitres", command=ajouter_chapitres_depuis_entry, bg=BOUTON_BG, fg=TEXTE).pack(pady=5)
liste = tk.Listbox(finder, width=30, height=8, bg=ENTREE_BG, fg=TEXTE)
liste.pack(pady=5)
tk.Button(finder, text="Trouver le nombre de pages", command=trouver_pages_tous, bg=BOUTON_BG, fg=TEXTE).pack(pady=10)
box_result = tk.Listbox(finder, width=40, height=10, bg=ENTREE_BG, fg=TEXTE)
box_result.pack(pady=5)
tk.Button(finder, text="Supprimer dossier temporaire", command=supprimer_dossier, bg=ROUGE, fg=TEXTE).pack(pady=10)

# ===== ONGLET DOWNLOADER =====
downloader = tk.Frame(tabs, bg=FOND)
tabs.add(downloader, text="⬇ Downloader")

tk.Label(downloader, text="Titre :", bg=FOND, fg=TEXTE).pack()
entry_titre_dl = tk.Entry(downloader, width=40, bg=ENTREE_BG, fg=TEXTE)
entry_titre_dl.pack()

tk.Label(downloader, text="URL modèle :", bg=FOND, fg=TEXTE).pack()
entry_url_dl = tk.Entry(downloader, width=60, bg=ENTREE_BG, fg=TEXTE)
entry_url_dl.pack()

box_dl = tk.Listbox(downloader, width=45, height=10, bg=ENTREE_BG, fg=TEXTE)
box_dl.pack(pady=10)

dossier_destination = tk.StringVar()
tk.Button(downloader, text="Choisir dossier", command=choisir_dossier, bg=BOUTON_BG, fg=TEXTE).pack()
tk.Label(downloader, textvariable=dossier_destination, bg=FOND, fg=TEXTE).pack()

progress = ttk.Progressbar(downloader, length=400, mode="determinate")
progress.pack(pady=10)

tk.Button(downloader, text="Télécharger", command=telecharger, bg=BOUTON_BG, fg=TEXTE, font=("Arial",12,"bold")).pack(pady=10)

fenetre.mainloop()
