# This file contains a class that performs the simulation
# Wrapping it in a class makes for easy referencing

from finkchlib.orders import Time
from finkchlib.vector import Vector2
from finkchlib.constants import *
from ramjet import Ramjet

class Simulation:
    def __init__(self, rate: float, framerate: float) -> None:
        self.exist: bool = True

        # Used to track performance
        self.clock: Time = Time(rate, framerate)

        # Seconds per simulation step
        self.step: float = rate

        # The craft to simulate
        # X_e   = 131.293 u
        # H     = 1.00784 u
        self.ramjet: Ramjet = Ramjet('ioRamjet-Beta', 100, self.step, 10, 1e7, 26, 4.9e4, 1.5e6, 1e6, 1e2, 1e8)
        self.ramjet.spacetime.position = Vector2(1, 0)
    
    # Simulation loop
    def __call__(self):
        while self.exist:
            
            # Stamps time taken for sim step
            #self.clock()

            # Simulates the ramjet
            self.ramjet()
            
            # Checks whether the simulation can end
            self.check_end()

        # Handles the end of the simulation
        self.end()


    # Performs a printout
    def printout(self):
        print('\n\n')
        print(self.time)
        print(self.ramjet)

    # Check if the simulation should end
    def check_end(self):

        # One end condition: tank is empty
        self.tank_empty()

        # Safety end condition: a century of steps (not time!) has past
        self.heat_death()

    # Hanldes the end of the simulation
    def end(self):
        self.printout()
        print('All done!')



    # A list of ending conditions
    def tank_empty(self) -> None:
        if self.ramjet.tank.is_empty():
            self.exist = False

    # Safety condition
    def heat_death(self) -> None:
        if self.ramjet.spacetime.time > 100 * year:
            self.exist = False



# The same as Simulation but the steps are taken at a rate of 1:1 with printouts.
# Only DebugSim can perform printouts
class DebugSimulation(Simulation):
    def __init__(self, rate: float, framerate: float) -> None:
        super().__init__(rate, framerate)

    def __call__(self) -> None:
        while self.exist:
            if self.real_time.time():
                self.clock()
                self.printout()
                self.ramjet()
            
                self.check_end()

        self.end()

