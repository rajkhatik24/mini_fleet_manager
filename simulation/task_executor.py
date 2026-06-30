from core.state import RobotExecutionState, TaskStatus


class TaskExecutor:
    def __init__(self, warehouse_map, tasks, planner=None):
        self.warehouse_map = warehouse_map
        self.tasks = tasks
        self.planner = planner

    def update_robot_task_state(self, robot) -> None:
        task = self._get_task_by_id(robot.assigned_task_id)

        if task is None:
            return

        if task.status == TaskStatus.ASSIGNED:
            pickup_position = self._get_pickup_position(task)

            if robot.position == pickup_position:
                self._handle_reached_pickup(robot, task)

        elif task.status == TaskStatus.IN_PROGRESS:
            dropoff_position = self._get_dropoff_position(task)

            if robot.position == dropoff_position:
                self._handle_reached_dropoff(robot, task)

    def _handle_reached_pickup(self, robot, task) -> None:
        print(f"Robot {robot.robot_id} reached pickup for Task {task.task_id}")

        task.start()
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

    def _get_pickup_position(self, task):
        pickup_id = task.parameters["pickup"]
        return self.warehouse_map.pickup_points[pickup_id]

    def _get_dropoff_position(self, task):
        dropoff_id = task.parameters["dropoff"]
        return self.warehouse_map.dropoff_points[dropoff_id]