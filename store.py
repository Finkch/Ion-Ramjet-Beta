# Stores ALL information from a given simulation

import sys


# A Store stores data
class Store:
    def __init__(self, initial_data = None) -> None:
        self.data = []
        
        # Tracks whether to overwrite or append
        self.first_write = True
        
        # The file to which to write
        self.file = 'temp.txt'

        # If supplied with some starting data, write it out immediatly
        if initial_data:
            self.data.append(initial_data)
            self.write()

    # Adds the data to the array
    def add(self, data) -> None:
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

        print('Write!')

    # Returns how large the data size is
    def data_size(self) -> int:
        return sys.getsizeof(self.data)