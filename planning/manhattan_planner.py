# planning/manhattan_planner.py

from core.types import Path, Position
from core.warehouse_map import WarehouseMap
from planning.planner_base import PlannerBase


class ManhattanPlanner(PlannerBase):

    def plan(
        self,
        start: Position,
        goal: Position,
        warehouse_map: WarehouseMap
    ) -> Path:

        path: Path = []

        current_x, current_y = start
        goal_x, goal_y = goal

        while current_x != goal_x:
            if current_x < goal_x:
                current_x += 1
            else:
                current_x -= 1

            next_position = (current_x, current_y)

            if warehouse_map.is_walkable(next_position):
                path.append(next_position)
            else:
                return []

        while current_y != goal_y:
            if current_y < goal_y:
                current_y += 1
            else:
                current_y -= 1

            next_position = (current_x, current_y)

            if warehouse_map.is_walkable(next_position):
                path.append(next_position)
            else:
                return []

        return path