# This file contains a class that performs the simulation
# Wrapping it in a class makes for easy referencing

from finkchlib.orders import Time
from finkchlib.vector import Vector2
from finkchlib.constants import *
from ramjet import Ramjet
from store import Store
import hangar

class Simulation:
    def __init__(self, rate: float, framerate: float, ramjet: str, file: str) -> None:
        self.exist: bool = True

        # Used to track performance
        self.clock: Time = Time(rate, framerate)

        # Seconds per simulation step
        self.step: float = rate

        # Keep track of simulation parameters
        self.steps = 0
        self.sim_time = 0


        # The craft to simulate
        self.ramjet: Ramjet = hangar.get_ramjet(ramjet)


        # Used to store data at each step
        self.store: Store = Store(file, {'step_size': self.step, 'name': self.ramjet.name})
    
    # Calling Simulation begins simulation loop
    def __call__(self):

        # Stamps start of simulation
        self.clock.real_time.stamp()

        # Simulation loop
        while self.exist:
            
            # Adds snapshot to data store
            self.store.add(self.preview())
            
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
        print(f'Rate:\t\t\t{self.step:.0f} s : 1 step')
        print(f'Total time:\t\t{readable_time((self.clock.real_time.peek_dif(1) + self.clock.real_time.peek_dif(0)) / 1000)} -> {(self.clock.real_time.peek_dif(1) + self.clock.real_time.peek_dif(0)) / 1000:.2e} s')
        print(f'Time to simulate:\t{readable_time(self.clock.real_time.peek_dif(1) / 1000)} -> {self.clock.real_time.peek_dif(1) / 1000:.2e} s')
        print(f'Time to store:\t\t{readable_time(self.clock.real_time.peek_dif()/ 1000)} -> {self.clock.real_time.peek_dif()/ 1000:.2e} s')
        print(f'Sim time:\t\t{readable_time(self.sim_time)} -> {self.sim_time:.2e} s')
        print(f'Ramjet time (dilated):\t{readable_time(self.ramjet.spacetime.time)} -> {self.ramjet.spacetime.time:.2e} s')
        print(f'Steps per second:\t{self.steps / self.clock.sim_time:.0f} (recent: {1000 / self.clock.timer.get_average_difs():.0f})')
        print(self.ramjet)

    # Check if the simulation should end
    def check_end(self):

        # One end condition: tank is empty
        # This is not always a condition
        self.tank_empty()

        # Safety end condition: a century of steps (not time!) has past
        #self.heat_death()

    # Handles the end of the simulation
    def end(self):

        # Timestamps end of simulation
        self.clock.real_time.stamp()

        # Adds final snapshot; writes any remaining data
        self.store.add(self.preview())
        self.store.write()

        # Re-writes the file to be easily read
        self.store.flatten_file()

        # Timestamps time taken to write and flatten
        self.clock.real_time.stamp()

        self.printout()
        print('All done!')


    
    # Gets a full snapshot at this step
    def preview(self):
        return {
            'steps': self.steps,
            'sim_time': self.sim_time,
            'real_time': self.clock.sim_time,
            'ramjet': self.ramjet.get_previews()
        }



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
    def __init__(self, rate: float, framerate: float, ramjet: str, file: str) -> None:
        super().__init__(rate, framerate, ramjet, file)

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