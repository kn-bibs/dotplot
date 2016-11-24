import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyFigure(FigureCanvas):
    def __init__(self):

        fig = Figure()
        FigureCanvas.__init__(self, fig)

        self.axes = fig.add_subplot(111)

    def update(self, dot_matrix):
        self.axes.imshow(dot_matrix, cmap='Greys', interpolation='nearest')
