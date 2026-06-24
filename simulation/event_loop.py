from simulation.clock import SimulationClock


class EventLoop:
    def __init__(self, simulation, visualizer=None):
        self.simulation = simulation
        self.visualizer = visualizer
        self.clock = SimulationClock()

    def run(self, max_ticks: int = 100) -> None:
        for _ in range(max_ticks):
            current_tick = self.clock.advance()

            self.simulation.tick(current_tick)

            if self.visualizer is not None:
                self.visualizer.render(
                    robots=self.simulation.robots,
                    tasks=self.simulation.tasks,
                    current_tick=current_tick,
                )

            if self.simulation.all_tasks_finished():
                print("\nAll tasks completed.")
                break

        if self.visualizer is not None:
            self.visualizer.close()