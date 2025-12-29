import os
import time
import threading
import queue
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import pyperclip

# ================= CONFIG =================
FOND_PRINCIPAL = "#1f0c41"
BOUTON_BG = "#92152f"
BOUTON_FG = "#f6b9d9"
BOUTON_HOVER = "#743649"
TEXT_COLOR = "#e7afa9"
ACCENT_COLOR = "#f6b9d9"

MAX_BOTS = 10
DOSSIER_BASE = "images_telechargees"
DELAY = 0.05
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://hhentai.fr/"
}
# =========================================

lock = threading.Lock()
total_chapitres = 0
chapitres_finis = 0
chapitre_urls = []
debut_chapitre_total = 1
fin_chapitre_total = 1
surveillance_active = False

# ---------------- Fonctions ----------------

def est_image(r):
    return r.headers.get("Content-Type", "").startswith("image")

def trouver_chapitres(manga_url):
    try:
        r = requests.get(manga_url, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except:
        messagebox.showerror("Erreur", "Impossible d'accéder au manga.")
        return [], 1, 1

    soup = BeautifulSoup(r.text, "html.parser")

    # Cas classique : plusieurs chapitres
    premier_tag = soup.find("a", id="btn-read-last")
    dernier_tag = soup.find("a", id="btn-read-first")

    if premier_tag and dernier_tag:
        import re
        def extraire_num(url):
            m = re.search(r"chapitre-(\d+)/?", url)
            return int(m.group(1)) if m else 1

        debut = extraire_num(premier_tag["href"])
        fin = extraire_num(dernier_tag["href"])
        base_url = premier_tag["href"].rsplit("chapitre-", 1)[0] + "chapitre-"
        urls = [base_url + str(n) + "/" for n in range(debut, fin + 1)]
        return urls, debut, fin

    messagebox.showerror("Erreur", "Impossible de trouver les chapitres.")
    return [], 1, 1

def telecharger_chapitre(lien_chapitre, dossier):
    os.makedirs(dossier, exist_ok=True)
    try:
        r = requests.get(lien_chapitre, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except:
        print(f"Erreur: impossible d'accéder à {lien_chapitre}")
        return 0

    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.select("div.page-break img.wp-manga-chapter-img")
    if not images:
        images = soup.find_all("img")

    if not images:
        print("Aucune image trouvée sur la page")
        return 0

    page = 1
    for img in images:
        src = img.get("src", "").strip()
        if not src:
            continue
        ext = os.path.splitext(src)[1]
        nom_page = f"page_{page}{ext}"
        try:
            r_img = requests.get(src, headers=HEADERS, timeout=10)
            if est_image(r_img):
                with open(os.path.join(dossier, nom_page), "wb") as f:
                    f.write(r_img.content)
                page += 1
                time.sleep(DELAY)
        except:
            continue
    return page - 1

def bot_worker(q):
    global chapitres_finis
    while True:
        try:
            titre, lien_chapitre, chap_num, lbl = q.get_nowait()
        except queue.Empty:
            break
        lbl.config(text=f"{titre} | Chapitre {chap_num} : ⏳ Téléchargement", fg=ACCENT_COLOR)
        dossier = os.path.join(DOSSIER_BASE, titre, f"Chapitre_{chap_num}")
        nb_pages = telecharger_chapitre(lien_chapitre, dossier)
        lbl.config(text=f"{titre} | Chapitre {chap_num} : ✔ Terminé ({nb_pages} pages)", fg=TEXT_COLOR)
        with lock:
            chapitres_finis += 1
            progress_var.set(int(chapitres_finis / total_chapitres * 100))
        q.task_done()

# ---------------- Actions Tkinter ----------------

def verifier_chapitres():
    global chapitre_urls, debut_chapitre_total, fin_chapitre_total
    manga_url = entry_url.get().strip()
    if not manga_url:
        return
    chapitre_urls, debut_chapitre_total, fin_chapitre_total = trouver_chapitres(manga_url)
    if chapitre_urls:
        label_info.config(text=f"Chapitres disponibles : {debut_chapitre_total} à {fin_chapitre_total}", fg=ACCENT_COLOR)
        entry_debut.config(state="normal")
        entry_fin.config(state="normal")
        entry_debut.delete(0, tk.END)
        entry_fin.delete(0, tk.END)
        entry_debut.insert(0, str(debut_chapitre_total))
        entry_fin.insert(0, str(fin_chapitre_total))
    else:
        label_info.config(text="Impossible de détecter les chapitres.", fg="red")

def lancer_telechargement():
    global total_chapitres, chapitres_finis
    manga_url = entry_url.get().strip()
    if not manga_url or not chapitre_urls:
        messagebox.showerror("Erreur", "Veuillez d'abord vérifier les chapitres.")
        return

    try:
        chap_debut = int(entry_debut.get())
        chap_fin = int(entry_fin.get())
    except:
        messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour les chapitres.")
        return
    if chap_debut < debut_chapitre_total or chap_fin > fin_chapitre_total or chap_debut > chap_fin:
        messagebox.showerror("Erreur", f"Chapitres disponibles : {debut_chapitre_total} à {fin_chapitre_total}")
        return

    titre = manga_url.rstrip("/").split("/")[-1].replace("-", " ").title()
    for w in frame_chapitres.winfo_children():
        w.destroy()
    q = queue.Queue()
    chapitres_finis = 0
    for i, lien in enumerate(chapitre_urls):
        chap_num = debut_chapitre_total + i
        if chap_num < chap_debut or chap_num > chap_fin:
            continue
        lbl = tk.Label(frame_chapitres, text=f"{titre} | Chapitre {chap_num} : ⏳ En attente",
                       bg=FOND_PRINCIPAL, fg=TEXT_COLOR, anchor="w")
        lbl.pack(fill="x", pady=2)
        q.put((titre, lien, chap_num, lbl))
    total_chapitres = q.qsize()
    if total_chapitres == 0:
        messagebox.showinfo("Info", "Aucun chapitre à télécharger.")
        return
    threads = []
    for _ in range(min(MAX_BOTS, total_chapitres)):
        t = threading.Thread(target=bot_worker, args=(q,))
        t.start()
        threads.append(t)
    def attendre():
        for t in threads:
            t.join()
        messagebox.showinfo("Terminé", "Tous les chapitres sélectionnés ont été téléchargés.")
    threading.Thread(target=attendre).start()

# ---- Effet survol bouton ----
def on_enter(e):
    e.widget['background'] = BOUTON_HOVER

def on_leave(e):
    e.widget['background'] = BOUTON_BG

# ---------------- Tkinter ----------------

root = tk.Tk()
root.title("Succubus Downloader")
root.geometry("1000x600")
root.config(bg=FOND_PRINCIPAL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "logo.png")
try:
    root.iconphoto(False, tk.PhotoImage(file=logo_path))
except Exception as e:
    print("Erreur chargement icône :", e)

# ---- Frame gauche ----
frame_gauche = tk.Frame(root, bg=FOND_PRINCIPAL)
frame_gauche.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tk.Label(frame_gauche, text="Succubus Downloader hhentai.fr",
         bg=FOND_PRINCIPAL, fg=TEXT_COLOR, font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(frame_gauche, text="Lien du manga :", bg=FOND_PRINCIPAL, fg=TEXT_COLOR).pack()
entry_url = tk.Entry(frame_gauche, width=50)
entry_url.pack(pady=5)

def demander_mode_surveillance():
    reponse = messagebox.askyesno("Mode surveillance",
                                  "Voulez-vous activer le mode surveillance du presse-papiers ?")
    if reponse:
        global surveillance_active
        surveillance_active = True
        messagebox.showinfo("Info", "Mode surveillance activé !")

btn_mode = tk.Button(frame_gauche, text="Activer le mode surveillance",
                     command=demander_mode_surveillance,
                     bg=BOUTON_BG, fg=BOUTON_FG, width=35)
btn_mode.pack(pady=5)
btn_mode.bind("<Enter>", on_enter)
btn_mode.bind("<Leave>", on_leave)

btn_verifier = tk.Button(frame_gauche, text="Vérifier les chapitres", command=verifier_chapitres,
          bg=BOUTON_BG, fg=BOUTON_FG, width=25)
btn_verifier.pack(pady=5)
btn_verifier.bind("<Enter>", on_enter)
btn_verifier.bind("<Leave>", on_leave)

label_info = tk.Label(frame_gauche, text="", bg=FOND_PRINCIPAL, fg=TEXT_COLOR)
label_info.pack()

tk.Label(frame_gauche, text="Chapitre de départ :", bg=FOND_PRINCIPAL, fg=TEXT_COLOR).pack()
entry_debut = tk.Entry(frame_gauche, width=10)
entry_debut.pack(pady=2)

tk.Label(frame_gauche, text="Chapitre de fin :", bg=FOND_PRINCIPAL, fg=TEXT_COLOR).pack()
entry_fin = tk.Entry(frame_gauche, width=10)
entry_fin.pack(pady=2)

btn_lancer = tk.Button(frame_gauche, text="Lancer le téléchargement", command=lancer_telechargement,
          bg=BOUTON_BG, fg=BOUTON_FG, width=30)
btn_lancer.pack(pady=10)
btn_lancer.bind("<Enter>", on_enter)
btn_lancer.bind("<Leave>", on_leave)

progress_var = tk.IntVar()
ttk.Progressbar(frame_gauche, variable=progress_var, maximum=100).pack(fill="x", padx=20, pady=10)

frame_chapitres = tk.Frame(frame_gauche, bg=FOND_PRINCIPAL)
frame_chapitres.pack(fill="both", expand=True, padx=10, pady=10)

# ---- Frame droite image ----
frame_droite = tk.Frame(root, bg=FOND_PRINCIPAL)
frame_droite.pack(side="right", fill="y", padx=10, pady=10)

image_path = os.path.join(BASE_DIR, "image.png")
try:
    image = Image.open(image_path)
    hauteur_fenetre = 600
    ratio = image.width / image.height
    nouvelle_hauteur = hauteur_fenetre
    nouvelle_largeur = int(ratio * nouvelle_hauteur)
    image = image.resize((nouvelle_largeur, nouvelle_hauteur), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    lbl_image = tk.Label(frame_droite, image=photo, bg=FOND_PRINCIPAL, bd=0, highlightthickness=0)
    lbl_image.image = photo
    lbl_image.pack()
except Exception as e:
    print("Erreur chargement image :", e)

# ---------------- Surveillance presse-papiers ----------------
def surveiller_presse_papiers():
    dernier_contenu = ""
    global surveillance_active
    while True:
        if surveillance_active:
            try:
                contenu = pyperclip.paste()
                if contenu != dernier_contenu:
                    dernier_contenu = contenu
                    if contenu.startswith("http"):
                        entry_url.delete(0, tk.END)
                        entry_url.insert(0, contenu)

                        root.attributes('-topmost', True)
                        root.update()
                        root.attributes('-topmost', False)

                        verifier_chapitres()
            except:
                pass
        time.sleep(0.5)

threading.Thread(target=surveiller_presse_papiers, daemon=True).start()

root.mainloop()
