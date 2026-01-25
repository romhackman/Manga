import tkinter as tk
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "genres_count.json")

def setup_graph_tab(tabs, FOND, GRIS, TEXTE):
    graph = tk.Frame(tabs, bg=FOND)
    tabs.add(graph, text="📊 Graph")
    canvas_graph = tk.Canvas(graph, bg=GRIS)
    canvas_graph.pack(fill="both", expand=True, padx=20, pady=20)

    def lire_json():
        if not os.path.exists(json_path): return {}
        with open(json_path,"r",encoding="utf-8") as f:
            try: return {k:int(v) for k,v in json.load(f).get("genres",{}).items()}
            except: return {}

    def dessiner_graphique():
        canvas_graph.delete("all")
        data = lire_json()
        largeur, hauteur, marge = canvas_graph.winfo_width(), canvas_graph.winfo_height(), 60
        if not data:
            canvas_graph.create_text(largeur/2, hauteur/2, text="Aucun genre dans le JSON", fill="white", font=("Arial",16))
            return
        genres_sorted = sorted(data.items(), key=lambda x:x[1], reverse=True)
        noms, valeurs = [k for k,v in genres_sorted],[v for k,v in genres_sorted]
        max_val, n = max(valeurs), len(noms)
        barre_largeur = (largeur-2*marge)/n*0.6
        espace = (largeur-2*marge)/n
        for i,(nom,val) in enumerate(genres_sorted):
            x0 = marge + i*espace + (espace-barre_largeur)/2
            y0 = hauteur - marge
            x1 = x0 + barre_largeur
            y1 = hauteur - marge - (val/max_val)*(hauteur-2*marge)
            couleur = f"#{(i*70)%256:02x}{(100+i*50)%256:02x}{(200-i*30)%256:02x}"
            canvas_graph.create_rectangle(x0,y0,x1,y1, fill=couleur)
            canvas_graph.create_text((x0+x1)/2, y1-10, text=str(val), fill="white", font=("Arial", max(8,int(12*(1/n)))), anchor="s")
            canvas_graph.create_text((x0+x1)/2, y0+15, text=nom, fill="white", font=("Arial", max(8,int(12*(1/n)))), angle=45, anchor="n")
        canvas_graph.create_text(largeur/2, 30, text="Genres préférés", fill="white", font=("Arial",18,"bold"))

    def update_graphique():
        dessiner_graphique()
        graph.after(3000, update_graphique)

    graph.after(0, update_graphique)
