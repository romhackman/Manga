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

* Télécharger les derniers chapitres de mangas depuis Anime Sama et MangaDex
* Interface simple et conviviale
* Open-source : vous pouvez contribuer ou l’améliorer
* Fonctionne sur Windows et Linux via un exécutable prêt à l’emploi
* Ajouter facilement des plugins
* Mise à jour automatique du nom de domaine de Anime Sama
* Mise à jour automatique de ce projet

---

## 💻 Téléchargement

Accédez au dépôt GitHub pour **télécharger l’application et le code source** :

[Manga Downloader Installer sur GitHub](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Install_Manga_V5_win_linux.py)

---

## ⚠️ Avertissement légal

Ce projet est fourni **à titre éducatif et technique uniquement**, pour expérimenter et apprendre le code.

**Important :**

* L’utilisateur est **entièrement responsable** de l’utilisation de ce logiciel et des fichiers téléchargés.
* **Aucun fichier protégé par le droit d’auteur n’est fourni avec ce programme.** Tout contenu protégé téléchargé via ce logiciel relève de la **responsabilité exclusive de l’utilisateur**.
* Le logiciel est fourni “tel quel”, sans aucune garantie. L’auteur **décline toute responsabilité** pour les dommages, pertes de données ou infractions légales pouvant résulter de l’usage de ce logiciel.
* Ces programmes sont destinés à un usage strictement personnel.

**Résumé :** Vous utilisez ce logiciel **à vos risques et périls**.

---

## 📜 Licence

Ce projet est sous **[Licence MIT](LICENSE)**.

---

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

Le **Launcher** est l’interface principale de l’application. Il permet d’accéder rapidement à vos mangas favoris ainsi qu’à tous les modules et fonctionnalités disponibles.

### Configuration ⚙️

Ce module permet de définir le **dossier principal** pour vos mangas.

* Au premier lancement, le programme vous demande de sélectionner un dossier où tous vos mangas seront téléchargés.
* Si vous annulez, un dossier par défaut sera créé dans le dossier Launcher.
* Les informations sur ce dossier sont stockées dans un fichier JSON.
* Vous pouvez changer le dossier de destination à tout moment en cliquant de nouveau sur ce bouton.

### Plugins 🧩

Ce module permet d’**ajouter des sites supplémentaires** pour télécharger des mangas autres que Anime-Sama et MangaDex.

