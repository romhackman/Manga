import os
import requests
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shutil
from PIL import Image
import threading
import re
from bs4 import BeautifulSoup

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
MAX_PAGES_POSSIBLE = 1000
THREADS = 10
search_results = []

# ======================================================
# Domaine
# ======================================================
def load_domaine():
    json_path = os.path.join(os.path.dirname(__file__), "..", "anime_sama", "ND_anime_sama", "domaine.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f).get("domaine", "si")
        except:
            return "si"
    return "si"

DOMAINE = load_domaine()

# ======================================================
# Recherche Anime-sama
# ======================================================
URL_HOME = f"https://anime-sama.{DOMAINE}/"
URL_SEARCH = f"https://anime-sama.{DOMAINE}/template-php/defaut/fetch.php"

headers_search = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": URL_HOME,
    "Referer": URL_HOME
}

session = requests.Session()
session.get(URL_HOME, headers=headers_search)

def fetch_anime_search(query):
    if not query:
        listbox_search.delete(0, tk.END)
        return
    try:
        r = session.post(URL_SEARCH, data={"query": query}, headers=headers_search)
        soup = BeautifulSoup(r.text, "html.parser")

        listbox_search.delete(0, tk.END)
        search_results.clear()

        for a in soup.select("a.asn-search-result"):
            titre = a.select_one(".asn-search-result-title").get_text(strip=True)
            listbox_search.insert(tk.END, titre)
            search_results.append(titre)
    except:
        pass

def on_titre_keyrelease(event):
    threading.Thread(
        target=fetch_anime_search,
        args=(entree_titre.get().strip(),),
        daemon=True
    ).start()

def on_select_anime(event):
    if listbox_search.curselection():
        titre = search_results[listbox_search.curselection()[0]]
        entree_titre.delete(0, tk.END)
        entree_titre.insert(0, titre)
        listbox_search.delete(0, tk.END)

# ======================================================
# FINDER
# ======================================================
def maj_liste_chapitres():
    liste.delete(0, tk.END)
    for chap in sorted(chapitres):
        liste.insert(tk.END, f"Chapitre {chap}")

def ajouter_chapitres_depuis_entry(event=None):
    for part in entree_chapitres.get().replace(",", " ").split():
        if part.isdigit() and int(part) not in chapitres:
            chapitres.append(int(part))
    entree_chapitres.delete(0, tk.END)
    maj_liste_chapitres()

def page_existe(titre_url, chapitre, page):
    url = f"https://anime-sama.{DOMAINE}/s2/scans/{titre_url}/{chapitre}/{page}.jpg"
    try:
        return requests.head(url, timeout=3).status_code == 200
    except:
        return False

def compter_pages_chapitre_binaire(titre_url, chapitre):
    low, high = 1, MAX_PAGES_POSSIBLE
    last = 0
    while low <= high:
        mid = (low + high) // 2
        if page_existe(titre_url, chapitre, mid):
            last = mid
            low = mid + 1
        else:
            high = mid - 1
    return chapitre, last

def trouver_pages_tous():
    global pages_trouvees, titre_anime
    titre_anime = entree_titre.get().strip()
    if not titre_anime or not chapitres:
        messagebox.showerror("Erreur", "Titre ou chapitres manquants")
        return

    pages_trouvees = {}
    titre_url = urllib.parse.quote(titre_anime)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(compter_pages_chapitre_binaire, titre_url, c) for c in chapitres]
        for f in as_completed(futures):
            c, p = f.result()
            pages_trouvees[c] = p

    afficher_resultats()
    remplir_downloader()

def afficher_resultats():
    box_result.delete(0, tk.END)
    for c, p in sorted(pages_trouvees.items()):
        box_result.insert(tk.END, f"Chapitre {c} : {p} pages")

