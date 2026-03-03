import tkinter as tk
from tkinter import messagebox
import threading, os, json, requests, webbrowser
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "genres_count.json")
download_folder = os.path.join(BASE_DIR, 'poster_scan')
logo_path = os.path.join(BASE_DIR, 'logo.png')
os.makedirs(download_folder, exist_ok=True)

# ===== Fonctions utilitaires =====
def anime_to_link(anime_name):
    url_name = anime_name.lower().replace(' ','-').replace(',','').replace('é','e').replace('è','e').replace('ê','e')
    url_name = url_name.replace('ô','o').replace('’','').replace(':','').replace('.','')
    return f"https://raw.githubusercontent.com/Anime-Sama/IMG/img/contenu/{url_name}.jpg"

def add_watermark_and_logo(image_path, text="romh@ckman", logo_path=logo_path):
    img = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new('RGBA', img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    font_size = max(20, img.width // 20)
    try: font = ImageFont.truetype("arial.ttf", font_size)
    except: font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0,0), text, font=font)
        text_width,text_height = bbox[2]-bbox[0], bbox[3]-bbox[1]
    except:
        text_width,text_height = font.getsize(text)
    draw.text((img.width-text_width-10, img.height-text_height-10), text, font=font, fill=(255,255,255,180))
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_width = int(img.width*0.15)
        logo_height = int(logo_width / (logo.width/logo.height))
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        img.paste(logo, (img.width-logo_width-10,10), logo)
    Image.alpha_composite(img, txt_layer).convert("RGB").save(image_path,"JPEG")

