import json

from core.robot import Robot
from core.task import Task
from core.state import TaskType
from core.types import RobotID, TaskID
from core.warehouse_map import WarehouseMap


def load_scenario(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        scenario_data = json.load(file)

    warehouse_map = WarehouseMap.from_json(scenario_data["map"])

    robots = []
    for robot_data in scenario_data["robots"]:
        robot = Robot(
            robot_id=RobotID(robot_data["robot_id"]),
            position=tuple(robot_data["start_position"]),
            battery=robot_data.get("battery", 100.0),
        )
        robots.append(robot)

    with open(scenario_data["tasks"], "r", encoding="utf-8") as file:
        tasks_data = json.load(file)

    tasks = []
    for task_data in tasks_data:
        task = Task(
            task_id=TaskID(task_data["task_id"]),
            task_type=TaskType(task_data["task_type"]),
            priority=task_data.get("priority", 1),
            parameters=task_data.get("parameters", {}),
        )
        tasks.append(task)

    return warehouse_map, robots, tasks