# Plots data

import json
import matplotlib.pyplot as mpl

# Responsible for plotting data from text files
class Plotter:
    def __init__(self, file: str) -> None:
        
        # The file in which data is stored
        self.file: str = file

        self.metadata: dict = {}
        self.data: dict = {}
        self.unflattened: list = []

        # Reads the data to memory
        self.read()


    # Calling Plotter plots data
    def __call__(self, x_key: str, y_key: str, plot_name: str, axes_names: list[str, str]) -> None:

        # Grabs the necessary data
        x = self.data[x_key]
        y = self.data[y_key]

        # Grabs the figure and axes
        figure, axes = mpl.subplots()

        # Plots the data
        axes.plot(x, y)

        # Sets the title
        axes.set_title(plot_name)

        # Sets axes names
        mpl.xlabel(axes_names[0])
        mpl.ylabel(axes_names[1])

    # Shows plot
    def show(self):
        mpl.show()


    # Loads the text file to memory
    def read(self) -> None:
        with open(self.file, 'r') as file:
            for line in file:
                line = line.replace("'", '"') # Replaces single-quotes with double-quotes
                self.unflattened.append(json.loads(line))

        # Grabs the metadata from data
        self.metadata = self.unflattened.pop(0)

        # Flattens the dictionary to minimal depth
        self.flatten()

    # Flattens the data array so that it has minimal depth
    def flatten(self):

        # Iterates over every line
        for line in self.unflattened:
            self.recursive_flatten(line, '')

        # Deletes unnecessary data
        self.unflattened = None

    # Recurse through the dictionary, adding items
    def recursive_flatten(self, data: dict, path: str):
        
        # Iterate over all items at this depth
        for key in data.keys():

            # If the item is a dictionary, recurse
            if isinstance(data[key], dict):
                self.recursive_flatten(data[key], f'{path}{key}-')

            # Otherwise, add the item to data
            else:
                self.add_flat(f'{path}{key}-', data[key])

    # Adds the piece of data to the flattened list
    def add_flat(self, key: str, item) -> None:

        # Removes the trailing hyphen
        key = key[:-1]

        # If this is a new entry, make a list for it
        if not key in self.data:
            self.data[key] = []

        # Add the item to data
        self.data[key].append(item)


