from typing import Tuple, List, NewType


Position = Tuple[int, int]
Path = List[Position]

RobotID = NewType("RobotID", str)
TaskID = NewType("TaskID", str)

TimeStep = NewType("TimeStep", int)