from dataclasses import dataclass, field
from typing import Any, Optional

from core.state import TaskStatus, TaskType
from core.types import RobotID, TaskID


@dataclass
class Task:
    task_id: TaskID
    task_type: TaskType

    priority: int = 1
    status: TaskStatus = TaskStatus.CREATED

    assigned_robot_id: Optional[RobotID] = None

    parameters: dict[str, Any] = field(default_factory=dict)

    created_time: float = 0.0
    start_time: Optional[float] = None
    completion_time: Optional[float] = None

    def assign(self, robot_id: RobotID) -> None:
        self.assigned_robot_id = robot_id
        self.status = TaskStatus.ASSIGNED

    def start(self) -> None:
        self.status = TaskStatus.IN_PROGRESS

    def block(self) -> None:
        self.status = TaskStatus.BLOCKED

    def complete(self) -> None:
        self.status = TaskStatus.COMPLETED

    def fail(self) -> None:
        self.status = TaskStatus.FAILED

    def cancel(self) -> None:
        self.status = TaskStatus.CANCELLED

    def is_finished(self) -> bool:
        return self.status in {
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        }

    def __repr__(self) -> str:
        return (
            f"Task("
            f"id={self.task_id}, "
            f"type={self.task_type.value}, "
            f"status={self.status.value}, "
            f"priority={self.priority}, "
            f"robot={self.assigned_robot_id}"
            f")"
        )