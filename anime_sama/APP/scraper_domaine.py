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
# 2️⃣ Fonction principale
# --------------------------------------
def get_anime_sama_extension():
    base_url = "https://anime-sama.pw"

    try:
        print("Connexion au site principal...")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("❌ Erreur lors de la connexion :", e)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche du bouton
    link = soup.find("a", class_="btn-primary", string="Accéder à Anime-Sama")

    if not link:
        link = soup.find("a", class_="btn-primary")

    if not link:
        print("❌ Lien non trouvé dans le HTML.")
        return None

    href = link.get("href")
    if not href:
        print("❌ Le lien trouvé ne contient pas de href.")
        return None

    print("Lien trouvé :", href)

    # --------------------------------------
    # 3️⃣ Suivre la redirection
    # --------------------------------------
    try:
        final_response = requests.get(href, allow_redirects=True, timeout=10)
        final_response.raise_for_status()
    except requests.RequestException as e:
        print("❌ Erreur lors du suivi de redirection :", e)
        return None

    final_url = final_response.url
    print("URL finale après redirection :", final_url)

    # --------------------------------------
    # 4️⃣ Extraction du domaine
    # --------------------------------------
    parsed = urlparse(final_url)
    hostname = parsed.hostname

    if not hostname:
        print("❌ Impossible d'extraire le hostname.")
        return None

    if "anime-sama" not in hostname:
        print("⚠️ Domaine inattendu :", hostname)
        return None

    domaine_extension = hostname.split(".")[-1]
    print("Extension extraite :", domaine_extension)

    return domaine_extension


# --------------------------------------
# 5️⃣ Exécution
# --------------------------------------
extension = get_anime_sama_extension()

if extension:
    data = {"domaine": extension}

    try:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Extension enregistrée dans {json_file}")
    except IOError as e:
        print("❌ Erreur lors de l'écriture du fichier JSON :", e)
else:
    print("❌ Aucune extension récupérée.")
