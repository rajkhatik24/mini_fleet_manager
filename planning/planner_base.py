from abc import ABC, abstractmethod

from core.types import Position, Path
from core.warehouse_map import WarehouseMap


class PlannerBase(ABC):

    @abstractmethod
    def plan(
        self,
        warehouse_map: WarehouseMap,
        start: Position,
        goal: Position,
    ) -> Path:
        pass