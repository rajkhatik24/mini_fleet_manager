from core.warehouse_map import WarehouseMap
from planning.cooperative_astar import CooperativeAStarPlanner
from planning.reservation_table import ReservationTable


warehouse = WarehouseMap(
    width=10,
    height=10,
    obstacles=set()
)

reservation_table = ReservationTable()

planner = CooperativeAStarPlanner(
    reservation_table=reservation_table
)

path_r1 = planner.plan(
    start=(1, 1),
    goal=(5, 1),
    warehouse_map=warehouse
)

reservation_table.reserve_path(
    robot_id="R1",
    path=path_r1,
    start_time=1
)

path_r2 = planner.plan(
    start=(5, 1),
    goal=(1, 1),
    warehouse_map=warehouse
)

print("R1 path:", path_r1)
print("R2 path:", path_r2)