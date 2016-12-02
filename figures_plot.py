import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyFigure(FigureCanvas):

    def __init__(self):

        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)

        self.main_plot = None
        self.create_main_plot()

    def create_main_plot(self):
        self.main_plot = self.fig.add_subplot(111)

    def reset(self):
        self.fig.clear()
        self.main_plot.clear()
        self.create_main_plot()

    def save_file(self, file_data):
        """Supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz."""
        file_format = file_data[1]
        extension_location = file_format.find("*.")
        extension = file_format[extension_location+1:len(file_format)-1]
        file_name = file_data[0]
        self.fig.savefig(file_name)
        if extension not in file_name:
            file_name += extension
        self.fig.savefig(file_name)
