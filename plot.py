# Plots data

import matplotlib.pyplot as mpl

# Responsible for plotting data from text files
class Plotter:
    def __init__(self, data: dict, metadata: dict) -> None:

        self.metadata: dict = metadata
        self.data: dict = data



    # Calling Plotter plots data
    def __call__(self, x_key: str, y_key: str, plot_name: str, axes_names: list[str, str], *args, **kwargs) -> None:

        # Grabs the necessary data
        x, y = self.get_data(x_key, y_key, kwargs)

        # Grabs the figure and axes
        figure, axes = mpl.subplots()

        # Plots the data
        axes.plot(x, y)

        # Sets the title
        axes.set_title(plot_name)

        # Sets axes names
        mpl.xlabel(axes_names[0])
        mpl.ylabel(axes_names[1])


        # Handles extra arguments
        if 'logy' in args:
            axes.set_yscale('log')
        
        if 'logx' in args:
            axes.set_xscale('log')


    # Shows plot
    def show(self):
        mpl.show()

    # Obtains the data
    def get_data(self, x_key: str, y_key: str, kwargs) -> tuple:

        # The limits of the slice
        x_start = 0
        x_end = None

        # Gets the first item closest to the asked starting value
        if 'x_start' in kwargs:
            for i in range(len(self.data[x_key])):
                if self.data[x_key][i] >= kwargs['x_start']:
                    x_start = i
                    break
        
        # Gets the first item closest to the asked ending value
        if 'x_end' in kwargs:
            for i in range(0, len(self.data[x_key], -1)):
                if self.data[x_key][i] <= kwargs['x_end']:
                    x_end = i
                    break

        # Returns the data
        return self.data[x_key][x_start:x_end], self.data[y_key][x_start:x_end]