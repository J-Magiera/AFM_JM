import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure(figsize=(7, 7))
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.gca(projection='3d')

        self.axes.set_xlabel('$X$', fontsize=20)
        self.axes.set_ylabel('$Y$', fontsize=20)
        self.axes.set_zlabel('$Z$', fontsize=20)

        self.axes.set_xlim3d(0, 100)
        self.axes.set_ylim3d(0, 100)
        self.axes.set_zlim3d(0, 50)



    def DrawGraph(self, x, y, z):
        self.axes.scatter(x, y, z, c=z)
        self.draw()
