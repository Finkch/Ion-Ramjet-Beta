# Plots data

import json

# Responsible for plotting data from text files
class Plotter:
    def __init__(self, file: str) -> None:
        
        # The file in which data is stored
        self.file: str = file

        self.metadata: dict = {}
        self.data: list = []

        # Reads the data to memory
        self.read()

    
    # Loads the text file to memory
    def read(self) -> None:
        with open(self.file, 'r') as file:
            for line in file:
                line = line.replace("'", '"') # Replaces single-quotes with double-quotes
                self.data.append(json.loads(line))

        # Grabs the metadata from data
        self.metadata = self.data.pop(0)