import tkinter as tk
import json, unicodedata, urllib.parse, os, tkinter.messagebox as messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "genres_count.json")

ALL_GENRES = ["Action","Adolescence","Aliens / Extra-terrestres","Amitié","Amour","Apocalypse",
"Art","Arts martiaux","Assassinat","Autre monde","Aventure","Combats","Comédie","Crime","Cyberpunk",
"Danse","Démons","Détective","Donghua","Dragon","Drame","Ecchi","Ecole","Elfe","Enquête","Famille",
"Fantastique","Fantasy","Fantômes","Futur","Gastronomie","Ghibli","Guerre","Harcèlement","Harem",
"Harem inversé","Histoire","Historique","Horreur","Isekai","Jeunesse","Jeux","Jeux vidéo","Josei",
"Journalisme","Kaï","Mafia","Magical girl","Magie","Maladie","Mariage","Mature","Mechas","Médiéval",
"Militaire","Monde virtuel","Monstres","Musique","Mystère","Nekketsu","Ninjas","Nostalgie","Paranormal",
"Philosophie","Pirates","Police","Politique","Post-apocalyptique","Pouvoirs psychiques","Préhistoire",
"Prison","Psychologique","Quotidien","Religion","Réincarnation / Transmigration","Romance",
"Samouraïs","School Life","Science-Fantasy","Science-fiction","Scientifique","Seinen","Shôjo",
"Shôjo-Ai","Shônen","Shônen-Ai","Slice of Life","Société","Sport","Super pouvoirs","Super-héros",
"Surnaturel","Survie","Survival game","Technologies","Thriller","Tournois","Travail","Vampires",
"Vengeance","Voyage","Voyage temporel","Webcomic","Yakuza","Yaoi","Yokai","Yuri"]

def setup_generator_tab(tabs, FOND, ENTREE_BG, TEXTE, BOUTON_BG):
    # Frame principale
    frame_root = tk.Frame(tabs, bg=FOND)
    tabs.add(frame_root, text="🔗 Générateur")

    # Canvas + Scrollbar
    canvas_gen = tk.Canvas(frame_root, bg=FOND, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_root, orient="vertical", command=canvas_gen.yview)
    canvas_gen.configure(yscrollcommand=scrollbar.set)

    canvas_gen.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame qui contient les checkbuttons
    frame = tk.Frame(canvas_gen, bg=FOND)
    frame_window = canvas_gen.create_window((0,0), window=frame, anchor="nw")

    # Redimensionnement dynamique
    def on_frame_configure(event):
        canvas_gen.configure(scrollregion=canvas_gen.bbox("all"))
    frame.bind("<Configure>", on_frame_configure)

    genre_vars, result_var = {}, tk.StringVar()

    def normalize(text):
        return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c)!="Mn")

    def refresh_genres():
        for widget in frame.winfo_children():
            widget.destroy()
        genre_vars.clear()
        if os.path.exists(json_path):
            with open(json_path,"r",encoding="utf-8") as f:
                raw_stats = json.load(f)
        else:
            raw_stats = {"genres":{}}
        stats = {normalize(k):int(v) for k,v in raw_stats.get("genres",{}).items()}
        sorted_genres = sorted(ALL_GENRES, key=lambda g: stats.get(normalize(g),0), reverse=True)
        for i, g in enumerate(sorted_genres):
            score = stats.get(normalize(g),0)
            label = f"{g} ({score})" if score>0 else g
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=label, variable=var, bg=FOND, fg=TEXTE,
                                 selectcolor=ENTREE_BG, anchor="w", justify="left")
            chk.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            genre_vars[g] = var

    def generate_link():
        selected = [g for g,v in genre_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning("Attention","Sélectionne au moins un genre")
            return
        params = [("type[]","Scans"),("search","")]
        for g in selected:
            params.append(("genre[]", g))
        result_var.set("https://anime-sama.si/catalogue/?" + urllib.parse.urlencode(params, doseq=True))

    def copy_link():
        frame_root.clipboard_clear()
        frame_root.clipboard_append(result_var.get())
        messagebox.showinfo("OK","Lien copié")

    # Boutons et Entry
    btn_frame = tk.Frame(frame_root, bg=FOND)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="🔄 Actualiser genres", command=refresh_genres, bg=BOUTON_BG, fg=TEXTE).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔗 Générer le lien", command=generate_link, bg=BOUTON_BG, fg=TEXTE).pack(side="left", padx=5)
    tk.Button(btn_frame, text="📋 Copier le lien", command=copy_link, bg=BOUTON_BG, fg=TEXTE).pack(side="left", padx=5)
    tk.Entry(frame_root, textvariable=result_var, width=120).pack(pady=5)

    refresh_genres()
    return frame_root