# ===== Onglet Downloader =====
def setup_downloader_tab(tabs, FOND, GRIS, TEXTE, BOUTON_BG):
    frame_root = tk.Frame(tabs, bg=FOND)
    tabs.add(frame_root, text="📥 Downloader")

    # ===== Frame des boutons en haut =====
    btn_frame = tk.Frame(frame_root, bg=FOND)
    btn_frame.pack(fill="x", pady=10)

    # ===== Canvas scrollable pour la liste =====
    canvas = tk.Canvas(frame_root, bg=FOND, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=FOND)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0,0), window=scroll_frame, anchor="nw")

    def resize_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", resize_frame)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ===== Molette =====
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # ===== Variables =====
    vars_list = []
    current_page = 0
    page_size = 15
    all_animes = []

    def load_all_animes():
        nonlocal all_animes
        if not os.path.exists(json_path):
            all_animes = []
            return
        with open(json_path,"r",encoding="utf-8") as f:
            data=json.load(f)
        all_animes = data.get("animes", [])

    def display_page(page):
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        vars_list.clear()
        start = page*page_size
        end = start+page_size
        for anime in all_animes[start:end]:
            var = tk.IntVar()
            chk = tk.Checkbutton(scroll_frame,text=anime,variable=var,
                                 bg=FOND,fg=TEXTE,selectcolor=GRIS,
                                 anchor="w",justify="left")
            chk.pack(fill="x",padx=10,pady=2)
            vars_list.append((anime,var))

    # ===== Actions boutons =====
    def refresh_list():
        load_all_animes()
        nonlocal current_page
        current_page = 0
        display_page(current_page)

    def next_page():
        nonlocal current_page
        if (current_page+1)*page_size < len(all_animes):
            current_page +=1
            display_page(current_page)

    def prev_page():
        nonlocal current_page
        if current_page>0:
            current_page -=1
            display_page(current_page)

    def download_selected_posters():
        selected_animes = [a for a,v in vars_list if v.get()==1]
        if not selected_animes:
            messagebox.showinfo("Info","Veuillez sélectionner au moins un anime.")
            return
        for anime in selected_animes:
            url = anime_to_link(anime)
            filename = os.path.join(download_folder, url.split('/')[-1])
            if os.path.exists(filename): continue
            try:
                resp = requests.get(url); resp.raise_for_status()
                with open(filename,'wb') as f: f.write(resp.content)
                add_watermark_and_logo(filename)
            except: pass
        messagebox.showinfo("Terminé","Téléchargement terminé !")

    # ===== Génération HTML pour toutes les images =====
    def view_images():
        images = [f for f in os.listdir(download_folder) if f.lower().endswith((".jpg",".jpeg",".png"))]
        if not images:
            messagebox.showinfo("Info","Aucune image disponible pour afficher.")
            return
        html_path = os.path.join(download_folder, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("""
            <html>
            <head>
            <title>Galerie Anime – Pro</title>
            <style>
                body { margin:0; background:#121212; font-family: Arial, sans-serif; color:#fff; }
                h1 { text-align:center; margin:20px 0; font-size:2em; }
                .gallery { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:25px; padding:25px; justify-items:center; }
                .item { cursor:pointer; border-radius:12px; overflow:hidden; transition: transform 0.3s, box-shadow 0.3s; }
                .item:hover { transform: scale(1.08); box-shadow:0 15px 30px rgba(0,0,0,0.6); }
                img { width:100%; display:block; border-radius:8px; }
                p { margin:8px 0 0; font-weight:bold; font-size:15px; text-align:center; color:#fff; }
                .lightbox { position:fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.95);
                            display:none; align-items:center; justify-content:center; z-index:1000; flex-direction:column;
                            opacity:0; transition: opacity 0.4s ease-in-out; }
                .lightbox.show { display:flex; opacity:1; }
                .lightbox img { max-width:85%; max-height:75%; border-radius:12px; transition: transform 0.4s ease; }
                .lightbox p { margin-top:12px; font-size:22px; font-weight:bold; }
                .close, .prev, .next { position:absolute; top:50%; transform:translateY(-50%); font-size:55px; color:#fff; cursor:pointer; user-select:none; padding:15px; border-radius:50%; background:rgba(0,0,0,0.4); transition: background 0.2s; }
                .close { top:25px; right:35px; font-size:45px; transform:none; }
                .prev { left:25px; }
                .next { right:25px; }
                .close:hover, .prev:hover, .next:hover { background:rgba(0,0,0,0.7); }
                @media(max-width:600px){ .gallery { grid-template-columns: repeat(auto-fill,minmax(150px,1fr)); } }
            </style>
            </head>
            <body>
            <h1>Galerie des Posters Anime</h1>
            <div class="gallery">
            """)
            for idx, img_file in enumerate(images):
                anime_name = os.path.splitext(img_file)[0].replace("-", " ").title()
                f.write(f"""
                <div class="item" onclick="openLightbox({idx})">
                    <img src="{img_file}" alt="{anime_name}">
                    <p>{anime_name}</p>
                </div>
                """)
            f.write("""
            </div>
            <div class="lightbox" id="lightbox">
                <span class="close" onclick="closeLightbox()">&times;</span>
                <span class="prev" onclick="prevImage()">&#10094;</span>
                <span class="next" onclick="nextImage()">&#10095;</span>
                <img id="lightbox-img" src="">
                <p id="lightbox-caption"></p>
            </div>
            <script>
                const images = [""")
            f.write(",".join([f'"{img}"' for img in images]))
            f.write("""];

                const captions = [""")
            f.write(",".join([f'"{os.path.splitext(img)[0].replace("-", " ").title()}"' for img in images]))
            f.write("""];

                let current = 0;
                const lightbox = document.getElementById('lightbox');
                const lbImg = document.getElementById('lightbox-img');
                const lbCaption = document.getElementById('lightbox-caption');

                function openLightbox(idx){
                    current = idx;
                    lbImg.src = images[current];
                    lbCaption.innerText = captions[current];
                    lightbox.classList.add('show');
                }
                function closeLightbox(){ lightbox.classList.remove('show'); }
                function prevImage(){ current = (current-1+images.length)%images.length; lbImg.src=images[current]; lbCaption.innerText=captions[current]; }
                function nextImage(){ current = (current+1)%images.length; lbImg.src=images[current]; lbCaption.innerText=captions[current]; }

                document.addEventListener('keydown', function(e){
                    if(lightbox.classList.contains('show')){
                        if(e.key==='ArrowLeft') prevImage();
                        if(e.key==='ArrowRight') nextImage();
                        if(e.key==='Escape') closeLightbox();
                    }
                });
            </script>
            </body>
            </html>
            """)
        webbrowser.open(f"file://{html_path}")

    # ===== Création boutons visibles en haut =====
    tk.Button(btn_frame,text="🔄 Actualiser",bg=BOUTON_BG,fg=TEXTE,command=refresh_list).pack(side="left", padx=5)
    tk.Button(btn_frame,text="⬇ Télécharger sélection",bg=BOUTON_BG,fg=TEXTE,
              command=lambda: threading.Thread(target=download_selected_posters, daemon=True).start()).pack(side="left", padx=5)
    tk.Button(btn_frame,text="🖼 Voir images",bg=BOUTON_BG,fg=TEXTE,command=view_images).pack(side="left", padx=5)
    tk.Button(btn_frame,text="⬅ Page précédente",bg=BOUTON_BG,fg=TEXTE,command=prev_page).pack(side="left", padx=5)
    tk.Button(btn_frame,text="Page suivante ➡",bg=BOUTON_BG,fg=TEXTE,command=next_page).pack(side="left", padx=5)

    refresh_list()