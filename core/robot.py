from dataclasses import dataclass, field
from typing import Optional

from core.state import RobotExecutionState, RobotStatus
from core.types import Path, Position, RobotID, TaskID


@dataclass
class Robot:
    robot_id: RobotID
    position: Position

    battery: float = 100.0

    status: RobotStatus = RobotStatus.IDLE
    execution_state: RobotExecutionState = RobotExecutionState.NONE

    assigned_task_id: Optional[TaskID] = None

    planned_route: Path = field(default_factory=list)
    route_index: int = 0

    def is_available(self) -> bool:
        return (
            self.status == RobotStatus.IDLE
            and self.assigned_task_id is None
            and self.battery > 20.0
        )

    def assign_task(self, task_id: TaskID) -> None:
        self.assigned_task_id = task_id
        self.status = RobotStatus.EXECUTING
        self.execution_state = RobotExecutionState.NAVIGATING

    def set_route(self, route: Path) -> None:
        self.planned_route = route
        self.route_index = 0

    def move_one_step(self) -> None:
        if self.status in (
            RobotStatus.ERROR,
            RobotStatus.OFFLINE,
            RobotStatus.BLOCKED,
        ):
            return

        if not self.planned_route:
            return

        if self.route_index < len(self.planned_route):
            self.position = self.planned_route[self.route_index]
            self.route_index += 1
            self.drain_battery()

        if self.route_index >= len(self.planned_route):
            self.planned_route = []
            self.route_index = 0
            self.execution_state = RobotExecutionState.NONE

    def drain_battery(self, amount: float = 1.0) -> None:
        self.battery = max(0.0, self.battery - amount)

        if self.battery == 0.0:
            self.status = RobotStatus.ERROR
            self.execution_state = RobotExecutionState.NONE

    def mark_idle(self) -> None:
        self.status = RobotStatus.IDLE
        self.execution_state = RobotExecutionState.NONE
        self.assigned_task_id = None
        self.planned_route = []
        self.route_index = 0

    def mark_blocked(self) -> None:
        self.status = RobotStatus.BLOCKED

    def clear_blocked(self) -> None:
        if self.status == RobotStatus.BLOCKED:
            self.status = RobotStatus.EXECUTING

    def mark_offline(self) -> None:
        self.status = RobotStatus.OFFLINE
        self.execution_state = RobotExecutionState.NONE

    def __repr__(self) -> str:
        return (
            f"Robot("
            f"id={self.robot_id}, "
            f"pos={self.position}, "
            f"battery={self.battery:.1f}, "
            f"status={self.status.value}, "
            f"execution={self.execution_state.value}, "
            f"task={self.assigned_task_id}"
            f")"
        )