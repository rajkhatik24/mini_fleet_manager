from simulation.clock import SimulationClock


class EventLoop:
    def __init__(self, simulation, visualizer=None, visualizers=None):
        self.simulation = simulation
        self.clock = SimulationClock()

        if visualizers is not None:
            self.visualizers = visualizers
        elif visualizer is not None:
            self.visualizers = [visualizer]
        else:
            self.visualizers = []

    def run(self, max_ticks: int = 100) -> None:
        for _ in range(max_ticks):
            current_tick = self.clock.advance()

            self.simulation.tick(current_tick)

            for visualizer in self.visualizers:
                visualizer.render(
                    robots=self.simulation.robots,
                    tasks=self.simulation.tasks,
                    current_tick=current_tick,
                )

            if self.simulation.all_tasks_finished():
                print("\nAll tasks completed.")
                break

        for visualizer in self.visualizers:
            visualizer.close()