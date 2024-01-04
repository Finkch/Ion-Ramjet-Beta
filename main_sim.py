# This file gets the ball rolling

from simulation import *

# Gets everything going
def main():
    
    debug = False

    rate = 1

    # Desired framerate for printouts
    framerate = 1000 / 60 if not debug else 1000

    # The file to store data in
    file = 'temp.txt'

    simulation = Simulation(rate, framerate, file) if not debug else DebugSimulation(rate, framerate, file) 

    simulation()

# Ready, set, go!
main()

