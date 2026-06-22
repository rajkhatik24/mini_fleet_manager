class Simulation:
    def __init__(self, warehouse_map, robots, tasks, task_executor):
        self.warehouse_map = warehouse_map
        self.robots = robots
        self.tasks = tasks
        self.task_executor = task_executor

    def tick(self, current_tick: int) -> None:
        print(f"\nTick {current_tick}")

        for robot in self.robots:
            had_route = bool(robot.planned_route)

            robot.move_one_step()

            route_finished = had_route and not robot.planned_route

            if route_finished:
                self.task_executor.handle_route_finished(robot)

            print(robot)

    def all_tasks_finished(self) -> bool:
        return all(
            task.is_finished()
            for task in self.tasks
        )