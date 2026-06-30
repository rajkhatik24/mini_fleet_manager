from heapq import heappop, heappush

from core.types import Path, Position
from core.warehouse_map import WarehouseMap
from planning.planner_base import PlannerBase
from planning.reservation_table import ReservationTable


class CooperativeAStarPlanner(PlannerBase):
    def __init__(
        self,
        reservation_table: ReservationTable,
        max_time: int = 200
    ):
        self.reservation_table = reservation_table
        self.max_time = max_time

    def heuristic(
        self,
        current: Position,
        goal: Position
    ) -> int:
        return (
            abs(current[0] - goal[0])
            + abs(current[1] - goal[1])
        )

    def plan(
        self,
        start: Position,
        goal: Position,
        warehouse_map: WarehouseMap,
        start_time: int = 0
    ) -> Path:

        if start == goal:
            return []

        open_set = []

        start_state = (start, start_time)

        heappush(
            open_set,
            (
                self.heuristic(start, goal),
                start_state
            )
        )

        came_from = {}
        g_score = {
            start_state: 0
        }

        while open_set:
            _, current_state = heappop(open_set)

            current_position, current_time = current_state

            if current_position == goal:
                return self._reconstruct_path(
                    came_from,
                    current_state
                )

            if current_time >= start_time + self.max_time:
                continue

            next_time = current_time + 1

            neighbors = warehouse_map.get_neighbors(current_position)

            # Allow waiting in place
            neighbors.append(current_position)

            for neighbor in neighbors:
                if not self.reservation_table.is_move_allowed(
                    from_position=current_position,
                    to_position=neighbor,
                    time_step=next_time
                ):
                    continue

                neighbor_state = (
                    neighbor,
                    next_time
                )

                tentative_g = g_score[current_state] + 1

                if (
                    neighbor_state not in g_score
                    or tentative_g < g_score[neighbor_state]
                ):
                    came_from[neighbor_state] = current_state
                    g_score[neighbor_state] = tentative_g

                    f_score = tentative_g + self.heuristic(
                        neighbor,
                        goal
                    )

                    heappush(
                        open_set,
                        (
                            f_score,
                            neighbor_state
                        )
                    )

        return []

    def _reconstruct_path(
        self,
        came_from,
        current_state
    ) -> Path:

        path = []

        while current_state in came_from:
            position, _ = current_state
            path.append(position)
            current_state = came_from[current_state]

        path.reverse()

        return path