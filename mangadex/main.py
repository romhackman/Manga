import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from api import search, chapters, pages
from downloader import download_chapter
import os
import subprocess
import sys


class MangaDLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MangaDL - MangaDex Downloader")
        self.root.geometry("1000x600")
        self.root.minsize(900, 500)
        self.root.configure(bg="#f27405")

        # Dossier du script
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Icône
        logo_path = os.path.join(self.BASE_DIR, "logo.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).resize((32, 32), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            root.iconphoto(False, self.logo)

        self.manga_data = []
        self.chapter_data = []
        self._img_orig = None
        self._resize_job = None

        # ================= BARRE DU HAUT =================
        top_frame = tk.Frame(root, bg="#fc8b13", height=40)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(
            top_frame,
            text="pdfV2",
            command=self.lancer_pdfV2,
            bg="#FFA75E",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=10, pady=5)

        # ================= FRAMES PRINCIPAUX =================
        self.left_frame = tk.Frame(root, bg="#f27405")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(
            root, width=300, bg="#f27405",
            highlightbackground="#fc8b13", highlightthickness=6
        )
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)

        # ================= IMAGE DROITE =================
        self.right_image_label = tk.Label(self.right_frame, bg="#f27405")
        self.right_image_label.pack(expand=True)
        self.load_image_async()
        self.root.bind("<Configure>", self.on_resize)

        # ================= UI GAUCHE =================
        self.create_left_ui()

    # ==================================================
    # LANCER PDFV2 (EXTERNE)
    # ==================================================
    def lancer_script(self, chemin):
        if os.path.exists(chemin):
            subprocess.Popen([sys.executable, chemin])
        else:
            messagebox.showerror("Erreur", f"Fichier introuvable :\n{chemin}")

    def lancer_pdfV2(self):
        manga_root = os.path.dirname(self.BASE_DIR)
        pdf_path = os.path.join(manga_root, "programme", "pdfV2.py")
        self.lancer_script(pdf_path)

    # ==================================================
    # UI GAUCHE
    # ==================================================
    def create_left_ui(self):
        self.lang_var = tk.StringVar(value="fr")

        lang_frame = tk.Frame(self.left_frame, bg="#f27405")
        tk.Label(lang_frame, text="Choisir langue:", bg="#f27405",
                 fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(lang_frame, text="FR", variable=self.lang_var,
                       value="fr", bg="#f27405", fg="white").pack(side=tk.LEFT)
        tk.Radiobutton(lang_frame, text="EN", variable=self.lang_var,
                       value="en", bg="#f27405", fg="white").pack(side=tk.LEFT)
        lang_frame.pack(pady=5, anchor="w")

        tk.Label(self.left_frame, text="Rechercher un manga:", bg="#f27405",
                 fg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        search_frame = tk.Frame(self.left_frame, bg="#f27405")
        self.search_input = tk.Entry(search_frame, width=25, font=("Arial", 11))
        self.search_input.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Rechercher",
                  command=self.search_manga, bg="#FFA75E",
                  fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        search_frame.pack(pady=5, anchor="w")

        tk.Label(self.left_frame, text="Résultats:", bg="#f27405",
                 fg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.result_list = tk.Listbox(self.left_frame, height=8,
                                      font=("Arial", 10), bg="white", fg="black")
        self.result_list.pack(fill=tk.BOTH, pady=5)
        self.result_list.bind("<<ListboxSelect>>", lambda e: self.show_chapters())

        tk.Label(self.left_frame, text="Chapitres:", bg="#f27405",
                 fg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.chapter_list = tk.Listbox(self.left_frame, selectmode=tk.MULTIPLE,
                                       font=("Arial", 10), bg="white", fg="black")
        self.chapter_list.pack(fill=tk.BOTH, expand=True, pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("orange.Horizontal.TProgressbar",
                        troughcolor="white", background="#FFA75E")
        self.progress = ttk.Progressbar(self.left_frame,
                                        orient=tk.HORIZONTAL, mode="determinate",
                                        style="orange.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=5)

        tk.Button(self.left_frame, text="Télécharger chapitre(s)",
                  command=self.download_selected, bg="#FFA75E",
                  fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    # ==================================================
    # IMAGE
    # ==================================================
    def load_image(self):
        if not self._img_orig:
            return
        h = self.right_frame.winfo_height() - 20
        w = self.right_frame.winfo_width() - 20
        if h <= 0 or w <= 0:
            return
        ow, oh = self._img_orig.size
        r = min(h / oh, w / ow)
        img = self._img_orig.resize((int(ow * r), int(oh * r)), Image.LANCZOS)
        self.right_image = ImageTk.PhotoImage(img)
        self.right_image_label.configure(image=self.right_image)

    def load_image_async(self):
        img_path = os.path.join(self.BASE_DIR, "image.png")
        if not os.path.exists(img_path):
            return

        def worker():
            self._img_orig = Image.open(img_path)
            self.root.after(0, self.load_image)

        threading.Thread(target=worker, daemon=True).start()

    def on_resize(self, event):
        if self._resize_job:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(150, self.load_image)

    # ==================================================
    # LOGIQUE
    # ==================================================
    def get_lang(self):
        return self.lang_var.get()

    def search_manga(self):
        title = self.search_input.get().strip()
        if not title:
            return
        self.result_list.delete(0, tk.END)
        self.chapter_list.delete(0, tk.END)
        try:
            self.manga_data = search(title)
            for m in self.manga_data:
                t = m["attributes"]["title"].get("en", "N/A")
                self.result_list.insert(tk.END, f"{t} | {m['id']}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def show_chapters(self):
        sel = self.result_list.curselection()
        if not sel:
            return
        manga_id = self.manga_data[sel[0]]["id"]
        self.chapter_list.delete(0, tk.END)
        try:
            self.chapter_data = chapters(manga_id, self.get_lang())
            for ch in self.chapter_data:
                num = ch["attributes"]["chapter"] or "N/A"
                title = ch["attributes"]["title"] or ""
                self.chapter_list.insert(tk.END, f"Chap {num} {title}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def download_selected(self):
        sel = self.chapter_list.curselection()
        if not sel:
            return
        chapters_to_dl = [self.chapter_data[i]["id"] for i in sel]
        folder = filedialog.askdirectory(title="Choisir dossier de téléchargement")
        if not folder:
            return
        threading.Thread(
            target=self.download_thread,
            args=(chapters_to_dl, folder),
            daemon=True
        ).start()

    def download_thread(self, chapters_to_dl, folder):
        self.progress["maximum"] = len(chapters_to_dl)
        self.progress["value"] = 0
        for i, chapter_id in enumerate(chapters_to_dl, 1):
            try:
                data = pages(chapter_id)
                download_chapter(data, folder, chapter_num=i, cbz=True)
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
            self.progress["value"] = i
        messagebox.showinfo("Succès", "Téléchargement terminé !")
        self.progress["value"] = 0


# ======================================================
# LANCEMENT
# ======================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MangaDLApp(root)
    root.mainloop()
