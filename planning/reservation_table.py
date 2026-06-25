from core.types import Path, Position, RobotID


class ReservationTable:
    def __init__(self):
        self.vertex_reservations: dict[tuple[Position, int], RobotID] = {}
        self.edge_reservations: dict[tuple[Position, Position, int], RobotID] = {}

    def reserve_path(
        self,
        robot_id: RobotID,
        path: Path,
        start_time: int = 0
    ) -> None:

        if not path:
            return

        previous_position = None

        for index, position in enumerate(path):
            time_step = start_time + index

            self.vertex_reservations[(position, time_step)] = robot_id

            if previous_position is not None:
                self.edge_reservations[
                    (previous_position, position, time_step)
                ] = robot_id

            previous_position = position

    def is_vertex_reserved(
        self,
        position: Position,
        time_step: int
    ) -> bool:

        return (position, time_step) in self.vertex_reservations

    def is_edge_reserved(
        self,
        from_position: Position,
        to_position: Position,
        time_step: int
    ) -> bool:

        opposite_edge = (
            to_position,
            from_position,
            time_step
        )

        return opposite_edge in self.edge_reservations

    def is_move_allowed(
        self,
        from_position: Position,
        to_position: Position,
        time_step: int
    ) -> bool:

        if self.is_vertex_reserved(to_position, time_step):
            return False

        if self.is_edge_reserved(from_position, to_position, time_step):
            return False

        return True

    def clear(self) -> None:
        self.vertex_reservations.clear()
        self.edge_reservations.clear()