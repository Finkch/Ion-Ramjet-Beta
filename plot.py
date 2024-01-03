# Plots data

import json

# Responsible for plotting data from text files
class Plotter:
    def __init__(self, file) -> None:
        
        # The file in which data is stored
        self.file = file

        self.metadata = {}
        self.data = []

        # Reads the data to memory
        self.read()
    
    # Loads the text file to memory
    def read(self):
        with open(self.file, 'r') as file:
            for line in file:
                line = line.replace("'", '"') # Replaces single-quotes with double-quotes
                self.data.append(json.loads(line))

        # Grabs the metadata from data
        self.metadata = self.data.pop(0)