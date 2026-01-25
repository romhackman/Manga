import os
import tkinter as tk
from tkinter import ttk
from finder import setup_finder_tab
from graph import setup_graph_tab
from generator import setup_generator_tab
from downloader import setup_downloader_tab

# ================= Thème =================
FOND = "#040404"
BLEU = "#007ACC"
GRIS = "#222222"
ENTREE_BG = "#222222"
TEXTE = "#FFFFFF"
BOUTON_BG = "#333333"

# ================= Fenêtre principale =================
root = tk.Tk()
root.title("Anime-sama – Tracker complet")
root.geometry("1200x800")
root.configure(bg=FOND)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=FOND, borderwidth=0)
style.configure("TNotebook.Tab", background=BOUTON_BG, foreground=TEXTE)
style.map("TNotebook.Tab", background=[("selected", BLEU)])

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

# ================= Onglets =================
setup_finder_tab(tabs, FOND, ENTREE_BG, TEXTE, BLEU, BOUTON_BG)
setup_graph_tab(tabs, FOND, GRIS, TEXTE)
setup_generator_tab(tabs, FOND, ENTREE_BG, TEXTE, BOUTON_BG)
setup_downloader_tab(tabs, FOND, GRIS, TEXTE, BOUTON_BG)

root.mainloop()
