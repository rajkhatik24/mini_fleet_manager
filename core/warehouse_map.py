from dataclasses import dataclass, field
from typing import Set, List

from core.types import Position


@dataclass
class WarehouseMap:
    width: int
    height: int
    obstacles: Set[Position] = field(default_factory=set)

    def is_inside(self, position: Position) -> bool:
        x, y = position

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def is_obstacle(self, position: Position) -> bool:
        return position in self.obstacles

    def is_walkable(self, position: Position) -> bool:
        return (
            self.is_inside(position)
            and not self.is_obstacle(position)
        )

    def get_neighbors(self, position: Position) -> List[Position]:
        x, y = position

        possible_neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        valid_neighbors = []

        for neighbor in possible_neighbors:
            if self.is_walkable(neighbor):
                valid_neighbors.append(neighbor)

        return valid_neighbors

    def add_obstacle(self, position: Position) -> None:
        if self.is_inside(position):
            self.obstacles.add(position)

    def remove_obstacle(self, position: Position) -> None:
        self.obstacles.discard(position)

    def __repr__(self) -> str:
        return (
            f"WarehouseMap("
            f"width={self.width}, "
            f"height={self.height}, "
            f"obstacles={len(self.obstacles)}"
            f")"
        )