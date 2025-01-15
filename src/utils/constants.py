"""Constantes utilisées dans le jeu de bataille navale."""

# Couleurs utilisées dans l'interface
COLORS = {
    'bg': '#E6E6FA',          # Couleur de fond (lavande clair)
    'button': '#FFFFFF',      # Boutons (blanc)
    'hit': '#FF4444',         # Tir réussi (rouge)
    'miss': '#4444FF',        # Tir manqué (bleu)
    'ship': '#666666',        # Navire (gris)
    'preview_ok': '#90EE90',  # Prévisualisation valide (vert clair)
    'preview_bad': '#FFB6C1', # Prévisualisation invalide (rose)
    'hover': '#E0E0E0'        # Survol (gris clair)
}

# Messages affichés pendant le jeu
MESSAGES = {
    'welcome': (
        "Bienvenue dans la Bataille Navale!\n"
        "Placez vos navires sur le plateau de gauche."
    ),
    'place_ship': (
        "Placez votre {} ({} cases)\n"
        "Clic gauche pour placer, clic droit pour pivoter"
    ),
    'your_turn': "À vous de jouer! Cliquez sur le plateau ennemi pour tirer.",
    'computer_turn': "Tour de l'ordinateur...",
    'hit': "Touché!",
    'miss': "Manqué!",
    'sunk': "Coulé! Le {} est détruit!",
    'victory': "Félicitations! Vous avez gagné!",
    'defeat': "Game Over! L'ordinateur a gagné!",
    'play_again': "Voulez-vous faire une nouvelle partie?",
    'error': {
        'invalid_position': "Position invalide!",
        'already_shot': "Vous avez déjà tiré ici!"
    }
}

# État des cases du plateau
CELL_STATES = {
    'EMPTY': 0,    # Case vide
    'SHIP': 1,     # Case occupée par un navire
    'HIT': 2,      # Tir réussi
    'MISS': 3,     # Tir manqué
    'SUNK': 4      # Navire coulé
}

# Couleurs utilisées pour chaque type de navire
SHIP_COLORS = {
    'Porte-avions': '#666666',  
    'Croiseur': '#666666',      
    'Destroyer': '#666666',     
    'Sous-marin': '#666666'     
}

# Symboles utilisés pour représenter les navires
# Symboles utilisés pour représenter les navires
SHIP_SYMBOL = "■"  # Caractère Unicode pour le navire
WATER_SYMBOL = "~"  # Caractère pour l'eau
HIT_SYMBOL = "X"    # Caractère pour les tirs réussis
MISS_SYMBOL = "O"   # Caractère pour les tirs manqués
