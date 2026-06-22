from simulation.clock import SimulationClock


class EventLoop:
    def __init__(self, simulation):
        self.simulation = simulation
        self.clock = SimulationClock()

    def run(self, max_ticks: int = 100) -> None:
        for _ in range(max_ticks):
            current_tick = self.clock.advance()

            self.simulation.tick(current_tick)

            if self.simulation.all_tasks_finished():
                print("\nAll tasks completed.")
                break