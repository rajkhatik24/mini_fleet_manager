from core.state import TaskStatus


class Coordinator:
    def __init__(self, planner):
        self.planner = planner

    def plan_routes_to_pickups(
        self,
        robots,
        tasks,
        warehouse_map
    ) -> None:

        for robot in robots:

            if robot.assigned_task_id is None:
                continue

            task = self._get_task_by_id(
                robot.assigned_task_id,
                tasks
            )

            if task is None:
                continue

            if task.status != TaskStatus.ASSIGNED:
                continue

            pickup_position = self._get_pickup_position(
                task,
                warehouse_map
            )

            route = self.planner.plan(
                robot.position,
                pickup_position,
                warehouse_map
            )

            robot.set_route(route)

    def _get_task_by_id(
        self,
        task_id,
        tasks
    ):

        for task in tasks:
            if task.task_id == task_id:
                return task

        return None

    def _get_pickup_position(
        self,
        task,
        warehouse_map
    ):

        pickup_id = task.parameters["pickup"]
        return warehouse_map.pickup_points[pickup_id]