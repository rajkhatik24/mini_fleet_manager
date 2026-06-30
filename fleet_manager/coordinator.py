from core.state import TaskStatus


class Coordinator:
    def __init__(self, planner, reservation_table=None):
        self.planner = planner
        self.reservation_table = reservation_table

    def plan_full_routes(
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

            dropoff_position = self._get_dropoff_position(
                task,
                warehouse_map
            )

            route_to_pickup = self._plan_route(
                robot.position,
                pickup_position,
                warehouse_map,
                start_time=0
            )

            pickup_arrival_time = len(route_to_pickup)

            route_to_dropoff = self._plan_route(
                pickup_position,
                dropoff_position,
                warehouse_map,
                start_time=pickup_arrival_time
            )

            full_route = route_to_pickup + route_to_dropoff

            robot.set_route(full_route)

            if self.reservation_table is not None:
                reservation_path = [robot.position] + full_route

                self.reservation_table.reserve_path(
                    robot_id=robot.robot_id,
                    path=reservation_path,
                    start_time=0,
                    hold_time=50
)

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

    def _get_dropoff_position(
        self,
        task,
        warehouse_map
    ):

        dropoff_id = task.parameters["dropoff"]
        return warehouse_map.dropoff_points[dropoff_id]
    

    def _plan_route(
    self,
    start,
    goal,
    warehouse_map,
    start_time: int = 0
    ):

        try:
            return self.planner.plan(
                start,
                goal,
                warehouse_map,
                start_time=start_time
            )
        except TypeError:
            return self.planner.plan(
                start,
                goal,
                warehouse_map
            )