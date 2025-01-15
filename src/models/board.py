from typing import List, Optional, Tuple, Set
from .ship import Ship

class Board:
    """Représente un plateau de jeu de bataille navale."""

    def __init__(self, size: int = 10):
        """Initialise un nouveau plateau.

        Args:
            size (int): Taille du plateau (par défaut 10x10).
        """
        self.size = size
        self.ships: List[Ship] = []
        self.sunken_ships: List[Ship] = []
        self.shots: Set[Tuple[int, int]] = set()
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def can_place_ship(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        """Vérifie si un navire peut être placé à une position donnée.

        Args:
            ship (Ship): Le navire à placer.
            x (int): Coordonnée x.
            y (int): Coordonnée y.
            horizontal (bool): True pour placement horizontal, False pour vertical.

        Returns:
            bool: True si le placement est possible.
        """
        if horizontal:
            if x < 0 or x + ship.size > self.size or y < 0 or y >= self.size:
                return False
            return all(self.grid[y][x + i] is None for i in range(ship.size))
        else:
            if y < 0 or y + ship.size > self.size or x < 0 or x >= self.size:
                return False
            return all(self.grid[y + i][x] is None for i in range(ship.size))

    def place_ship(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        """Place un navire sur le plateau.

        Args:
            ship (Ship): Le navire à placer.
            x (int): Coordonnée x.
            y (int): Coordonnée y.
            horizontal (bool): True pour placement horizontal, False pour vertical.

        Returns:
            bool: True si le placement a réussi.
        """
        if not self.can_place_ship(ship, x, y, horizontal):
            return False

        positions = []
        for i in range(ship.size):
            if horizontal:
                self.grid[y][x + i] = ship
                positions.append((x + i, y))
            else:
                self.grid[y + i][x] = ship
                positions.append((x, y + i))

        ship.positions = positions
        self.ships.append(ship)
        return True

    def receive_shot(self, x: int, y: int) -> Tuple[bool, bool, Optional[Ship]]:
        """Reçoit un tir aux coordonnées données.

        Args:
            x (int): Coordonnée x du tir.
            y (int): Coordonnée y du tir.

        Returns:
            tuple: (déjà tiré, touché, navire coulé).
        """
        if not self.is_valid_position(x, y):
            return True, False, None

        if (x, y) in self.shots:
            return True, False, None

        self.shots.add((x, y))
        ship = self.grid[y][x]

        if ship is None:
            return False, False, None

        hit = ship.hit(x, y)
        if ship.is_sunk() and ship not in self.sunken_ships:
            self.sunken_ships.append(ship)
            return False, True, ship

        return False, True, None

    def is_valid_position(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées sont valides.

        Args:
            x (int): Coordonnée x.
            y (int): Coordonnée y.

        Returns:
            bool: True si les coordonnées sont valides.
        """
        return 0 <= x < self.size and 0 <= y < self.size

    def get_ship_at(self, x: int, y: int) -> Optional[Ship]:
        """Retourne le navire à une position donnée.

        Args:
            x (int): Coordonnée x.
            y (int): Coordonnée y.

        Returns:
            Optional[Ship]: Le navire ou None si la case est vide.
        """
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]

    def all_ships_sunk(self) -> bool:
        """Vérifie si tous les navires sur le plateau sont coulés.

        Returns:
            bool: True si tous les navires sont coulés.
        """
        return all(ship.is_sunk() for ship in self.ships)
    
    def get_cell_state(self, x: int, y: int) -> int:
        """Retourne l'état d'une case (vide, navire, touché, manqué)."""
        if not self.is_valid_position(x, y):
            return CELL_STATES['EMPTY']
        if (x, y) in self.shots:
            return CELL_STATES['HIT'] if self.grid[y][x] else CELL_STATES['MISS']
        return CELL_STATES['SHIP'] if self.grid[y][x] else CELL_STATES['EMPTY']

