# This file contains a class that performs the simulation
# Wrapping it in a class makes for easy referencing

from finkchlib.clock import Clock
from ramjet import Ramjet


class Simulation:
    def __init__(self) -> None:
        self.exist: bool = True

        # Whether or not to perform debug printouts
        self.debug = True

        # Seconds per simulation step
        self.step: int = 1

        # Used to perform printouts
        self.clock: Clock = Clock(1000 / 60)

        # The craft to simulate
        self.ramjet: Ramjet = Ramjet("ioRam-Beta", 100, 5, self.step, 10, 1e3, 26, 4.9e4, 1.5e6, 1e3, 1e3, 1e7)


    # The simulation loop
    def __call__(self):
        while self.exist:
            self.ramjet()


            if self.debug and self.clock.time():
                self.debug()

    def debug(self):
        print(self.ramjet)
