from simulation.scenario_loader import load_scenario
from simulation.simulation import Simulation
from simulation.event_loop import EventLoop
from simulation.task_executor import TaskExecutor

from scheduling.nearest_robot import NearestRobotScheduler
from planning.manhattan_planner import ManhattanPlanner

def main():
    warehouse_map, robots, tasks = load_scenario(
        "data/scenarios/four_robot_demo.json"
    )

    print(warehouse_map)

    print("\nRobots:")
    for robot in robots:
        print(robot)

    print("\nTasks:")
    for task in tasks:
        print(task)
    
    planner = ManhattanPlanner()
    scheduler = NearestRobotScheduler(planner=planner)
    assignments = scheduler.assign_tasks(robots, tasks, warehouse_map)

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

    event_loop = EventLoop(simulation)
    event_loop.run(max_ticks=100)

    print("\nTasks After Assignment:")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()