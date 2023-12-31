# This file contains a class that performs the simulation
# Wrapping it in a class makes for easy referencing

from finkchlib.clock import Clock
from finkchlib.vector import Vector2
from ramjet import Ramjet

class Simulation:
    def __init__(self, framerate) -> None:
        self.exist = True

        # Seconds per simulation step
        self.step: int = 1

        # Used to perform printouts
        self.clock: Clock = Clock(framerate)

        # The craft to simulate
        # X_e   = 131.293 u
        # H     = 1.00784 u
        self.ramjet: Ramjet = Ramjet("ioRam-Beta", 100, 5, self.step, 10, 1e3, 26, 4.9e4, 1.5e6, 1e3, 1e3, 1e7)
        self.ramjet.spacetime.position = Vector2(1, 0)
    
    # Simulation loop
    def __call__(self):
        while self.exist:
            self.ramjet()

            if self.clock.time():
                self.printout()

    def printout(self):
        print('\n\n')
        print(self.ramjet)


# The same as Simulation but the steps are taken at a rate of 1:1 with printouts
class DebugSimulation(Simulation):
    def __init__(self, framerate) -> None:
        super().__init__(framerate)

    def __call__(self) -> None:
        while self.exist:
            if self.clock.time():
                self.printout()
                self.ramjet()

