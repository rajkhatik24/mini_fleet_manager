from core.state import TaskStatus
from scheduling.scheduler_base import SchedulerBase


class NearestRobotScheduler(SchedulerBase):

    def assign_tasks(self, robots, tasks, warehouse_map):
        assignments = {}

        available_robots = [
            robot for robot in robots
            if robot.is_available()
        ]

        pending_tasks = [
            task for task in tasks
            if task.status == TaskStatus.CREATED
        ]

        pending_tasks.sort(
            key=self._get_task_priority,
            reverse=True
        )

        for task in pending_tasks:

            if not available_robots:
                break

            pickup_position = self._get_pickup_position(
                task,
                warehouse_map
            )

            best_robot = self._find_nearest_robot(
                available_robots,
                pickup_position
            )

            self.assign_robot_to_task(
                best_robot,
                task
            )

            assignments[task.task_id] = best_robot.robot_id
            available_robots.remove(best_robot)

        return assignments

    def _get_task_priority(self, task):
        return task.priority

    def _get_pickup_position(self, task, warehouse_map):
        pickup_id = task.parameters["pickup"]
        return warehouse_map.pickup_points[pickup_id]

    def _find_nearest_robot(self, robots, pickup_position):
        best_robot = None
        best_distance = float("inf")

        for robot in robots:
            distance = self._manhattan_distance(
                robot.position,
                pickup_position
            )

            if distance < best_distance:
                best_distance = distance
                best_robot = robot

        return best_robot

    def _manhattan_distance(self, position_a, position_b):
        x1, y1 = position_a
        x2, y2 = position_b

        return abs(x1 - x2) + abs(y1 - y2)