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

        # Keep track of simulation parameters
        self.steps = 0
        self.sim_time = 0

        # The craft to simulate
        # X_e   = 131.293 u
        # H     = 1.00784 u
        self.ramjet: Ramjet = Ramjet('ioRamjet-Beta', 100, 10, 1e7, 26, 4.9e4, 1.5e6, 1e6, 1e2, 1e8)
        self.ramjet.spacetime.position = Vector2(1, 0)
    
    # Simulation loop
    def __call__(self):
        while self.exist:
            
            # Stamps time taken for sim step
            self.clock()
            self.sim_time += self.step
            self.steps += 1

            # Simulates the ramjet
            self.ramjet(self.step)
            
            # Checks whether the simulation can end
            self.check_end()

        # Handles the end of the simulation
        self.end()


    # Performs a printout
    def printout(self):
        print('\n\n')
        print(f'Real time: {self.clock} -> {self.clock.sim_time:.2e} s')
        print(f'Sim time:  {readable_time(self.sim_time)} -> {self.sim_time:.2e} s')
        print(f'Sim time\':  {readable_time(self.ramjet.spacetime.time)} -> {self.ramjet.spacetime.time:.2e} s')
        print(f'Steps per second: {self.steps / self.clock.sim_time:.0f} (recent: {1000 / self.clock.timer.get_average_difs():.0f})')
        print(self.ramjet)

    # Check if the simulation should end
    def check_end(self):

        # One end condition: tank is empty
        # Thisis not always a condition
        #self.tank_empty()

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
        if self.steps > 2 * day:
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



def readable_time(time: float):
    # Converts time to a human-readable format
    time = int(time)

    return "{years:.2e} y, {days:03} d, {hours:02} h, {minutes:02} m, {seconds:02} s".format(
        years = time // year,
        days = (time // day) % 365,
        hours = (time // hour) % 24,
        minutes = (time // minute) % 60,
        seconds = time % 60
    )