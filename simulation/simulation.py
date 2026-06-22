class Simulation:
    def __init__(self, warehouse_map, robots, tasks):
        self.warehouse_map = warehouse_map
        self.robots = robots
        self.tasks = tasks

    def tick(self, current_tick: int) -> None:
        print(f"\nTick {current_tick}")

        for robot in self.robots:
            robot.move_one_step()
            print(robot)

    def all_routes_finished(self) -> bool:
        return all(
            not robot.planned_route
            for robot in self.robots
        )