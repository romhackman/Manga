import tkinter as tk
from tkinter import ttk
import threading
import requests
from bs4 import BeautifulSoup
import os
import json

# Chemin du dossier où est le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin correct vers le JSON
json_path = os.path.join(script_dir, "..", "ND_anime_sama", "domaine.json")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        DOMAINE = data.get("domaine", "tv")
except Exception as e:
    print(f"[ERROR] Impossible de lire le JSON : {e}")
    DOMAINE = "tv"

print("Domaine utilisé :", DOMAINE)



URL_HOME = f"https://anime-sama.{DOMAINE}/"
URL_SEARCH = f"https://anime-sama.{DOMAINE}/template-php/defaut/fetch.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": URL_HOME,
    "Referer": URL_HOME
}

session = requests.Session()
try:
    session.get(URL_HOME, headers=HEADERS)
except Exception as e:
    print(f"[ERROR] Impossible de se connecter à {URL_HOME} : {e}")

# ----------------- Fonctions -----------------
def fetch_anime_search(query):
    """Recherche les titres sur Anime-sama et retourne une liste de tuples (titre, lien)"""
    if not query:
        return []

    try:
        r = session.post(URL_SEARCH, data={"query": query}, headers=HEADERS, timeout=5)
        r.raise_for_status()
        results_list = []

        # Essayer JSON d'abord
        try:
            results = r.json()
            for item in results.get("results", []):
                titre = item.get("title") or item.get("name")
                lien = item.get("url")
                if titre and lien:
                    results_list.append((titre, lien))
        except Exception:
            # fallback HTML
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select("a.asn-search-result"):
                titre = a.select_one(".asn-search-result-title").get_text(strip=True)
                lien = a.get("href")
                results_list.append((titre, lien))

        return results_list

    except Exception as e:
        print(f"[ERROR] Recherche échouée : {e}")
        return []

def update_results(event=None):
    query = entry_search.get().strip()
    listbox_results.delete(0, tk.END)

    if not query:
        return

    def worker():
        results = fetch_anime_search(query)
        listbox_results.delete(0, tk.END)
        print(f"\n[LOG] {len(results)} résultats pour '{query}':")
        for titre, lien in results:
            listbox_results.insert(tk.END, titre)
            print(f"{titre} → {lien}")

    threading.Thread(target=worker, daemon=True).start()

# ----------------- Interface -----------------
root = tk.Tk()
root.title("Anime-sama Finder (Temps réel + Liens)")
root.geometry("500x400")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(frame, text="Rechercher un anime :", font=("Segoe UI", 12)).pack(anchor="w")
entry_search = tk.Entry(frame, font=("Segoe UI", 12))
entry_search.pack(fill="x")
entry_search.bind("<KeyRelease>", update_results)

listbox_results = tk.Listbox(frame, font=("Segoe UI", 11))
listbox_results.pack(fill="both", expand=True, pady=10)

root.mainloop()
