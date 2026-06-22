class SimulationClock:
    def __init__(self):
        self.current_tick = 0

    def advance(self) -> int:
        self.current_tick += 1
        return self.current_tick