from planning.reservation_table import ReservationTable


table = ReservationTable()

path = [
    (1, 1),
    (2, 1),
    (3, 1),
]

table.reserve_path(
    robot_id="R1",
    path=path,
    start_time=0
)

print(table.is_vertex_reserved((2, 1), 1))
print(table.is_move_allowed((2, 1), (1, 1), 1))