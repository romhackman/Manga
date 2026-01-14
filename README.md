# Manga Downloader V5 🌐📚

![Logo Manga Downloader](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png?raw=true)

**Bonjour, je suis Romh@ckman !**  
Je développe une application Python open-source pour **télécharger facilement les meilleurs scans de mangas** depuis [Anime Sama](https://anime-sama.si) et [MangaDex](https://mangadex.org), gratuitement !

---

## 🚀 Fonctionnalités

- Télécharger les derniers chapitres de mangas depuis Anime Sama et MangaDex  
- Interface simple et conviviale  
- Open-source : vous pouvez contribuer ou l’améliorer  
- Fonctionne sur Windows et Linux via un exécutable prêt à l’emploi  
- Ajouter facilement des plugins  
- Mise à jour automatique du nom de domaine de Anime Sama

---

## 💻 Téléchargement

Accédez au dépôt GitHub pour **télécharger l’application et le code source** :

[Manga Downloader Installer sur GitHub](https://github.com/romhackman/Manga_Downloader_installer/blob/main/install_Manga_V4_win_linux.py)

---

## ⚠️ Attention

Je décline toute responsabilité quant à l’utilisation et au contenu des fichiers téléchargés. Ces programmes sont destinés à un usage strictement personnel. Certains contenus peuvent enfreindre les droits d’auteur ou soulever des questions éthiques et légales. L’utilisateur est seul responsable de l’usage qu’il en fait et des éventuelles conséquences légales.

---

# Sommaire
- [Launcher 📕](#launcher)
  - [Configuration ⚙️](#configuration)
  - [Plugins 🧩](#plugins)
  - [PDF V2 📜](#pdf-v2)
  - [Anime-Sama 🐾](#anime-sama)
  - [MangaDex 🐈](#mangadex)
  - [Actualiser 🔄](#actualiser)
- [Plugins 🧩](#plugins-1)
- [Anime-Sama 🐾](#anime-sama-1)
- [MangaDex 🐈](#mangadex-1)

---

## Launcher 📕
![Launcher](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/home/logo.png?raw=true)

Le **Launcher** est l'interface principale de cette application. Il permet d'accéder rapidement à vos mangas favoris et à tous les modules et fonctionnalités disponibles.

### Configuration ⚙️
*Permet de définir le dossier principal pour vos mangas. Au premier lancement, le programme vous demande de sélectionner un dossier où tous vos mangas seront téléchargés. Si vous annulez, un dossier par défaut sera créé dans le dossier Launcher. Les informations sur ce dossier sont stockées dans un fichier JSON. Vous pouvez changer le dossier de destination à tout moment en cliquant à nouveau sur ce bouton.*

### Plugins 🧩
*Ce module permet d'ajouter des sites supplémentaires pour télécharger des mangas autres que Anime-Sama et MangaDex. Il est également possible de créer des extensions sans toucher au code de l'application. Le fonctionnement complet, du téléchargement à la création de plugins, [est détaillé dans le manuel, section Plugins](#plugins-1).*

### PDF V2 📜
*Ce module rend la lecture de toutes les images de vos mangas plus simple et agréable. Vous pouvez faire défiler vos mangas page par page, ce qui améliore grandement le confort de lecture.*

### Anime-Sama 🐾
*Anime-Sama permet de télécharger des scans provenant de ce site, ce qui est normalement impossible. Le module propose également d'autres fonctionnalités pour faciliter le téléchargement de vos scans. Tous les détails sont disponibles dans [le manuel, section Anime-Sama](#anime-sama-1).*

### MangaDex 🐈
*MangaDex permet de télécharger facilement des scans provenant de MangaDex. Ce module est un peu plus complexe qu’Anime-Sama mais contient moins de scans en stock. Son fonctionnement est détaillé dans [le manuel, section MangaDex](#mangadex-1).*

### Actualiser 🔄
*Ce bouton permet de rafraîchir la liste de vos mangas. Cette action est également effectuée automatiquement à chaque ouverture du Launcher.*

---
## Plugins 🧩
![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/logo.png?raw=true)

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

## Anime-Sama 🐾
![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/logo.png)
![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/image.png)

---

## MangaDex 🐈
![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/logo.png?raw=true)
![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/image.png?raw=true)
