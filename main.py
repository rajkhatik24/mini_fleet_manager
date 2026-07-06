from simulation.scenario_loader import load_scenario
from simulation.simulation import Simulation
from simulation.event_loop import EventLoop
from simulation.task_executor import TaskExecutor

from scheduling.nearest_robot import NearestRobotScheduler

from planning.cooperative_astar import CooperativeAStarPlanner
from planning.reservation_table import ReservationTable

from fleet_manager.coordinator import Coordinator

from visualization.matplotlib_visualizer import MatplotlibVisualizer
from ros2_adapter.robot_state_pub import RobotStatePublisher


def main():
    warehouse_map, robots, tasks = load_scenario(
        "data/scenarios/mapf_overlap_demo.json"
    )

    print(warehouse_map)

    print("\nRobots:")
    for robot in robots:
        print(robot)

    print("\nTasks:")
    for task in tasks:
        print(task)

    reservation_table = ReservationTable()

    planner = CooperativeAStarPlanner(
        reservation_table=reservation_table
    )


    scheduler = NearestRobotScheduler()
    assignments = scheduler.assign_tasks(
        robots,
        tasks,
        warehouse_map
    )

    coordinator = Coordinator(
        planner=planner,
        reservation_table=reservation_table
    )


    coordinator.plan_full_routes(
        robots,
        tasks,
        warehouse_map
    )

    print("\nAssignments:")
    if assignments:
        for task_id, robot_id in assignments.items():
            print(f"Task {task_id} -> Robot {robot_id}")
    else:
        print("No assignments created.")

    print("\nRobots After Assignment:")
    for robot in robots:
        print(robot)

    print("\nPlanned Routes:")
    for robot in robots:
        if robot.planned_route:
            print(f"Robot {robot.robot_id}: {robot.planned_route}")

    print("\nStarting Simulation:")

    task_executor = TaskExecutor(
        warehouse_map,
        tasks,
        planner
    )

    simulation = Simulation(
        warehouse_map,
        robots,
        tasks,
        task_executor
    )

    matplotlib_visualizer = MatplotlibVisualizer(
        warehouse_map,
        pause_time=0.5
    )

    ros2_visualizer = RobotStatePublisher(
        warehouse_map
    )

    event_loop = EventLoop(
        simulation,
        visualizers =[
            matplotlib_visualizer,
            ros2_visualizer
        ]
    )

    event_loop.run(max_ticks=100)

    print("\nTasks After Assignment:")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()