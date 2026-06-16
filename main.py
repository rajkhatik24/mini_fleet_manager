from simulation.scenario_loader import load_scenario


def main():
    warehouse_map, robots, tasks = load_scenario(
        "data/scenarios/single_robot_demo.json"
    )

    print(warehouse_map)

    print("\nRobots:")
    for robot in robots:
        print(robot)

    print("\nTasks:")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()