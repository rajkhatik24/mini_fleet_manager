from simulation.scenario_loader import load_scenario
from scheduling.nearest_robot import NearestRobotScheduler


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
    
    scheduler = NearestRobotScheduler()
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

    print("\nTasks After Assignment:")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()