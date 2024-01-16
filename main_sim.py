# This file gets the ball rolling

# There's a bug right now:
#   There are incorrect time dependencies; the sim rate affects craft performance.
#   Figure out what code component causes this.
#       Spacetime, craft parts, or something else?

from simulation import *

# Gets everything going
def main():
    
    # The Ramjet to use in this simulation
    ramjet = 'Dawn'

    # Whether to run in debug mode
    # In debug mode, sim-steps occur in lock-step with printouts
    debug = False

    # How many seconds are simulated in each step
    rate = hour

    # Desired framerate for printouts
    framerate = 1000 / 60 if not debug else 1000

    # The file to store data in
    file = 'temp.txt'

    # Creates the simulation
    simulation = Simulation(rate, framerate, ramjet, file) if not debug else DebugSimulation(rate, framerate, ramjet, file) 

    # Runs the simulation
    simulation()

# Ready, set, go!
main()

