import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List
from ..controllers.game_controller import GameController
from src.models.ship import Ship
from ..utils.config import GAME_CONFIG
import logging
from ..utils.constants import COLORS, MESSAGES, SHIP_COLORS, SHIP_SYMBOL, WATER_SYMBOL, HIT_SYMBOL, MISS_SYMBOL
import pygame
import os


pygame.mixer.init()

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../../assets/sounds')

SOUNDS = {
    'shoot': pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'shoot.mp3')),
    'hit': pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'hit.wav')),
    'sunk': pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sunk.wav')),
    'victory': pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'victory.wav')),
    'defeat': pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'defeat.mp3'))
}



class GameView:
    """Interface graphique du jeu de bataille navale."""

    def __init__(self):
        """Initialise l'interface graphique."""
        logging.info("Création de l'interface graphique...")
        self.window = tk.Tk()
        self.window.title(GAME_CONFIG["WINDOW"]["title"])
        self.window.minsize(
            GAME_CONFIG["WINDOW"]["min_width"],
            GAME_CONFIG["WINDOW"]["min_height"]
        )
        self.window.configure(bg=COLORS['bg'])

        self.difficulty = tk.StringVar(value="normal")
        self.game = GameController(difficulty=self.difficulty.get())
        self.buttons_player = []
        self.buttons_computer = []
        self.current_ship = None
        self.is_horizontal = tk.BooleanVar(value=True)
        self.ships_to_place = []

        self.setup_gui()
        self.new_game()

    def setup_gui(self):
        """Configure l'interface graphique."""
        logging.info("Configuration de l'interface graphique...")
        main_frame = ttk.Frame(self.window, padding=GAME_CONFIG["WINDOW"]["padding"])
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Titre
        title = ttk.Label(
            main_frame,
            text="BATAILLE NAVALE",
            font=('Arial', 24, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Status
        self.status_label = ttk.Label(
            main_frame,
            text=MESSAGES['welcome'],
            font=('Arial', 12)
        )
        self.status_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Plateaux de jeu
        self.create_boards(main_frame)

        # Contrôles
        self.create_controls(main_frame)

    def create_controls(self, parent):
        """Crée les contrôles du jeu."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Panneau de contrôle gauche
        left_panel = ttk.Frame(control_frame)
        left_panel.pack(side=tk.LEFT, padx=20)

        # Bouton nouvelle partie
        new_game_btn = ttk.Button(
            left_panel,
            text="Nouvelle Partie",
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)

        # Contrôle de difficulté
        difficulty_frame = ttk.LabelFrame(left_panel, text="Difficulté", padding=5)
        difficulty_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            difficulty_frame,
            text="Facile",
            variable=self.difficulty,
            value="easy"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            difficulty_frame,
            text="Normal",
            variable=self.difficulty,
            value="normal"
        ).pack(side=tk.LEFT, padx=5)

        # Panneau de contrôle droite (orientation)
        right_panel = ttk.Frame(control_frame)
        right_panel.pack(side=tk.RIGHT, padx=20)
       
        ttk.Label(right_panel, text="Orientation:").pack(side=tk.LEFT)
        ttk.Checkbutton(
            right_panel,
            text="Horizontal",
            variable=self.is_horizontal
        ).pack(side=tk.LEFT)

    def show_preview(self, x: int, y: int):
        """Affiche la prévisualisation du placement d'un navire."""
        if not self.current_ship:
            return

        self.clear_preview()
        ship = self.current_ship
        horizontal = self.is_horizontal.get()

        try:
            # Vérifie si le placement est possible
            can_place = self.game.can_place_ship(ship, x, y, horizontal)
            color = COLORS['preview_ok'] if can_place else COLORS['preview_bad']
            
            # Affiche la prévisualisation
            for i in range(ship.size):
                if horizontal:
                    if x + i < GAME_CONFIG["BOARD_SIZE"]:
                        button = self.buttons_player[y][x + i]
                        if button['bg'] != COLORS['ship']:
                            button.config(bg=color)
                else:
                    if y + i < GAME_CONFIG["BOARD_SIZE"]:
                        button = self.buttons_player[y + i][x]
                        if button['bg'] != COLORS['ship']:
                            button.config(bg=color)
        except IndexError:
            pass

    def clear_preview(self):
        """Efface la prévisualisation."""
        for i in range(GAME_CONFIG["BOARD_SIZE"]):
            for j in range(GAME_CONFIG["BOARD_SIZE"]):
                button = self.buttons_player[i][j]
                if button['bg'] in [COLORS['preview_ok'], COLORS['preview_bad']]:
                    button.config(bg=COLORS['button'])
                    
    def toggle_orientation(self):
        """Change l'orientation du navire à placer."""
        self.is_horizontal.set(not self.is_horizontal.get())

    def place_ship(self, x: int, y: int):
        """Place un navire sur le plateau du joueur."""
        if not self.current_ship:
            return

        if self.game.place_player_ship(
            self.current_ship,
            x, y,
            self.is_horizontal.get()
        ):
            self.update_ship_display(x, y)
            self.prepare_next_ship()

    def update_ship_display(self, x: int, y: int):
        """Met à jour l'affichage après le placement d'un navire."""
        ship = self.current_ship
        horizontal = self.is_horizontal.get()
        ship_color = SHIP_COLORS.get(ship.name, COLORS['ship'])  # Couleur spécifique du navire

        for i in range(ship.size):
            if horizontal:
                if x + i < GAME_CONFIG["BOARD_SIZE"]:
                    self.buttons_player[y][x + i].config(
                        bg=ship_color, 
                        text=SHIP_SYMBOL  # Symbole du navire
                    )
            else:
                if y + i < GAME_CONFIG["BOARD_SIZE"]:
                    self.buttons_player[y + i][x].config(
                        bg=ship_color, 
                        text=SHIP_SYMBOL  # Symbole du navire
                    )



    def prepare_next_ship(self):
        """Prépare le placement du prochain navire."""
        if self.ships_to_place:
            self.current_ship = self.ships_to_place.pop(0)
            self.status_label.config(
                text=MESSAGES['place_ship'].format(
                    self.current_ship.name,
                    self.current_ship.size
                )
            )
        else:
            self.current_ship = None
            self.start_game()

    def player_shoot(self, x: int, y: int):
        """Gère un tir du joueur."""
        try:
            already_shot, hit, ship = self.game.handle_player_shot(x, y)
            button = self.buttons_computer[y][x]

            # Joue le son de tir
            SOUNDS['shoot'].play()

            if already_shot:
                messagebox.showinfo("Erreur", MESSAGES['error']['already_shot'])
                return

            if hit:
                button.config(bg=COLORS['hit'], text=HIT_SYMBOL)  # Tir réussi
                SOUNDS['hit'].play()  # Joue le son de tir réussi
                if ship and ship.is_sunk():
                    SOUNDS['sunk'].play()  # Joue le son de navire coulé
                    messagebox.showinfo("Touché-Coulé!", f"Vous avez coulé le {ship.name}!")
            else:
                button.config(bg=COLORS['miss'], text=MISS_SYMBOL)  # Tir manqué

            if self.check_game_over():
                return

            self.status_label.config(text="Tour de l'ordinateur...")
            self.window.after(1000, self.computer_turn)

        except Exception as e:
            logging.error(f"Erreur lors du tir du joueur : {e}", exc_info=True)



    def computer_turn(self):
        """Gère le tour de l'ordinateur."""
        try:
            x, y, _, hit, ship = self.game.handle_computer_shot()
            button = self.buttons_player[y][x]

            # Joue le son de tir
            SOUNDS['shoot'].play()

            if hit:
                button.config(bg=COLORS['hit'])
                SOUNDS['hit'].play()  # Joue le son de tir réussi
                if ship and ship.is_sunk():
                    SOUNDS['sunk'].play()  # Joue le son de navire coulé
                    messagebox.showinfo("Navire coulé", MESSAGES['sunk'].format(ship.name))
            else:
                button.config(bg=COLORS['miss'])

            if not self.check_game_over():
                self.status_label.config(text=MESSAGES['your_turn'])

        except Exception as e:
            logging.error(f"Erreur lors du tour de l'ordinateur : {e}", exc_info=True)

    def check_game_over(self) -> bool:
        """Vérifie si la partie est terminée."""
        winner = self.game.check_game_over()
        if winner:
            if winner == self.game.player:
                SOUNDS['victory'].play()  # Joue le son de victoire
                message = "Félicitations, vous avez gagné !"
            else:
                SOUNDS['defeat'].play()  # Joue le son de défaite
                message = "Dommage, l'ordinateur a gagné."
    
            if messagebox.askyesno("Fin de partie", f"{message}\nVoulez-vous rejouer ?"):
                self.new_game()
            else:
                self.window.quit()
            return True
        return False


    def new_game(self):
        """Commence une nouvelle partie."""
        self.game = GameController(difficulty=self.difficulty.get())
        self.game.initialize_game()

        for i in range(GAME_CONFIG["BOARD_SIZE"]):
            for j in range(GAME_CONFIG["BOARD_SIZE"]):
                self.buttons_player[i][j].config(bg=COLORS['button'], text=WATER_SYMBOL, state='normal')
                self.buttons_computer[i][j].config(bg=COLORS['button'], text=WATER_SYMBOL, state='disabled')

        self.ships_to_place = self.game.player.initialize_ships()
        self.current_ship = self.ships_to_place.pop(0)
        self.status_label.config(
            text=MESSAGES['place_ship'].format(
                self.current_ship.name,
                self.current_ship.size
            )
        )


    def start_game(self):
        """Commence la phase de jeu."""
        self.status_label.config(text=MESSAGES['your_turn'])
        for row in self.buttons_computer:
            for button in row:
                button.config(state='normal')

    def run(self):
        """Lance le jeu."""
        logging.info("Lancement de la boucle principale Tkinter...")
        try:
            self.window.mainloop()
            logging.info("Boucle principale terminée, fermeture de la fenêtre Tkinter.")
        except Exception as e:
            logging.error(f"Erreur dans la boucle principale Tkinter : {e}", exc_info=True)

    def create_boards(self, parent):
        """Crée les grilles de jeu avec les vagues initiales."""
        boards_frame = ttk.Frame(parent)
        boards_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Plateau joueur
        player_frame = ttk.LabelFrame(boards_frame, text="Votre flotte", padding=10)
        player_frame.grid(row=0, column=0, padx=20)

        self.buttons_player = []
        for i in range(GAME_CONFIG["BOARD_SIZE"]):
            row = []
            for j in range(GAME_CONFIG["BOARD_SIZE"]):
                btn = tk.Button(
                    player_frame,
                    **GAME_CONFIG["BUTTON_STYLE"],
                    text=WATER_SYMBOL,  # Ajoute les vagues comme texte initial
                    bg=COLORS['button']
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                btn.bind("<Enter>", lambda e, y=i, x=j: self.show_preview(x, y))
                btn.bind("<Leave>", lambda e: self.clear_preview())
                btn.bind("<Button-1>", lambda e, y=i, x=j: self.place_ship(x, y))
                btn.bind("<Button-3>", lambda e: self.toggle_orientation())
                row.append(btn)
            self.buttons_player.append(row)

        # Plateau ordinateur
        computer_frame = ttk.LabelFrame(boards_frame, text="Flotte ennemie", padding=10)
        computer_frame.grid(row=0, column=1, padx=20)

        self.buttons_computer = []
        for i in range(GAME_CONFIG["BOARD_SIZE"]):
            row = []
            for j in range(GAME_CONFIG["BOARD_SIZE"]):
                btn = tk.Button(
                    computer_frame,
                    **GAME_CONFIG["BUTTON_STYLE"],
                    text=WATER_SYMBOL,  # Ajoute les vagues comme texte initial
                    bg=COLORS['button'],
                    state='disabled'
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                btn.configure(command=lambda y=i, x=j: self.player_shoot(x, y))
                row.append(btn)
            self.buttons_computer.append(row)


    def show_hover(self, x: int, y: int):
        """Change la couleur de la case sous la souris."""
        button = self.buttons_player[y][x]
        if button['bg'] == COLORS['button']:  # Seulement si la case est vide
            button.config(bg=COLORS['hover'], text=WATER_SYMBOL)
    
    def clear_hover(self):
        """Réinitialise les couleurs après le hover."""
        for row in self.buttons_player:
            for button in row:
                if button['bg'] == COLORS['hover']:
                    button.config(bg=COLORS['button'], text="")

