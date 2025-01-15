"""
Point d'entrée du jeu de bataille navale.
"""

import tkinter as tk
from src.views.game_view import GameView
import logging
import sys
import os


def configure_logging():
    """Configure le système de journalisation."""
    log_file = 'battleship.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler()
        ]
    )
    logging.info(f"Fichier de log : {os.path.abspath(log_file)}")


def main():
    """Lance le jeu de bataille navale."""
    # Configuration du logging
    configure_logging()

    # Ajout du chemin du dossier src pour éviter les erreurs d'import
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

    try:
        logging.info("Démarrage du jeu")
        
        # Vérifiez que Tkinter fonctionne
        try:
            test_window = tk.Tk()
            test_window.destroy()
            logging.info("Tkinter fonctionne correctement.")
        except Exception as tk_error:
            logging.error("Erreur avec Tkinter : Tkinter n'est pas configuré correctement.")
            raise tk_error

        # Initialisation de GameView
        logging.info("Initialisation de GameView...")
        game = GameView()
        logging.info("GameView initialisée avec succès.")
        
        # Démarrage du jeu
        logging.info("Lancement du jeu...")
        game.run()
        logging.info("Fermeture normale du jeu")
    except Exception as e:
        logging.error(f"Erreur pendant l'exécution du jeu : {str(e)}", exc_info=True)
    finally:
        logging.info("Fin de l'application")


if __name__ == "__main__":
    main()
