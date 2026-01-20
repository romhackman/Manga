# Manga Downloader V5.1 🌐📚

![Logo Manga Downloader](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png?raw=true)

**Bonjour, je suis Romh@ckman !**

**Accroche :**
Téléchargez facilement vos mangas favoris en quelques clics, depuis Anime Sama et MangaDex, grâce à une application simple et open-source.

**Explication rapide :**
Manga Downloader V5 est une application Python open-source qui centralise tous vos besoins : téléchargement automatique des chapitres, création de PDF, gestion des plugins et organisation des fichiers. Compatible Windows et Linux, elle calcule automatiquement le nombre de pages par chapitre et permet aux utilisateurs avancés d’ajouter ou créer des plugins pour étendre les sources de mangas disponibles.

---
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/) 
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-Yes-blue?style=flat-square)
![Linux](https://img.shields.io/badge/Linux-Yes-blue?style=flat-square)
![Stars](https://img.shields.io/github/stars/romhackman/Manga)
![Forks](https://img.shields.io/github/forks/romhackman/Manga)

---
## 🚀 Fonctionnalités

- Télécharger les derniers chapitres de mangas depuis Anime Sama et MangaDex  
- Interface simple et conviviale  
- Open-source : vous pouvez contribuer ou l’améliorer  
- Fonctionne sur Windows et Linux via un exécutable prêt à l’emploi  
- Ajouter facilement des plugins  
- Mise à jour automatique du nom de domaine de Anime Sama
- Mise à jour automatique de ce projet

---

## 💻 Téléchargement

Accédez au dépôt GitHub pour **télécharger l’application et le code source** :

[Manga Downloader Installer sur GitHub](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Install_Manga_V5_win_linux.py)

---

## ⚠️ Avertissement légal

Ce projet est fourni **à titre éducatif et technique uniquement**, pour expérimenter et apprendre le code.  
Je décline toute responsabilité quant à l’utilisation et au contenu des fichiers téléchargés. Ces programmes sont destinés à un usage strictement personnel. **Aucun fichier protégé par le droit d’auteur n’est fourni.**  
Certains contenus peuvent enfreindre les droits d’auteur ou soulever des questions éthiques et légales. L’utilisateur est **entièrement responsable** de l’usage qu’il en fait et des éventuelles conséquences légales.  

Le code est fourni “tel quel” sous **licence MIT**. L’auteur ne garantit rien et ne peut être tenu responsable de l’utilisation du logiciel.

---

## 📜 Licence

Ce projet est sous **[Licence MIT](LICENSE)**.

# 📑 Sommaire

* [Launcher](#-launcher)
* [Plugins](#-plugins)
* [Anime-Sama](#-anime-sama)
  * [MangaV3](#-manga)
  * [ShareV2](#-sharev2)
  * [APPV2](#-appv2)
* [Scraper Anime-Sama](#-anime-sama-domain-scraper)
* [MangaDex](#-mangadex)
* [Update](#-update)
  
---

## Launcher 
![Launcher](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/home/logo.png?raw=true)

Le **Launcher** est l'interface principale de cette application. Il permet d'accéder rapidement à vos mangas favoris et à tous les modules et fonctionnalités disponibles.

### Configuration ⚙️
*Permet de définir le dossier principal pour vos mangas. Au premier lancement, le programme vous demande de sélectionner un dossier où tous vos mangas seront téléchargés. Si vous annulez, un dossier par défaut sera créé dans le dossier Launcher. Les informations sur ce dossier sont stockées dans un fichier JSON. Vous pouvez changer le dossier de destination à tout moment en cliquant à nouveau sur ce bouton.*

### Plugins 🧩
*Ce module permet d'ajouter des sites supplémentaires pour télécharger des mangas autres que Anime-Sama et MangaDex. Il est également possible de créer des extensions sans toucher au code de l'application. Le fonctionnement complet, du téléchargement à la création de plugins, [est détaillé dans le manuel, section Plugins](#-plugins).*

### PDF V2 📜
*Ce module rend la lecture de toutes les images de vos mangas plus simple et agréable. Vous pouvez faire défiler vos mangas page par page, ce qui améliore grandement le confort de lecture.*

### Anime-Sama 🐾
*Anime-Sama permet de télécharger des scans provenant de ce site, ce qui est normalement impossible. Le module propose également d'autres fonctionnalités pour faciliter le téléchargement de vos scans. Tous les détails sont disponibles dans [le manuel, section Anime-Sama](#-anime-sama).*

### MangaDex 🐈
*MangaDex permet de télécharger facilement des scans provenant de MangaDex. Ce module est un peu plus complexe qu’Anime-Sama mais contient moins de scans en stock. Son fonctionnement est détaillé dans [le manuel, section MangaDex](#-mangadex).*

### Actualiser 🔄
*Ce bouton permet de rafraîchir la liste de vos mangas. Cette action est également effectuée automatiquement à chaque ouverture du Launcher.*

---
## 🧩 Plugins
![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/logo.png?raw=true)
[Somaine 📑](#-sommaire)
Ce programme est un **gestionnaire de plugins**. Il permet à l’utilisateur de télécharger, installer et lancer facilement des plugins depuis GitHub, sans avoir besoin de manipuler des fichiers ou des commandes.

### Comment fonctionne le programme
- **Affichage des plugins** : Le programme lit le fichier `plugins/instance_plugins.json` pour afficher tous les plugins déjà installés dans la liste.  
- **Téléchargement d’un plugin** : Lorsqu’un utilisateur entre un lien GitHub et clique sur **Télécharger**, le programme :
  1. Télécharge le plugin depuis le dépôt GitHub.  
  2. Extrait les fichiers dans `plugins/nom_plugin/`.  
  3. Exécute le script d’installation (`install.sh` ou `install.bat`) si présent.  
  4. Met à jour `plugins/instance_plugins.json` pour se souvenir du chemin du plugin.
- **Lancement d’un plugin** : Double-cliquer sur un plugin dans la liste lance automatiquement le fichier principal du plugin (`nom_plugin.py`) avec le Python de l’environnement virtuel `.venv`.
- **Mémorisation des chemins** : Tous les plugins installés sont stockés dans le dossier `plugins` et leurs chemins sont sauvegardés dans `plugins/instance_plugins.json`. Ainsi, le programme se souvient des plugins même après fermeture.

### Fonctionnalités
- Voir tous les plugins installés  
- Lancer un plugin en un clic  
- Ajouter de nouveaux plugins depuis GitHub automatiquement  

### Utilisation

**Voir les plugins**  
- Les plugins installés apparaissent à gauche dans la liste **Plugins :**  
- Cliquez sur **Actualiser** pour mettre à jour la liste si nécessaire.

**Lancer un plugin**  
- Double-cliquez sur le plugin dans la liste pour l’exécuter.

**Ajouter un plugin depuis GitHub**  
1. Copier le lien du dépôt GitHub du plugin.  
   - Exemple de lien correct :  
     ```
     https://github.com/utilisateur/nom_plugin
     ```
   - Le dépôt doit contenir :
     - un fichier principal `nom_plugin.py`
     - un script d’installation optionnel (`install.sh` ou `install.bat`)
2. Coller le lien dans le champ sous la liste des plugins.  
3. Cliquer sur **Télécharger**.  
4. Attendre que le plugin s’installe et cliquer sur **Actualiser** si nécessaire.

**Où sont stockés les plugins**  
- Tous les plugins sont dans le dossier **plugins** du programme.  
- Le programme mémorise automatiquement les chemins dans **plugins/instance_plugins.json**, donc ils restent accessibles après la fermeture du programme.

**Résumé rapide :**  
- **Double-cliquer** → lancer un plugin  
- **Entrer un lien + Télécharger** → ajouter un plugin  
- **Actualiser** → mettre à jour la liste

![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/image.png?raw=true)

---

## 🐾 Anime Sama 
![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/logo.png)

# Module Anime-Sama 📚
[Somaine 📑](#-sommaire)
Le module **Anime-Sama** est conçu pour **télécharger des scans** provenant du site Anime-Sama.

## Interface 🪟

L’interface comporte plusieurs boutons et sections, chacun ayant une fonction précise.

### Boutons principaux 🟢

En haut à gauche, on trouve plusieurs boutons permettant de lancer différentes applications liées au téléchargement de scans :

* **MangaV3** : Application pour **télécharger des scans manuellement**.
* **PDV2** : Application pour **créer des PDF** à partir d’images.
* **ShareV2** : Application pour **rechercher le nombre de pages** d’un ou plusieurs chapitres d’un manga.
* **APPV2** : L’**application principale**, permettant de **télécharger les scans rapidement et facilement**.

### Bouton Actualiser 🔄

En bas de la fenêtre, un bouton **Actualiser** permet de :

* Mettre à jour la liste des scans et chapitres disponibles,
* Fonctionne de la même manière que le bouton d’actualisation de l’interface principale du projet dans le **Launcher**.

## Application de c'est fentre anime-sama:

- 1 **MangaV3**
- 2 **ShareV2**
- 3 **APPV2**
---

### 🪢 Manga

MangaV3 est une base de l'application Anime-Sama. Elle permet de télécharger des scans de manière *manuelle* en utilisant un lien, ainsi qu’en renseignant le nombre de pages par chapitre.

### Interface 🪟

* Une zone pour **entrer le titre du manga**, qui servira de nom pour le dossier accueillant le téléchargement des chapitres.
* Une zone pour **entrer le lien du scan** à télécharger.
* Un bouton **Choisir le dossier principal** pour sélectionner l’emplacement où le dossier de téléchargement sera créé.
* Une **barre de téléchargement** pour suivre l’avancement du téléchargement en cours.
* Un bouton **Télécharger** pour lancer le téléchargement.

### Fonctionnement ⚙️

MangaV3 fonctionne en suivant un processus simple et guidé pour télécharger les chapitres d’un manga depuis un lien modèle. Voici les étapes principales :

1. **Sélection du dossier principal**
   L’utilisateur commence par choisir un dossier sur son ordinateur où seront créés tous les fichiers du manga téléchargé. MangaV2 crée ensuite un sous-dossier portant le nom du manga pour y ranger tous les chapitres.


2 **Téléchargement automatique des pages**

   * Pour chaque chapitre, MangaV3 crée un sous-dossier spécifique.
   * Chaque page est téléchargée à partir du lien généré en remplaçant `CHAP` et `NUM` par les valeurs appropriées.
   * Une barre de progression et un compteur indiquent en temps réel l’avancement du téléchargement total.

3. **Entrée des informations du manga**

   * **Titre du manga** : sert à nommer le dossier contenant tous les chapitres.
   * **Lien modèle** : un lien de téléchargement contenant deux placeholders importants :

     * `CHAP` pour le numéro du chapitre
     * `NUM` pour le numéro de la page dans le chapitre
       Cela permet à l’application de générer automatiquement les URL des images pour chaque page de chaque chapitre.
       
4. **Définition des chapitres à télécharger**
   L’utilisateur peut choisir :

   * Un intervalle précis de chapitres (début → fin)
   * Ou un chapitre de départ avec un nombre de chapitres à télécharger



5. **Définition du nombre de pages par chapitre**
   Une fenêtre s’ouvre pour que l’utilisateur saisisse le nombre exact de pages pour chaque chapitre. Cette étape est obligatoire pour que le téléchargement s’effectue correctement.

6. **Gestion des erreurs**

   * Si une page ne peut pas être téléchargée, une fenêtre d’erreur indique le problème.
   * Les champs de saisie sont vérifiés pour éviter les valeurs invalides (ex : nombre de pages négatif).

7. **Finalisation**
   Une fois tous les chapitres téléchargés, une notification indique que le processus est terminé et la barre de progression est réinitialisée.

Bien sûr ! Voici une version corrigée et clarifiée de ton texte **ShareV2**, avec la partie « Fonctionnement » rédigée de manière complète en s’appuyant sur ton code Python. J’ai corrigé les fautes, amélioré la lisibilité et structuré le tout proprement.

---

### 🔍 ShareV2

**ShareV2** est un programme qui permet de **trouver le nombre de pages dans un scan de manga**. Cette application sert principalement à **faciliter le téléchargement via l’application MangaV3**.

### Interface 🪟

* Une zone pour **saisir le nom du scan** (nom du manga).
* Un bouton pour **ouvrir le lien lié au titre**.

  * Si rien ne s’ouvre, le lien ou le titre est incorrect.
* Une zone pour **entrer les chapitres** que le programme doit traiter.
* Un bouton pour **lancer la recherche du nombre de pages** pour les chapitres sélectionnés.
* Une liste affichant les **chapitres ajoutés**.
* Un bouton pour **supprimer le dossier temporaire** créé lors de la recherche.

### Fonctionnement ⚙️

Le fonctionnement de ShareV2 repose sur la logique suivante (expliquée à partir du code Python) :

1. **Lecture du domaine du site**

   * Le programme lit un fichier JSON (`domaine.json`) pour connaître le domaine actuel du site Anime-sama.
   * Si le fichier est absent ou corrompu, le domaine par défaut `"si"` est utilisé.

2. **Création du lien vers le scan**

   * Le nom du manga est formaté en **minuscules** et les accents sont remplacés par des lettres simples (`é` → `e`, `à` → `a`, etc.).
   * Les espaces sont remplacés par des tirets (`-`) pour générer une URL valide sur Anime-sama.

3. **Gestion des chapitres**

   * L’utilisateur peut saisir plusieurs chapitres séparés par des **espaces ou des virgules**.
   * Les chapitres sont ajoutés à une liste interne et affichés dans la zone de liste.

4. **Recherche du nombre de pages (algorithme binaire)**

   * Pour chaque chapitre, ShareV2 utilise une **recherche binaire** pour déterminer le nombre de pages :

     * On commence avec une plage de pages de 1 à 1000 (variable `MAX_PAGES_POSSIBLE`).
     * On teste si la page `mid` existe sur le serveur via une requête `HEAD`.
     * Si elle existe, la recherche continue dans la partie supérieure (`low = mid + 1`).
     * Sinon, elle continue dans la partie inférieure (`high = mid - 1`).
   * À la fin, le programme connaît **le dernier numéro de page valide** pour le chapitre.

5. **Parallélisation**

   * La recherche de pages pour plusieurs chapitres se fait **en parallèle** grâce à `ThreadPoolExecutor`, ce qui accélère grandement le processus.

6. **Stockage temporaire**

   * Les résultats sont sauvegardés dans un **dossier temporaire**, un fichier par chapitre contenant le nombre de pages.
   * L’utilisateur peut choisir de **supprimer ce dossier** via un bouton.

### Résumé du flux de travail

1. L’utilisateur saisit le nom du manga.
2. Il ajoute un ou plusieurs chapitres.
3. Il clique sur **“Trouver le nombre de pages (tous)”**.
4. ShareV2 calcule le nombre de pages pour chaque chapitre et affiche le résultat.
5. Les fichiers temporaires sont créés pour sauvegarder les résultats.
6. Optionnel : l’utilisateur peut supprimer le dossier temporaire après usage.

---

### 🔽 APPV2 

APPV2 est sans doute l'application la plus pratique de ce projet.

### Interface 🪟

Le projet comporte 2 interfaces, car cette fenêtre possède 2 onglets :

* **Onglet 1 (Finder)**

  * Une zone pour entrer le titre du scan, de la même façon que pour ShareV2.
  * Une zone pour entrer les chapitres à télécharger.
  * Un bouton pour lancer la recherche des pages.
  * Un bouton pour supprimer le dossier `Temp`.

* **Onglet 2 (Downloader)**

  * Une zone où apparaîtra le titre du manga.
  * Une zone où le lien Anime-sama apparaîtra.
  * Un bouton pour sélectionner le dossier de destination du téléchargement.
  * Une barre de progression pour suivre l’avancement du téléchargement des scans.
  * Un bouton pour lancer le téléchargement.

### Finder 🔍

Finder fonctionne de la même façon que ShareV2, il suffit de mettre le **titre exact** dans le champ *Nom de l'anime :*.

### Downloader 🔽

Downloader télécharge automatiquement les images des scans en utilisant les informations fournies en interne par la partie Finder.

---

### Fonctionnement ⚙️

L’application APPV2 fonctionne en deux grandes étapes, correspondant aux deux onglets de l’interface : **Finder** et **Downloader**.

#### 1️⃣ Finder 🔍

Le rôle du Finder est de **préparer les informations nécessaires pour le téléchargement**.

1. **Entrée du titre de l’anime**

   * L’utilisateur saisit le nom exact de l’anime dans le champ *Nom de l'anime*.
   * Le programme génère automatiquement un lien vers la page correspondante sur Anime-sama, en normalisant les accents et les espaces.

2. **Sélection des chapitres**

   * Les chapitres à télécharger sont ajoutés via le champ prévu à cet effet.
   * Il est possible de saisir plusieurs chapitres séparés par des espaces ou des virgules.
   * La liste des chapitres s’affiche dans la zone correspondante.

3. **Recherche du nombre de pages par chapitre**

   * Le Finder vérifie pour chaque chapitre combien de pages existent réellement.
   * Cette vérification est **optimisée** grâce à une recherche binaire pour éviter de tester inutilement des pages inexistantes.
   * Les résultats sont affichés dans la liste et sauvegardés dans un dossier temporaire (`_Temp`) pour utilisation par le Downloader.

4. **Suppression du dossier temporaire**

   * L’utilisateur peut supprimer le dossier temporaire une fois les informations utilisées ou si elles ne sont plus nécessaires.

#### 2️⃣ Downloader ⬇

Le Downloader utilise les informations collectées par le Finder pour **télécharger automatiquement les scans** :

1. **Affichage des informations**

   * Le titre de l’anime et un modèle d’URL pour les images sont automatiquement remplis.
   * La liste des chapitres et du nombre de pages disponibles s’affiche.

2. **Choix du dossier de destination**

   * L’utilisateur sélectionne le dossier où seront stockées les images téléchargées.
   * L’application crée automatiquement un sous-dossier pour chaque chapitre.

3. **Téléchargement des scans**

   * Chaque page est téléchargée à partir de l’URL générée dynamiquement en remplaçant les placeholders `CHAP` et `NUM`.
   * La barre de progression indique l’avancement global du téléchargement.
   * Le téléchargement se fait séquentiellement, chapitre par chapitre et page par page.

4. **Finalisation**

   * Une fois toutes les pages téléchargées, l’application informe l’utilisateur que le téléchargement est terminé.

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/image.png)

---

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png)

# 📡 Anime-Sama Domain Scraper
[Somaine 📑](#-sommaire)
Ce projet est un **scraper Python** permettant de détecter automatiquement le **domaine actif d’Anime-Sama** et d’enregistrer l’information dans un fichier JSON.

Anime-Sama change très fréquemment d’URL, ce qui rend les liens rapidement obsolètes dans les applications qui y sont connectées.
Ce script permet d’automatiser entièrement ce processus.

# ⚙️ Fonctionnement

1. Le script se rend sur le site officiel **anime-sama.pw**
2. Il analyse le code HTML à l’aide de **BeautifulSoup**
3. Il recherche le bouton **"Accéder à Anime-Sama"**
4. Il récupère l’URL active actuellement fonctionnelle
5. Il extrait **l’extension du domaine** (`.fr`, `.si`, `.com`, etc.)
6. Il enregistre cette information dans un fichier `domaine.json`

# 📁 Structure des fichiers

Le script crée automatiquement le dossier suivant (si inexistant) :

```
ND_anime_sama/
└── domaine.json
```

### Exemple de contenu de `domaine.json` :

```json
{
    "domaine": "si"
}
```

Ce fichier peut ensuite être utilisé par d’autres applications ou scripts pour construire dynamiquement l’URL Anime-Sama valide.

# ✅ Avantages

* 🔄 Détection automatique du domaine actif
* 🛠️ Plus besoin de modifier le code à chaque changement d’URL
* 📦 Format JSON simple à exploiter
* 🚀 Intégration facile dans d’autres projets

# 🆕 Version

Depuis la **V4**, la gestion des changements de domaine Anime-Sama est **entièrement automatisée**.

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/image.png)

## 🐈 MangaDex 
![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/logo.png?raw=true)
[Somaine 📑](#-sommaire)
Bien sûr ! Voici une version corrigée et légèrement améliorée de ton texte pour qu’il soit plus clair, fluide et grammaticalement correct :

---

MangaDex est une application permettant de télécharger des mangas provenant du site MangaDex. Ce programme est simple et utilise l’API du site pour effectuer les téléchargements. *Ce site contient moins de scans que Anime-Sama.*

### Interface 🪟

* Un bouton vers le module PDFV2
* Une zone de sélection de la langue entre FR et EN
* Une zone pour entrer le nom du scan recherché
* Une zone pour choisir les chapitres à télécharger
* Un bouton pour lancer le téléchargement

### Fonctionnement ⚙️
Parfait ! Avec tous les fichiers que tu as fournis, je peux te rédiger une section **Fonctionnement ⚙️** claire et détaillée pour ton document, qui explique exactement comment ton programme fonctionne, en s’appuyant sur `api.py`, `downloader.py`, `main.py` et `mangadex.py`. Voici une version adaptée :

---

### Fonctionnement ⚙️

MangaDL utilise l’API de MangaDex pour rechercher et télécharger des mangas. Le programme est structuré en plusieurs modules :

#### 1. `api.py` – Communication avec MangaDex

* **`search(title)`** : recherche un manga par son titre (max 5 résultats).
* **`chapters(manga_id, lang)`** : liste les chapitres disponibles pour un manga donné, dans la langue choisie (FR ou EN).
* **`pages(chapter_id)`** : récupère les URLs de toutes les pages d’un chapitre.

#### 2. `downloader.py` – Téléchargement des chapitres

* **`download_chapter(data, out_folder, chapter_num, cbz=True)`** : télécharge toutes les pages d’un chapitre dans un dossier local.
* Chaque chapitre est enregistré dans un dossier nommé `Chapitre_<num>` et chaque page est nommée `Page_<num>.jpg`.
* Si l’option CBZ est activée, le chapitre est automatiquement compressé en fichier `.cbz` pour une lecture facile.

#### 3. `main.py` – Interface graphique (Tkinter)

* L’application permet de :

  1. Choisir la langue des chapitres (FR ou EN).
  2. Rechercher un manga par son titre et afficher les résultats.
  3. Sélectionner les chapitres à télécharger.
  4. Lancer le téléchargement, avec une barre de progression et un retour visuel des pages téléchargées.
* Une fonctionnalité externe **PDFV2** est intégrée via un bouton, permettant de générer des PDF depuis les chapitres téléchargés.

#### 4. `mangadex.py` – Interface en ligne de commande (CLI)

* MangaDL peut également être utilisé depuis le terminal :

  * `search <titre>` : recherche un manga.
  * `chapters <manga_id>` : liste les chapitres disponibles.
  * `download <chapter_id> [-o dossier] [--cbz]` : télécharge un chapitre dans un dossier choisi, avec option CBZ.

#### 5. Processus complet

1. L’utilisateur recherche un manga ou sélectionne un manga existant.
2. L’application récupère les chapitres disponibles via l’API.
3. L’utilisateur choisit les chapitres à télécharger.
4. Le programme télécharge chaque page et crée un dossier/CBZ pour chaque chapitre.
5. La barre de progression se met à jour en temps réel.
6. À la fin, l’utilisateur reçoit une notification de succès.

![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/image.png?raw=true)



