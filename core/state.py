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
    NAVIGATING = "navigating"
    PICKING = "picking"
    DROPPING = "dropping"
    DOCKING = "docking"


class TaskStatus(Enum):
    CREATED = "created"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    ACTIVE = "active"
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