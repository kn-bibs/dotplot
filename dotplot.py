#!/usr/bin/env python3

import sys
from argument_parser import ArgumentParser
from drawer import Drawer
from plotter import Plotter

# keep app object in global scope to prevent Python's GC from destroying PyQt
# objects in wrong order (see: pyqt.sourceforge.net/Docs/PyQt5/gotchas.html)
application = None


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


def is_pyqt5_available():
    """Check if the PyQt module is installed and importable."""
    try:
        import PyQt5 as _   # 'as _' tells pylint to ignore this variable
        return True
    except ImportError:
        return False


def is_matplotlib_available():
    """Check if the matplotlib module is installed and importable."""
    try:
        import matplotlib as _
        return True
    except ImportError:
        return False


def main(argv):
    """Main function running dotplot application.

    Args:
        argv:
            list of (command-line like) arguments to be parsed by
            ArgumentParser and used in the program's run. The first
            argument in the list should be the name of the script.
    """
    args = ArgumentParser().parse(argv)

    if args.gui:
        if not is_pyqt5_available():
            print('You need to install PyQt5 to use GUI.')
        else:
            from PyQt5.QtWidgets import QApplication
            from gui import MainWindow

            global application

            # register application
            application = QApplication(sys.argv)

            # create main window; henceforth this class takes all control
            main_window = MainWindow(args)

            # after releasing lock by MainWindow, quit gracefully
            sys.exit(application.exec())

    else:
        dotplot = Dotplot(args.parsed_sequences, args.plotter, args.drawer)
        dotplot.make_plot()

        if args.drawer.method == 'matplotlib':
            if not is_matplotlib_available():
                print('You need to install matplotlib to use it.')
            else:
                # ORDER MATTERS here. And one cannot just merge these imports.
                import matplotlib
                matplotlib.use('TkAgg')
                import matplotlib.pyplot as pyplot
                figure = pyplot.figure()
                main_plot = figure.add_subplot(111)
                dotplot.draw(main_plot, args.parsed_sequences)
                pyplot.show()
        else:
            drawings = dotplot.draw()
            print(drawings)

    return True


if __name__ == '__main__':
    main(sys.argv)
