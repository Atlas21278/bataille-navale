# 🛳️ Bataille Navale

Bienvenue dans **Bataille Navale**, un jeu classique de stratégie développé avec Python et Tkinter. Défiez l'IA et coulez tous ses navires avant qu'elle ne coule les vôtres !

---

## 🎯 Fonctionnalités

- **Placement des navires** : Placez vos navires sur la grille ou laissez l'ordinateur les positionner automatiquement.
- **Tirs interactifs** : Cliquez pour tirer sur la flotte ennemie.
- **Effets sonores** : Sons pour les tirs, les navires coulés et la victoire/défaite.
- **IA réglable** : Modes de difficulté pour l'ordinateur.

---

## 🛠️ Installation

### Prérequis
- Avoir Python 3.10 ou une version supérieure installé sur votre machine.

### Étapes
1. **Téléchargez le projet** : Clonez le dépôt Git ou téléchargez les fichiers directement.
2. **Accédez au dossier** : Ouvrez un terminal et naviguez jusqu'au dossier du projet.
3. **Installez les dépendances** : Utilisez la commande `pip install -r requirements.txt` pour installer les modules nécessaires.

### ⚠️ Dépendances supplémentaires

- **Tkinter** : Inclus par défaut avec Python. Si vous rencontrez une erreur liée à `tkinter`, installez-le.
  
4. **Lancez le jeu** : Exécutez le fichier principal `main.py` pour démarrer le jeu.

---

## 🎮 Comment jouer ?

1. Placez vos navires manuellement sur la grille ou laissez l'ordinateur les positionner automatiquement.
2. Cliquez sur les cases de la grille ennemie pour tirer.
3. Le premier joueur à couler tous les navires adverses gagne !

---

## 📂 Structure du projet

Le projet est organisé comme suit :

- **`assets/`** : Contient les fichiers audio pour les effets sonores du jeu (tirs, victoires, défaites, etc.).
- **`src/`** : Contient le code source, organisé en plusieurs sous-dossiers :
  - **`controllers/`** : Gère la logique principale du jeu.
  - **`models/`** : Définit les classes pour les navires, les joueurs et les plateaux.
  - **`utils/`** : Contient les constantes et configurations globales.
  - **`views/`** : Implémente l'interface graphique avec Tkinter.
- **`main.py`** : Le point d'entrée du projet pour démarrer le jeu.
- **`requirements.txt`** : Liste des dépendances Python nécessaires.

---

