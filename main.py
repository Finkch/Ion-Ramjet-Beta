# This file gets the ball rolling

from simulation import *

# Gets everything going
def main():
    
    debug = False

    rate = 1

    # Desired framerate for printouts
    framerate = 1000 / 60 if not debug else 1000

    simulation = Simulation(rate, framerate) if not debug else DebugSimulation(rate, framerate) 

    simulation()

# Ready, set, go!
main()

