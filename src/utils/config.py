"""Configuration du jeu de bataille navale."""

GAME_CONFIG = {
    # Configuration du plateau
    "BOARD_SIZE": 10,
    
    # Configuration des boutons
    "BUTTON_STYLE": {
        'width': 3,
        'height': 1,
        'font': ('Arial', 12, 'bold'),  # Texte plus visible
        'relief': 'raised',
        'borderwidth': 2
    },

    # Configuration des navires
    "SHIPS": [
        {"name": "Porte-avions", "size": 5, "quantity": 1},
        {"name": "Croiseur", "size": 4, "quantity": 1},
        {"name": "Destroyer", "size": 3, "quantity": 2},
        {"name": "Sous-marin", "size": 2, "quantity": 2}
    ],

    # Configuration de l'interface
    "WINDOW": {
        "title": "Bataille Navale",
        "min_width": 800,
        "min_height": 600,
        "padding": 20
    },

    # Configuration des délais (en millisecondes)
     "DELAYS": {
        "computer_turn": 1000,  # Délai avant le tour de l'ordinateur
        "shot_animation": 500  # Animation de tir
    }
}