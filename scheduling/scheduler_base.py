from abc import ABC, abstractmethod


class SchedulerBase(ABC):

    @abstractmethod
    def assign_tasks(self, robots, tasks, warehouse_map):
        pass