from heapq import heappush, heappop

from core.types import Position, Path
from core.warehouse_map import WarehouseMap
from planning.planner_base import PlannerBase


class AStarPlanner(PlannerBase):

    def heuristic(
        self,
        current: Position,
        goal: Position
    ) -> int:

        return (
            abs(current[0] - goal[0])
            + abs(current[1] - goal[1])
        )

    def reconstruct_path(
        self,
        came_from: dict,
        current: Position
    ) -> Path:

        path = []

        while current in came_from:
            path.append(current)
            current = came_from[current]

        path.reverse()

        return path

    def plan(
        self,
        start: Position,
        goal: Position,
        warehouse_map: WarehouseMap
    ) -> Path:

        if start == goal:
            return []

        open_set = []

        heappush(
            open_set,
            (
                self.heuristic(start, goal),
                start
            )
        )

        came_from = {}

        g_score = {
            start: 0
        }

        while open_set:

            _, current = heappop(open_set)

            if current == goal:
                return self.reconstruct_path(
                    came_from,
                    current
                )

            for neighbor in warehouse_map.get_neighbors(current):

                tentative_g = (
                    g_score[current] + 1
                )

                if (
                    neighbor not in g_score
                    or tentative_g < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g

                    f_score = (
                        tentative_g
                        + self.heuristic(
                            neighbor,
                            goal
                        )
                    )

                    heappush(
                        open_set,
                        (
                            f_score,
                            neighbor
                        )
                    )

        return []