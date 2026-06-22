from core.state import RobotExecutionState, TaskStatus


class TaskExecutor:
    def __init__(self, warehouse_map, tasks, planner):
        self.warehouse_map = warehouse_map
        self.tasks = tasks
        self.planner = planner

    def handle_route_finished(self, robot) -> None:
        task = self._get_task_by_id(robot.assigned_task_id)

        if task is None:
            return

        if task.status == TaskStatus.ASSIGNED:
            self._handle_reached_pickup(robot, task)

        elif task.status == TaskStatus.IN_PROGRESS:
            self._handle_reached_dropoff(robot, task)

    def _handle_reached_pickup(self, robot, task) -> None:
        print(f"Robot {robot.robot_id} reached pickup for Task {task.task_id}")

        task.start()

        robot.execution_state = RobotExecutionState.PICKING

        dropoff_position = self._get_dropoff_position(task)

        route_to_dropoff = self.planner.plan(
            robot.position,
            dropoff_position,
            self.warehouse_map
        )

        robot.set_route(route_to_dropoff)
        robot.execution_state = RobotExecutionState.NAVIGATING_TO_DROPOFF

    def _handle_reached_dropoff(self, robot, task) -> None:
        print(f"Robot {robot.robot_id} reached dropoff for Task {task.task_id}")

        robot.execution_state = RobotExecutionState.DROPPING

        task.complete()
        robot.mark_idle()

    def _get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    def _get_dropoff_position(self, task):
        dropoff_id = task.parameters["dropoff"]
        return self.warehouse_map.dropoff_points[dropoff_id]