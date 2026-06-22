from abc import ABC, abstractmethod

from core.types import Position, Path
from core.warehouse_map import WarehouseMap


class PlannerBase(ABC):

    @abstractmethod
    def plan(
        self,
        start: Position,
        goal: Position,
        warehouse_map: WarehouseMap
    ) -> Path:
        pass