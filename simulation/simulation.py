from simulation.collision_checker import CollisionChecker


class Simulation:
    def __init__(self, warehouse_map, robots, tasks, task_executor):
        self.warehouse_map = warehouse_map
        self.robots = robots
        self.tasks = tasks
        self.task_executor = task_executor
        self.collision_checker = CollisionChecker()

    def tick(self, current_tick: int) -> None:
        print(f"\nTick {current_tick}")

        previous_positions = {
            robot.robot_id: robot.position
            for robot in self.robots
        }

        for robot in self.robots:
            robot.move_one_step()

            self.task_executor.update_robot_task_state(robot)

            print(robot)

        self.collision_checker.check_collisions(
            robots=self.robots,
            previous_positions=previous_positions,
            current_tick=current_tick,
        )

    def all_tasks_finished(self) -> bool:
        return all(
            task.is_finished()
            for task in self.tasks
        )