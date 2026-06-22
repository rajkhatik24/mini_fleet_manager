from enum import Enum


class RobotStatus(Enum):
    IDLE = "idle"
    EXECUTING = "executing"
    WAITING = "waiting"
    BLOCKED = "blocked"
    CHARGING = "charging"
    OFFLINE = "offline"
    ERROR = "error"


class RobotExecutionState(Enum):
    NONE = "none"
    NAVIGATING_TO_PICKUP = "navigating_to_pickup"
    PICKING = "picking"
    NAVIGATING_TO_DROPOFF = "navigating_to_dropoff"
    DROPPING = "dropping"
    DOCKING = "docking"


class TaskStatus(Enum):
    CREATED = "created"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    TRANSPORT = "transport"
    MOVE = "move"
    CHARGE = "charge"
    INSPECT = "inspect"
    DELIVERY = "delivery"
    CUSTOM = "custom"