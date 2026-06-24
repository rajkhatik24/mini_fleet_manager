from planning.astar_planner import AStarPlanner
from core.warehouse_map import WarehouseMap


warehouse = WarehouseMap(
    width=10,
    height=10,
    obstacles={
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
    }
)

planner = AStarPlanner()

path = planner.plan(
    (0, 0),
    (5, 0),
    warehouse
)

print(path)