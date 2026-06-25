class CollisionChecker:

    def check_collisions(
        self,
        robots,
        previous_positions,
        current_tick: int
    ) -> None:
        self._check_vertex_collisions(
            robots,
            current_tick
        )

        self._check_edge_collisions(
            robots,
            previous_positions,
            current_tick
        )

    def _check_vertex_collisions(
        self,
        robots,
        current_tick: int
    ) -> None:
        occupied_positions = {}

        for robot in robots:
            position = robot.position

            if position in occupied_positions:
                other_robot = occupied_positions[position]

                print(
                    f"VERTEX COLLISION at tick {current_tick}: "
                    f"{other_robot.robot_id} and {robot.robot_id} "
                    f"are both at {position}"
                )
            else:
                occupied_positions[position] = robot

    def _check_edge_collisions(
        self,
        robots,
        previous_positions,
        current_tick: int
    ) -> None:
        for i in range(len(robots)):
            for j in range(i + 1, len(robots)):

                robot_a = robots[i]
                robot_b = robots[j]

                old_a = previous_positions[robot_a.robot_id]
                old_b = previous_positions[robot_b.robot_id]

                new_a = robot_a.position
                new_b = robot_b.position

                if old_a == new_b and old_b == new_a:
                    print(
                        f"EDGE COLLISION at tick {current_tick}: "
                        f"{robot_a.robot_id} moved {old_a} -> {new_a}, "
                        f"{robot_b.robot_id} moved {old_b} -> {new_b}"
                    )