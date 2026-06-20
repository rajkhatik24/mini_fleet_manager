from abc import ABC, abstractmethod
from typing import Optional

from planning.planner_base import PlannerBase


class SchedulerBase(ABC):

    def __init__(self, planner: Optional[PlannerBase] = None):
        self.planner = planner

    @abstractmethod
    def assign_tasks(self, robots, tasks, warehouse_map):
        pass

    def assign_robot_to_task(
        self,
        robot,
        task,
        pickup_position,
        warehouse_map
    ):
        task.assign(robot.robot_id)
        robot.assign_task(task.task_id)

        if self.planner is not None:
            route = self.planner.plan(
                robot.position,
                pickup_position,
                warehouse_map
            )
            robot.set_route(route)