from typing import List, Tuple, Set

class Ship:
    """Représente un navire dans le jeu de bataille navale."""

    def __init__(self, name: str, size: int):
        """Initialise un nouveau navire.

        Args:
            name (str): Nom du navire.
            size (int): Taille du navire en cases.
        """
        self.name = name
        self.size = size
        self.positions: List[Tuple[int, int]] = []  # Coordonnées des cases occupées
        self.hits: Set[Tuple[int, int]] = set()  # Coordonnées des cases touchées

    def hit(self, x: int, y: int) -> bool:
        """Enregistre un tir sur le navire.

        Args:
            x (int): Coordonnée x du tir.
            y (int): Coordonnée y du tir.

        Returns:
            bool: True si le tir a touché une nouvelle position.
        """
        position = (x, y)
        if position in self.positions and position not in self.hits:
            self.hits.add(position)
            return True
        return False

    def is_sunk(self) -> bool:
        """Vérifie si le navire est coulé.

        Returns:
            bool: True si toutes les positions sont touchées.
        """
        return set(self.positions) == self.hits

    def get_positions(self) -> List[Tuple[int, int]]:
        """Retourne les positions occupées par le navire.

        Returns:
            List[Tuple[int, int]]: Liste des coordonnées.
        """
        return self.positions

    def __str__(self) -> str:
        """Représentation textuelle du navire.

        Returns:
            str: Description du navire.
        """
        status = "coulé" if self.is_sunk() else f"{len(self.hits)}/{self.size} touches"
        return f"{self.name} ({status})"
