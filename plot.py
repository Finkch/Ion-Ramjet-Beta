# Plots data

import matplotlib.pyplot as mpl

# Responsible for plotting data from text files
class Plotter:
    def __init__(self, data: dict, metadata: dict) -> None:

        self.metadata: dict = metadata
        self.data: dict = data



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