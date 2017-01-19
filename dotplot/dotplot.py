from .drawer import Drawer
from .plotter import Plotter


class Dotplot(object):
    def __init__(self, sequences, plotter_args=None, drawer_args=None):

        self.sequences = sequences
        self.plotter = Plotter(plotter_args)
        self.drawer = Drawer(drawer_args)
        self.plot = None

    def make_plot(self):
        self.plot = self.plotter.plot(self.sequences)

    def draw(self, *args, **kwargs):
        plot = kwargs.get('plot', self.plot)
        return self.drawer.draw(plot, *args, **kwargs)
