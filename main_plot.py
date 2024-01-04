# Used to draw plots

from store import Store
from plot import Plotter

def main():

    # The file from which to read
    file: str = 'temp.txt'

    # Gets the data Store up
    store: Store = Store(file)

    # Reads from the data file
    data, metadata = store.read()

    # Creates Plotter
    plot = Plotter(data, metadata)

    # Plots some data
    plot('sim_time', 'ramjet-spacetime-pos_x', 'Position vs. Time', ['Time (s)', 'Position (m)'])
    plot('sim_time', 'ramjet-spacetime-vel_x', 'Velocity vs. Time', ['Time (s)', 'Velocity (m/s)'])
    plot('sim_time', 'ramjet-spacetime-acc_x', 'Acceleration vs. Time', ['Time (s)', 'Acceleration (m/s)'])
    
    # Shows the data
    plot.show()

main()