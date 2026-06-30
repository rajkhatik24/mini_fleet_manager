from abc import ABC, abstractmethod


class SchedulerBase(ABC):

    @abstractmethod
    def assign_tasks(self, robots, tasks, warehouse_map):
        pass

    def assign_robot_to_task(
        self,
        robot,
        task
    ):
        task.assign(robot.robot_id)
        robot.assign_task(task.task_id)