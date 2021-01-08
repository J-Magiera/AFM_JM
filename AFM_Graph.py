import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(FigureCanvas):  # Class for 3D window
    def __init__(self):
        self.fig = plt.figure(figsize=(7, 7))
        FigureCanvas.__init__(self, self.fig)  # creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')  # generates 3D Axes object
        self.setWindowTitle("Main")  # sets Window title
        self.axes.legend()

    def DrawGraph(self, x, y, z):  # Fun for Graph plotting
        self.axes.scatter(x, y, z, c=z)  # plots the 3D surface plot
        self.draw()