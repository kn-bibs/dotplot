import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyFigure(FigureCanvas):
    def __init__(self):

        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)

        self.axes = self.fig.add_subplot(111)

    def draw_dotplot(self, dot_matrix):
        self.fig.clear()
        self.axes.clear()
        self.draw()
        self.axes = self.fig.add_subplot(111)
        self.axes.imshow(dot_matrix, cmap='Greys', interpolation='nearest')
        self.draw()
