import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --------------------------------------
# 1️⃣ Chemins relatifs basés sur le script
# --------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
nd_dir = os.path.join(base_dir, "ND_anime_sama")
json_file = os.path.join(nd_dir, "domaine.json")

os.makedirs(nd_dir, exist_ok=True)

# --------------------------------------
# 2️⃣ Scraper le site
# --------------------------------------
url = "https://anime-sama.pw"
response = requests.get(url)
print("Status code:", response.status_code)

if response.status_code != 200:
    print("Erreur lors du téléchargement de la page.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Cherche le bouton "Accéder à Anime-Sama"
link = soup.find("a", class_="btn-primary", string="Accéder à Anime-Sama")
if not link:
    link = soup.find("a", class_="btn-primary")

if link:
    href = link.get("href")
    print("Lien trouvé :", href)

    # --------------------------------------
    # 3️⃣ Extraction de l'extension du domaine
    # --------------------------------------
    parsed = urlparse(href)
    hostname = parsed.hostname  # ex: 'anime-sama.si' ou 'www.anime-sama.com'
    if hostname:
        domaine_extension = hostname.split(".")[-1]  # prend la dernière partie
        print("Extension extraite :", domaine_extension)

        data = {"domaine": domaine_extension}
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"L'extension du domaine a été enregistrée dans {json_file}")
    else:
        print("Impossible d'extraire le domaine 😕")
else:
    print("Lien non trouvé 😕")
