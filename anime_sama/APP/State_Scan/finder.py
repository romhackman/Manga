import tkinter as tk
from tkinter import messagebox
import threading, re, unicodedata, os, json, requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "genres_count.json")

# JSON initialization
if not os.path.exists(json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"genres": {}, "animes": []}, f, ensure_ascii=False, indent=4)

with open(json_path, "r", encoding="utf-8") as f:
    try:
        genres_data = json.load(f)
        if "genres" not in genres_data: genres_data["genres"] = {}
        if "animes" not in genres_data: genres_data["animes"] = []
    except json.JSONDecodeError:
        genres_data = {"genres": {}, "animes": []}

# Session requests
DOMAINE = "si"
URL_HOME = f"https://anime-sama.{DOMAINE}/"
URL_SEARCH = f"https://anime-sama.{DOMAINE}/template-php/defaut/fetch.php"
headers_search = {"User-Agent":"Mozilla/5.0","X-Requested-With":"XMLHttpRequest",
                  "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": URL_HOME,"Referer": URL_HOME}
session = requests.Session()
session.get(URL_HOME, headers=headers_search)
search_results = []

# ================= Fonctions =================
def nettoyer_nom(nom):
    nom_sans_accents = unicodedata.normalize('NFKD', nom).encode('ASCII','ignore').decode('utf-8')
    nom_avec_tirets = nom_sans_accents.strip().replace(" ","-")
    return re.sub(r'[^a-zA-Z0-9\-]', '', nom_avec_tirets).lower()

def creer_lien_genres(nom):
    return f"https://anime-sama.si/catalogue/{nettoyer_nom(nom)}/"

def setup_finder_tab(tabs, FOND, ENTREE_BG, TEXTE, BLEU, BOUTON_BG):
    global entree_titre, listbox_search, listbox_genres, genres_data
    
    finder = tk.Frame(tabs, bg=FOND)
    tabs.add(finder, text="🔍 Finder")

    tk.Label(finder, text="🔍 Recherche anime :", bg=FOND, fg=TEXTE, font=("Segoe UI",10,"bold")).pack(anchor="w", padx=10, pady=(10,2))
    entree_titre = tk.Entry(finder, bg=ENTREE_BG, fg=TEXTE, insertbackground=TEXTE, relief="flat", font=("Segoe UI",11))
    entree_titre.pack(fill="x", padx=10)

    listbox_search = tk.Listbox(finder, bg=ENTREE_BG, fg=TEXTE, selectbackground=BLEU, selectforeground=TEXTE,
                                relief="flat", height=5, highlightthickness=0, font=("Segoe UI",10))
    listbox_search.pack(fill="x", padx=10, pady=(2,5))

    tk.Label(finder, text="Genres :", bg=FOND, fg=TEXTE, font=("Segoe UI",10,"bold")).pack(anchor="w", padx=10, pady=(10,2))
    listbox_genres = tk.Listbox(finder, bg=ENTREE_BG, fg=TEXTE, height=6)
    listbox_genres.pack(fill="x", padx=10, pady=(0,5))

    tk.Button(finder, text="Récupérer genres", command=lambda: recuperer_genres_interface(), bg=BOUTON_BG, fg=TEXTE).pack(pady=5)

    # ================= Événements =================
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
        except: pass

    def on_titre_keyrelease(event):
        threading.Thread(target=fetch_anime_search, args=(entree_titre.get().strip(),), daemon=True).start()

    def on_select_anime(event):
        if listbox_search.curselection():
            titre = search_results[listbox_search.curselection()[0]]
            entree_titre.delete(0, tk.END)
            entree_titre.insert(0, titre)
            listbox_search.delete(0, tk.END)

    def recuperer_genres_interface():
        titre = entree_titre.get().strip()
        if not titre:
            messagebox.showerror("Erreur", "Veuillez entrer un titre d'anime")
            return
        if titre in genres_data["animes"]:
            messagebox.showinfo("Info", "Cet anime a déjà été ajouté")
            return
        url = creer_lien_genres(titre)
        try:
            r = requests.get(url)
            if r.status_code != 200:
                messagebox.showerror("Erreur", "Page introuvable")
                return
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text,"html.parser")
            section_genres = soup.find('h2', string=re.compile("Genres", re.I))
            if not section_genres:
                messagebox.showinfo("Info", "Aucun genre trouvé")
                return
            genres_tag = section_genres.find_next_sibling('a')
            if not genres_tag:
                messagebox.showinfo("Info", "Aucun genre trouvé")
                return
            genres = [g.strip().lower() for g in genres_tag.text.split(',')]
            listbox_genres.delete(0, tk.END)
            for g in genres:
                listbox_genres.insert(tk.END, g)
                if g in genres_data["genres"]:
                    genres_data["genres"][g] = str(int(genres_data["genres"][g]) + 1)
                else:
                    genres_data["genres"][g] = "1"
            genres_data["animes"].append(titre)
            with open(json_path,"w",encoding="utf-8") as f:
                json.dump(genres_data,f,ensure_ascii=False, indent=4)
            messagebox.showinfo("Succès","Genres récupérés et mis à jour dans JSON")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les genres : {e}")

    entree_titre.bind("<KeyRelease>", on_titre_keyrelease)
    listbox_search.bind("<<ListboxSelect>>", on_select_anime)
