# This file contains a class that performs the simulation
# Wrapping it in a class makes for easy referencing

class Simulation:
    def __init__(self) -> None:
        self.exist = True

    # The simulation loop
    def __call__(self):
        while self.exist:
            pass
