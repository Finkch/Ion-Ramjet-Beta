# Stores ALL information from a given simulation

import sys
import json

# A Store stores data
class Store:
    def __init__(self, file: str, initial_data = None) -> None:
        self.data: list = []
        
        # Tracks whether to overwrite or append
        self.first_write: bool = True
        
        # The file to which to write
        self.file: str = 'temp.txt'

        # Used for reading data
        self.metadata: dict = {}
        self.data: dict = {}
        self.unflattened: list = []

        # If supplied with some starting data, write it out immediatly
        if initial_data:
            self.unflattened.append(initial_data)
            self.write()

    # Adds the data to the array
    def add(self, data: dict) -> None:
        self.data.append(data)

        # If we're storing more than a gigabyte, write it out
        if self.data_size() > 1e9:
            self.write()

    # Writes data to text
    def write(self) -> None:
        
        # Gets the correct flag.
        # We want to clear data from the previous simulation, but add to the current
        flag = 'w' if self.first_write else 'a'
        self.first_write = False # Updates
        
        # Writes the data
        with open(self.file, flag) as file:
            for step in self.data:
                file.write(str(step) + '\n')

        # Since we're done writing, clear data
        self.data = []

    # Returns how large the data size is
    def data_size(self) -> int:
        return sys.getsizeof(self.data)
    


    # Reads data from a file, returning it as a dictionary
    def read(self) -> dict:
        with open(self.file, 'r') as file:
            for line in file:
                line = line.replace("'", '"') # Replaces single-quotes with double-quotes
                self.unflattened.append(json.loads(line))

        # Grabs the metadata from data
        self.metadata = self.unflattened.pop(0)

        # Flattens the dictionary to minimal depth
        self.flatten()

        return self.data, self.metadata

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




