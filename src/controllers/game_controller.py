from typing import List, Tuple, Optional, Set
from src.models.player import Player
from src.models.ship import Ship
from src.models.board import Board
from collections import deque
import random
import logging

class GameController:
    """Contrôleur principal de la logique de jeu de bataille navale."""

    def __init__(self, difficulty: str = "normal"):
        """Initialise le contrôleur de jeu.

        Args:
            difficulty (str): Niveau de difficulté ("easy" ou "normal").
        """
        self.difficulty = difficulty
        self.player = Player("Joueur")
        self.computer = Player("Ordinateur", is_computer=True)
        self.current_turn = self.player
        
        # Attributs pour la logique de tir de l'ordinateur
        self.computer_shots: Set[Tuple[int, int]] = set()
        self.last_hit: Optional[Tuple[int, int]] = None
        self.target_queue: deque[Tuple[int, int]] = deque()
        self.successful_hits: List[Tuple[int, int]] = []

    def initialize_game(self):
        """Initialise le jeu avec les navires placés sur les plateaux."""
        logging.info("Initialisation des navires...")

        # Placement des navires du joueur (manuellement via l'interface)
        self.player.board.ships = self.player.initialize_ships()

        # Placement aléatoire des navires de l'ordinateur
        for ship in self.computer.initialize_ships():
            self.place_computer_ship_randomly(ship)

    def place_computer_ship_randomly(self, ship: Ship):
        """Place un navire de l'ordinateur de manière aléatoire.

        Args:
            ship (Ship): Le navire à placer.
        """
        placed = False
        while not placed:
            x = random.randint(0, self.computer.board.size - 1)
            y = random.randint(0, self.computer.board.size - 1)
            horizontal = random.choice([True, False])
            placed = self.computer.board.place_ship(ship, x, y, horizontal)

    def can_place_ship(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        """Vérifie si un navire peut être placé à une position donnée.

        Args:
            ship (Ship): Le navire à placer.
            x (int): Coordonnée x.
            y (int): Coordonnée y.
            horizontal (bool): True si horizontal, False si vertical.

        Returns:
            bool: True si le placement est possible.
        """
        return self.player.board.can_place_ship(ship, x, y, horizontal)

    def place_player_ship(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        """Place un navire sur le plateau du joueur.

        Args:
            ship (Ship): Le navire à placer.
            x (int): Coordonnée x.
            y (int): Coordonnée y.
            horizontal (bool): True si horizontal, False si vertical.

        Returns:
            bool: True si le placement a réussi.
        """
        return self.player.board.place_ship(ship, x, y, horizontal)

    def handle_player_shot(self, x: int, y: int) -> Tuple[bool, bool, Optional[Ship]]:
        """Gère un tir du joueur sur le plateau de l'ordinateur.

        Args:
            x (int): Coordonnée x du tir.
            y (int): Coordonnée y du tir.

        Returns:
            tuple: (déjà tiré, touché, navire coulé).
        """
        return self.computer.board.receive_shot(x, y)

    def handle_computer_shot(self) -> Tuple[int, int, bool, bool, Optional[Ship]]:
        """Gère un tir de l'ordinateur sur le plateau du joueur.

        Returns:
            tuple: (x, y, déjà tiré, touché, navire coulé).
        """
        x, y = self.get_computer_shot_coordinates()
        already_shot, hit, ship = self.player.board.receive_shot(x, y)
        
        # Met à jour la logique de tir de l'ordinateur
        self.computer_shots.add((x, y))
        if hit and not already_shot:
            if ship and ship.is_sunk():
                # Réinitialise la stratégie si le navire est coulé
                self.target_queue.clear()
                self.successful_hits.clear()
                self.last_hit = None
            else:
                # Continue le ciblage
                self.successful_hits.append((x, y))
                self.last_hit = (x, y)
                self._add_adjacent_targets(x, y)
        
        return x, y, already_shot, hit, ship

    def get_computer_shot_coordinates(self) -> Tuple[int, int]:
        """Détermine les coordonnées du prochain tir de l'ordinateur en fonction de la difficulté.

        Returns:
            tuple: Coordonnées (x, y).
        """
        if self.difficulty == "easy":
            # Mode facile : tirs aléatoires
            while True:
                x = random.randint(0, self.player.board.size - 1)
                y = random.randint(0, self.player.board.size - 1)
                if (x, y) not in self.computer_shots:
                    return x, y

        elif self.difficulty == "normal":
            # Mode normal : tirs intelligents avec ciblage
            if self.target_queue:
                return self.target_queue.popleft()

            # Si pas de cible, tir aléatoire
            while True:
                x = random.randint(0, self.player.board.size - 1)
                y = random.randint(0, self.player.board.size - 1)
                if (x, y) not in self.computer_shots:
                    return x, y

    def _add_adjacent_targets(self, x: int, y: int):
        """Ajoute les cases adjacentes à cibler."""
        # Directions possibles (haut, droite, bas, gauche)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Si on a plusieurs hits successifs, on privilégie la direction établie
        if len(self.successful_hits) >= 2:
            last_hits = self.successful_hits[-2:]
            dx = last_hits[1][0] - last_hits[0][0]
            dy = last_hits[1][1] - last_hits[0][1]
            
            if dx != 0 or dy != 0:  # Si on a une direction établie
                directions = [(dx, dy), (-dx, -dy)]  # Continue dans cette direction
        
        # Ajoute les cases adjacentes valides
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self._is_valid_target(new_x, new_y):
                self.target_queue.append((new_x, new_y))

    def _is_valid_target(self, x: int, y: int) -> bool:
        """Vérifie si une cible est valide."""
        return (0 <= x < self.player.board.size and 
                0 <= y < self.player.board.size and 
                (x, y) not in self.computer_shots)

    def check_game_over(self) -> Optional[Player]:
        """Vérifie si la partie est terminée.

        Returns:
            Optional[Player]: Le gagnant si la partie est terminée, None sinon.
        """
        if self.player.has_lost():
            return self.computer
        if self.computer.has_lost():
            return self.player
        return None