import matplotlib.pyplot as plt


class MatplotlibVisualizer:
    def __init__(self, warehouse_map, pause_time: float = 0.4):
        self.warehouse_map = warehouse_map
        self.pause_time = pause_time

        plt.ion()
        self.fig, self.ax = plt.subplots()

    def render(self, robots, tasks=None, current_tick: int = 0) -> None:
        self.ax.clear()

        self._draw_grid()
        self._draw_obstacles()
        self._draw_points(self.warehouse_map.pickup_points, "P")
        self._draw_points(self.warehouse_map.dropoff_points, "D")
        self._draw_points(self.warehouse_map.charging_stations, "C")
        self._draw_robots(robots)

        self.ax.set_title(f"Mini Fleet Manager - Tick {current_tick}")
        self.ax.set_xlim(-0.5, self.warehouse_map.width - 0.5)
        self.ax.set_ylim(-0.5, self.warehouse_map.height - 0.5)
        self.ax.set_aspect("equal")

        self.ax.set_xticks(range(self.warehouse_map.width))
        self.ax.set_yticks(range(self.warehouse_map.height))
        self.ax.grid(True)

        self.ax.invert_yaxis()

        plt.pause(self.pause_time)

    def _draw_grid(self) -> None:
        for x in range(self.warehouse_map.width):
            for y in range(self.warehouse_map.height):
                self.ax.plot(x, y, marker="s", markersize=18, alpha=0.05)

    def _draw_obstacles(self) -> None:
        for x, y in self.warehouse_map.obstacles:
            self.ax.plot(x, y, marker="s", markersize=18)
            self.ax.text(
                x,
                y,
                "X",
                ha="center",
                va="center",
                fontsize=8,
            )

    def _draw_points(self, points, prefix: str) -> None:
        for name, position in points.items():
            x, y = position
            self.ax.plot(x, y, marker="s", markersize=18, alpha=0.4)
            self.ax.text(
                x,
                y,
                name,
                ha="center",
                va="center",
                fontsize=8,
                fontweight="bold",
            )

    def _draw_robots(self, robots) -> None:
        for robot in robots:
            x, y = robot.position

            self.ax.plot(x, y, marker="o", markersize=16)
            self.ax.text(
                x,
                y,
                robot.robot_id,
                ha="center",
                va="center",
                fontsize=8,
                fontweight="bold",
            )

    def close(self) -> None:
        plt.ioff()
        plt.show()