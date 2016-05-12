import sys
from plotter import Plotter
from drawer import Drawer
from argument_parser import ArgumentParser


class Dotplot(object):

    def __init__(self,  sequences, plotter_args=None, drawer_args=None):
        self.sequences = sequences
        self.plotter = Plotter(plotter_args)
        self.drawer  = Drawer(drawer_args )

    def make_plot(self):
        plot = self.plotter(self.sequences)

    def draw(self, plot):
        self.drawer.draw(self, plot)

if __name__ == "main":
    kwargs = ArgumentParser(sys.argv)
    dotplot = Dotplot(**kwargs)
    plot = dotplot.make_plot()
    dotplot.draw()

