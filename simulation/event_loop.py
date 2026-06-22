from simulation.clock import SimulationClock


class EventLoop:
    def __init__(self, simulation):
        self.simulation = simulation
        self.clock = SimulationClock()

    def run(self, max_ticks: int = 30) -> None:
        for _ in range(max_ticks):
            current_tick = self.clock.advance()

            self.simulation.tick(current_tick)

            if self.simulation.all_routes_finished():
                print("\nAll planned routes finished.")
                break