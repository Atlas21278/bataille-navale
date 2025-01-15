from typing import List, Set, Tuple
from .board import Board
from .ship import Ship

class Player:
    """Représente un joueur dans le jeu de bataille navale."""

    def __init__(self, name: str, is_computer: bool = False):
        """Initialise un nouveau joueur.

        Args:
            name (str): Nom du joueur.
            is_computer (bool): True si c'est l'ordinateur.
        """
        self.name = name
        self.is_computer = is_computer
        self.board = Board()  # Plateau du joueur
        self.shots: Set[Tuple[int, int]] = set()  # Tirs effectués

    def initialize_ships(self) -> List[Ship]:
        """Crée la liste initiale des navires.

        Returns:
            List[Ship]: Liste des navires à placer.
        """
        return [
            Ship("Porte-avions", 5),
            Ship("Croiseur", 4),
            Ship("Destroyer 1", 3),
            Ship("Destroyer 2", 3),
            Ship("Sous-marin 1", 2),
            Ship("Sous-marin 2", 2)
        ]

    def has_lost(self) -> bool:
        """Vérifie si le joueur a perdu (tous ses navires sont coulés).

        Returns:
            bool: True si le joueur a perdu.
        """
        return all(ship.is_sunk() for ship in self.board.ships)

    def receive_shot(self, x: int, y: int) -> Tuple[bool, bool, Ship]:
        """Reçoit un tir aux coordonnées données.

        Args:
            x (int): Coordonnée x du tir.
            y (int): Coordonnée y du tir.

        Returns:
            Tuple[bool, bool, Ship]: (déjà tiré, touché, navire coulé).
        """
        return self.board.receive_shot(x, y)

    def can_shoot_at(self, x: int, y: int) -> bool:
        """Vérifie si le joueur peut tirer à ces coordonnées.

        Args:
            x (int): Coordonnée x.
            y (int): Coordonnée y.

        Returns:
            bool: True si le tir est possible.
        """
        return (x, y) not in self.shots and self.board.is_valid_position(x, y)

    def record_shot(self, x: int, y: int, hit: bool):
        """Enregistre un tir effectué.

        Args:
            x (int): Coordonnée x du tir.
            y (int): Coordonnée y du tir.
            hit (bool): True si le tir a touché.
        """
        self.shots.add((x, y))
        if hit:
            self.board.grid[y][x] = True  # Marque comme touché
        else:
            self.board.grid[y][x] = False  # Marque comme raté

    def get_remaining_ships(self) -> List[Ship]:
        """Retourne la liste des navires non coulés.

        Returns:
            List[Ship]: Liste des navires encore à flot.
        """
        return [ship for ship in self.board.ships if not ship.is_sunk()]
