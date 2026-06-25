import time

from core.robot import Robot
from core.warehouse_map import WarehouseMap
from planning.cooperative_astar import CooperativeAStarPlanner
from planning.reservation_table import ReservationTable
from visualization.matplotlib_visualizer import MatplotlibVisualizer


warehouse = WarehouseMap(
    width=8,
    height=5,
    obstacles=set()
)

reservation_table = ReservationTable()

planner = CooperativeAStarPlanner(
    reservation_table=reservation_table,
    max_time=50
)

# Two robots facing each other in same row
robot_1 = Robot(
    robot_id="R1",
    position=(1, 2)
)

robot_2 = Robot(
    robot_id="R2",
    position=(6, 2)
)

path_r1 = planner.plan(
    start=robot_1.position,
    goal=(6, 2),
    warehouse_map=warehouse
)

reservation_table.reserve_path(
    robot_id=robot_1.robot_id,
    path=path_r1,
    start_time=1
)

path_r2 = planner.plan(
    start=robot_2.position,
    goal=(1, 2),
    warehouse_map=warehouse
)

robot_1.set_route(path_r1)
robot_2.set_route(path_r2)

robots = [
    robot_1,
    robot_2
]

visualizer = MatplotlibVisualizer(
    warehouse_map=warehouse,
    pause_time=0.5
)

print("R1 path:", path_r1)
print("R2 path:", path_r2)

for tick in range(1, 20):
    print(f"\nTick {tick}")

    for robot in robots:
        robot.move_one_step()
        print(robot)

    visualizer.render(
        robots=robots,
        current_tick=tick
    )

    if not robot_1.planned_route and not robot_2.planned_route:
        break

visualizer.close()