* Il est également possible de créer des extensions sans modifier le code de l’application.
* Le fonctionnement complet, du téléchargement à la création de plugins, est détaillé dans [le manuel, section Plugins](#-plugins).

### PDF V2 📜

Ce module facilite la lecture des images de vos mangas :

* Faites défiler vos mangas page par page, pour un confort de lecture optimal.

### Anime-Sama 🐾

Ce module permet de télécharger des scans provenant de **Anime-Sama**, avec des fonctionnalités supplémentaires pour gérer les téléchargements.

* Tous les détails sont disponibles dans [le manuel, section Anime-Sama](#-anime-sama).

### MangaDex 🐈

Ce module permet de télécharger des scans depuis **MangaDex**.

* Son fonctionnement est légèrement plus complexe qu’Anime-Sama, mais il offre un accès direct aux scans disponibles sur le site.
* Le détail complet se trouve dans [le manuel, section MangaDex](#-mangadex).

### Actualiser 🔄

Ce bouton permet de **rafraîchir la liste de vos mangas**.

* Cette action est également effectuée automatiquement à chaque ouverture du Launcher.

---

## 🧩 Plugins

![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/logo.png?raw=true)
[Somaine 📑](#-sommaire)

Ce programme est un **gestionnaire de plugins**. Il permet de **télécharger, installer et lancer facilement des plugins depuis GitHub**, sans avoir besoin de manipuler des fichiers ou des commandes.

### Comment fonctionne le programme

* **Affichage des plugins** :
  Le programme lit le fichier `plugins/instance_plugins.json` pour afficher tous les plugins déjà installés.
* **Téléchargement d’un plugin** :
  Lorsqu’un utilisateur entre un lien GitHub et clique sur **Télécharger**, le programme :

  1. Télécharge le plugin depuis le dépôt GitHub.
  2. Extrait les fichiers dans `plugins/nom_plugin/`.
  3. Exécute le script d’installation (`install.sh` ou `install.bat`) si présent.
  4. Met à jour `plugins/instance_plugins.json` pour mémoriser le chemin du plugin.
* **Lancement d’un plugin** :
  Double-cliquer sur un plugin dans la liste lance automatiquement le fichier principal du plugin (`nom_plugin.py`) avec le Python de l’environnement virtuel `.venv`.
* **Mémorisation des chemins** :
  Tous les plugins installés sont stockés dans le dossier `plugins`, et leurs chemins sont sauvegardés dans `plugins/instance_plugins.json`, pour rester accessibles même après fermeture du programme.

### Fonctionnalités principales

* Afficher tous les plugins installés
* Lancer un plugin en un clic
* Ajouter de nouveaux plugins depuis GitHub automatiquement

### Utilisation

**Voir les plugins**

* Les plugins installés apparaissent dans la liste **Plugins :** à gauche.
* Cliquez sur **Actualiser** pour mettre à jour la liste si nécessaire.

**Lancer un plugin**

* Double-cliquez sur le plugin pour l’exécuter.

**Ajouter un plugin depuis GitHub**

1. Copier le lien du dépôt GitHub du plugin.

   * Exemple de lien correct :

     ```text
     https://github.com/utilisateur/nom_plugin
     ```
   * Le dépôt doit contenir :

     * un fichier principal `nom_plugin.py`
     * un script d’installation optionnel (`install.sh` ou `install.bat`)
2. Coller le lien dans le champ sous la liste des plugins.
3. Cliquer sur **Télécharger**.
4. Attendre la fin de l’installation et cliquer sur **Actualiser** si nécessaire.

**Où sont stockés les plugins**

* Tous les plugins sont dans le dossier **plugins** du programme.
* Le programme mémorise automatiquement les chemins dans **plugins/instance_plugins.json**, donc ils restent accessibles après la fermeture.

**Résumé rapide :**

* **Double-cliquer** → lancer un plugin
* **Entrer un lien + Télécharger** → ajouter un plugin
* **Actualiser** → mettre à jour la liste

**💡 Avertissement légal :**
L’utilisateur est entièrement responsable des plugins installés et de leur contenu. Le programme ne vérifie pas les fichiers des plugins et décline toute responsabilité pour tout problème ou contenu illégal provenant des plugins.

![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/image.png?raw=true)

---


## 🐾 Anime-Sama

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/logo.png)
[Somaine 📑](#-sommaire)

Le module **Anime-Sama** permet de **télécharger des scans** depuis le site Anime-Sama et propose plusieurs applications intégrées pour faciliter la gestion et le téléchargement des mangas.

---

### Interface générale 🪟

L’interface se compose de plusieurs boutons et sections :

#### Boutons principaux 🟢

* **MangaV3** : Télécharger des scans **manuellement**.
* **PDV2** : Créer des **PDF** à partir d’images.
* **ShareV2** : Rechercher le **nombre de pages** d’un ou plusieurs chapitres.
* **APPV2** : Application principale pour **télécharger rapidement les scans**.

#### Bouton Actualiser 🔄

* Met à jour la liste des scans et chapitres disponibles.
* Fonctionne comme le bouton d’actualisation du Launcher.

---

### 🪢 MangaV3

**MangaV3** est l’outil de base pour télécharger des scans manuellement à partir d’un **lien modèle**.

**Interface 🪟**

* Champ pour **entrer le titre du manga**, utilisé comme nom du dossier de téléchargement.
* Champ pour **entrer le lien du scan**.
* Bouton **Choisir le dossier principal** pour définir l’emplacement de téléchargement.
* Barre de progression pour suivre le téléchargement.
* Bouton **Télécharger** pour lancer l’opération.

**Fonctionnement ⚙️**

1. **Sélection du dossier principal** : Création d’un sous-dossier pour chaque manga.
2. **Téléchargement automatique des pages** : Chaque chapitre a son propre sous-dossier, et chaque page est récupérée depuis le lien modèle (`CHAP` → numéro de chapitre, `NUM` → numéro de page).
3. **Entrée des informations** :

   * Titre du manga → nom du dossier.
   * Lien modèle → génère automatiquement les URL des pages.
4. **Définition des chapitres à télécharger** : Intervalle ou nombre de chapitres à partir d’un départ choisi.
5. **Nombre de pages par chapitre** : L’utilisateur doit entrer le nombre exact de pages pour chaque chapitre.
6. **Gestion des erreurs** : Notifications en cas de pages manquantes ou saisies invalides.
7. **Finalisation** : Notification de fin de téléchargement et réinitialisation de la barre de progression.

---

### 🔍 ShareV2

**ShareV2** permet de **déterminer le nombre de pages par chapitre**, utile pour MangaV3 et APPV2.

**Interface 🪟**

* Champ pour **saisir le nom du scan**.
* Zone pour entrer les chapitres à traiter.
* Liste affichant les chapitres ajoutés.
* Boutons pour lancer la recherche des pages et supprimer les fichiers temporaires.

**Fonctionnement ⚙️**

1. Lecture du domaine actuel d’Anime-Sama depuis un fichier JSON (`domaine.json`).
2. Génération du lien vers le scan (normalisation des accents et des espaces).
3. Gestion des chapitres saisis par l’utilisateur.
4. Recherche du nombre de pages par chapitre via **recherche binaire**, pour optimiser le processus.
5. Exécution en parallèle pour plusieurs chapitres avec `ThreadPoolExecutor`.
6. Sauvegarde temporaire des résultats dans des fichiers par chapitre, supprimables par l’utilisateur.

---

### 🔽 APPV2

**APPV2** est l’outil principal et combine **Finder** et **Downloader**.

#### Onglet 1 : Finder 🔍

* Prépare les informations pour le téléchargement.
* Saisie du titre exact du manga et des chapitres à télécharger.
* Recherche du nombre de pages par chapitre avec optimisation binaire.
* Création d’un dossier temporaire `_Temp` pour stocker les informations.

#### Onglet 2 : Downloader ⬇

* Utilise les données de Finder pour télécharger automatiquement les scans.
* Affichage du titre, lien modèle, liste des chapitres et nombre de pages.
* Sélection du dossier de destination, création automatique de sous-dossiers par chapitre.
* Téléchargement page par page avec barre de progression.
* Notification à la fin du téléchargement.

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/image.png)

---

💡 **Avertissement légal :**
L’utilisateur est **entièrement responsable** du contenu téléchargé depuis Anime-Sama. Le logiciel ne vérifie pas le respect des droits d’auteur et **décline toute responsabilité** pour tout usage illégal ou violation de copyright.

---
Voici une version **réécrite et clarifiée** de ta section *Anime-Sama Domain Scraper*, en gardant le contenu technique mais avec une structure uniforme, plus lisible et une mention légale pour rester cohérent avec le reste du README :

---

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png)

# 📡 Anime-Sama Domain Scraper

[Somaine 📑](#-sommaire)

Le **Anime-Sama Domain Scraper** est un **script Python** qui détecte automatiquement le **domaine actif d’Anime-Sama** et enregistre l’information dans un fichier JSON.

Anime-Sama change fréquemment de domaine, ce qui rend les liens rapidement obsolètes dans les applications connectées. Ce script automatise entièrement cette tâche pour que vos autres modules (MangaV3, ShareV2, APPV2) utilisent toujours une URL valide.

---

## ⚙️ Fonctionnement

1. Le script se connecte au site officiel **anime-sama.pw**.
2. Analyse le code HTML avec **BeautifulSoup**.
3. Recherche le bouton **"Accéder à Anime-Sama"**.
4. Récupère l’URL active actuellement fonctionnelle.
5. Extrait **l’extension du domaine** (`.fr`, `.si`, `.com`, etc.).
6. Sauvegarde l’information dans le fichier `domaine.json`.

---

## 📁 Structure des fichiers

Le script crée automatiquement le dossier suivant si nécessaire :

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

Ce fichier peut ensuite être utilisé par d’autres applications ou scripts pour construire dynamiquement l’URL valide d’Anime-Sama.

---

## ✅ Avantages

* 🔄 Détection automatique du domaine actif
* 🛠️ Plus besoin de modifier le code à chaque changement d’URL
* 📦 Format JSON simple à exploiter
* 🚀 Intégration facile dans d’autres projets Python

---

## 🆕 Historique

Depuis la **V4**, la gestion des changements de domaine Anime-Sama est **entièrement automatisée**.

---

💡 **Avertissement légal :**
L’utilisateur est **entièrement responsable** de l’usage du scraper et des contenus accessibles via le domaine Anime-Sama. Ce script est fourni **à titre éducatif et technique uniquement**, et **l’auteur décline toute responsabilité** en cas de violation de droits d’auteur ou d’utilisation illégale.

---

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/image.png)

---

![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/logo.png?raw=true)

# 🐈 MangaDex

[Somaine 📑](#-sommaire)

**MangaDex** est un module permettant de télécharger des mangas depuis le site MangaDex. L’application utilise l’API officielle du site pour récupérer les chapitres et les pages.

> Note : MangaDex contient généralement moins de scans que Anime-Sama.

---

## Interface 🪟

* Bouton vers le module **PDFV2** pour générer des PDF à partir des chapitres.
* Sélecteur de langue : **FR** ou **EN**.
* Champ pour saisir le **nom du manga** recherché.
* Zone pour choisir les **chapitres à télécharger**.
* Bouton pour **lancer le téléchargement** avec suivi visuel.

---

## Fonctionnement ⚙️

Le module MangaDex est structuré en plusieurs composants :

### 1️⃣ `api.py` – Communication avec MangaDex

* **`search(title)`** : recherche un manga par titre (max 5 résultats).
* **`chapters(manga_id, lang)`** : liste les chapitres disponibles pour un manga donné dans la langue sélectionnée.
* **`pages(chapter_id)`** : récupère toutes les URLs des pages d’un chapitre.

### 2️⃣ `downloader.py` – Téléchargement

* **`download_chapter(data, out_folder, chapter_num, cbz=True)`** : télécharge toutes les pages d’un chapitre dans un dossier local.
* Chaque chapitre est sauvegardé dans un dossier `Chapitre_<num>` et chaque page nommée `Page_<num>.jpg`.
* Option **CBZ** : compresse automatiquement le chapitre en fichier `.cbz` pour une lecture facilitée.

### 3️⃣ `main.py` – Interface graphique (Tkinter)

* Permet de choisir la langue, rechercher un manga et sélectionner les chapitres.
* Affiche une barre de progression pour suivre l’avancement du téléchargement.
* Intègre **PDFV2** pour générer des fichiers PDF depuis les chapitres téléchargés.

### 4️⃣ `mangadex.py` – Interface CLI

* MangaDex peut également être utilisé depuis le terminal :

  * `search <titre>` : recherche un manga.
  * `chapters <manga_id>` : liste les chapitres disponibles.
  * `download <chapter_id> [-o dossier] [--cbz]` : télécharge un chapitre dans le dossier choisi, avec option CBZ.

### 5️⃣ Processus complet

1. L’utilisateur recherche ou sélectionne un manga.
2. L’application récupère les chapitres via l’API.
3. L’utilisateur choisit les chapitres à télécharger.
4. Le programme télécharge chaque page et crée un dossier/CBZ pour chaque chapitre.
5. La barre de progression s’actualise en temps réel.
6. À la fin, une notification indique la réussite du téléchargement.

---

![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/image.png?raw=true)

💡 **Avertissement légal :**
Le téléchargement de contenu depuis MangaDex doit respecter les droits d’auteur. **L’utilisateur est seul responsable** de l’usage qu’il fait des fichiers téléchargés. Ce module est fourni **à titre éducatif et technique uniquement**, et **l’auteur décline toute responsabilité** en cas d’usage illégal.




