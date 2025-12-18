import os
import zipfile
import requests

def download_chapter(data, out_folder, chapter_num, cbz=True):
    """
    Télécharge un chapitre et crée un CBZ si demandé.
    Renomme chaque chapitre en Chapitre_<num> et chaque page en Page_<num>.jpg
    """
    chapter_folder = os.path.join(out_folder, f"Chapitre_{chapter_num}")
    os.makedirs(chapter_folder, exist_ok=True)

    base = data["baseUrl"]
    hash_ = data["chapter"]["hash"]
    images = data["chapter"]["data"]

    local_files = []
    for i, img in enumerate(images, 1):
        filename = f"Page_{i}.jpg"
        filepath = os.path.join(chapter_folder, filename)
        url = f"{base}/data/{hash_}/{img}"
        r = requests.get(url)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        local_files.append(filepath)
        print(f"✔ Page {i} téléchargée dans {chapter_folder}")

    if cbz:
        cbz_path = chapter_folder + ".cbz"
        with zipfile.ZipFile(cbz_path, "w") as z:
            for f in local_files:
                z.write(f, arcname=os.path.basename(f))
        print(f"📦 CBZ créé : {cbz_path}")