# ======================================================
# DOWNLOADER
# ======================================================
def remplir_downloader():
    entry_titre_dl.delete(0, tk.END)
    entry_titre_dl.insert(0, titre_anime)

    entry_url_dl.delete(0, tk.END)
    entry_url_dl.insert(0, f"https://anime-sama.{DOMAINE}/s2/scans/{urllib.parse.quote(titre_anime)}/CHAP/NUM.jpg")

    box_dl.delete(0, tk.END)
    for chap, pages in sorted(pages_trouvees.items()):
        box_dl.insert(tk.END, f"Chapitre {chap} ({pages} pages)")

def choisir_dossier():
    dossier = filedialog.askdirectory()
    if dossier:
        dossier_destination.set(dossier)

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def creer_pdf_boost(dossier_racine):
    sous_dossiers = [os.path.join(dossier_racine, d) for d in os.listdir(dossier_racine)
                     if os.path.isdir(os.path.join(dossier_racine, d))]
    if not sous_dossiers:
        messagebox.showerror("Erreur", "Aucun chapitre trouvé pour créer les PDF.")
        return

    resultats = []
    for dossier in sorted(sous_dossiers, key=natural_sort_key):
        fichiers = sorted([f for f in os.listdir(dossier) if f.lower().endswith((".jpg",".jpeg",".png"))],
                          key=natural_sort_key)
        images = []
        for f in fichiers:
            try:
                img = Image.open(os.path.join(dossier, f)).convert("RGB")
                images.append(img)
            except Exception as e:
                print(f"Erreur ouverture image {f} : {e}")
                continue
        if images:
            chemin_pdf = os.path.join(dossier_racine, f"{os.path.basename(dossier)}.pdf")
            try:
                images[0].save(chemin_pdf, save_all=True, append_images=images[1:])
                resultats.append(f"{os.path.basename(dossier)} → OK ({chemin_pdf})")
            except Exception as e:
                resultats.append(f"{os.path.basename(dossier)} → Erreur ({e})")
        else:
            resultats.append(f"{os.path.basename(dossier)} → Aucune image")

    messagebox.showinfo("PDF Boost terminé", "\n".join(resultats))

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

    progress['value'] = 0
    messagebox.showinfo("Terminé", "Téléchargement terminé.")

    if messagebox.askyesno("Créer PDF", "Voulez-vous créer les PDF avec le mode boosté ?"):
        threading.Thread(target=creer_pdf_boost, args=(dossier_manga,)).start()

def supprimer_dossier():
    global dossier_temp
    if dossier_temp and os.path.exists(dossier_temp):
        if messagebox.askyesno("Supprimer dossier ?", f"Supprimer '{dossier_temp}' ?"):
            shutil.rmtree(dossier_temp)
            messagebox.showinfo("Supprimé", f"Dossier '{dossier_temp}' supprimé.")
            dossier_temp = None
    else:
        messagebox.showwarning("Aucun dossier", "Aucun dossier temporaire trouvé.")

# ======================================================
# INTERFACE
# ======================================================
fenetre = tk.Tk()
fenetre.title("Anime-sama Finder & Downloader")
fenetre.geometry("1100x650")
fenetre.minsize(850, 500)
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

frame_search = tk.Frame(finder, bg=GRIS, highlightbackground=BLEU, highlightthickness=1)
frame_search.pack(padx=15, pady=10, fill="x")

tk.Label(frame_search, text="🔍 Recherche", bg=GRIS, fg=TEXTE, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=8, pady=(6,2))
entree_titre = tk.Entry(frame_search, bg=ENTREE_BG, fg=TEXTE, insertbackground=TEXTE, relief="flat", font=("Segoe UI", 11))
entree_titre.pack(fill="x", padx=8, pady=(0,4))
entree_titre.bind("<KeyRelease>", on_titre_keyrelease)

listbox_search = tk.Listbox(frame_search, bg=ENTREE_BG, fg=TEXTE, selectbackground=BLEU, selectforeground=TEXTE, relief="flat", height=4, highlightthickness=0, font=("Segoe UI", 10))
listbox_search.pack(fill="x", padx=8, pady=(0,6))
listbox_search.bind("<<ListboxSelect>>", on_select_anime)

tk.Label(finder, text="Chapitres :", bg=FOND, fg=TEXTE).pack()
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
