import requests

BASE = "https://api.mangadex.org"

def search(title):
    """Recherche un manga par titre (max 5 résultats)"""
    r = requests.get(f"{BASE}/manga", params={"title": title, "limit": 5})
    r.raise_for_status()
    return r.json()["data"]

def chapters(manga_id, lang="fr"):
    """Liste des chapitres d'un manga"""
    r = requests.get(f"{BASE}/chapter", params={
        "manga": manga_id,
        "translatedLanguage[]": [lang],
        "order[chapter]": "asc",
        "limit": 10
    })
    r.raise_for_status()
    return r.json()["data"]

def pages(chapter_id):
    """Récupère les pages d'un chapitre"""
    r = requests.get(f"{BASE}/at-home/server/{chapter_id}")
    r.raise_for_status()
    return r.json()
