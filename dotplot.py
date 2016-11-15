import sys
from argument_parser import ArgumentParser
from drawer import Drawer
from plotter import Plotter
from sequence import Sequence


class Dotplot(object):
    def __init__(self, sequences, plotter_args=None, drawer_args=None):
        self.sequences = [
            Sequence.from_fasta_file(sequences.file1),
            Sequence.from_fasta_file(sequences.file2)
        ]
        self.plotter = Plotter(plotter_args)
        self.drawer = Drawer(drawer_args)
        self.plot = None

    def make_plot(self):
        self.plot = self.plotter.plot(self.sequences)

    def draw(self, plot=None):
        if not plot:
            plot = self.plot
        self.drawer.draw(plot)


def is_pyqt5_available():
    """Check if the PyQt module is installed and importable."""
    try:
        import PyQt5 as _   # 'as _' tells pylint to ignore this variable
        return True
    except ImportError:
        return False


def main():
    args = ArgumentParser().parse(sys.argv)
    if args.gui:
        if not is_pyqt5_available():
            print('You need to install PyQt5 to use GUI')
        else:

            from PyQt5.QtWidgets import QApplication
            from gui import MainWindow

            # register application
            application = QApplication(sys.argv)

            # create main window; henceforth this class takes all control
            main_window = MainWindow(args)

            # after releasing lock by MainWindow, quit gracefully
            sys.exit(application.exec_())

    else:
        dotplot = Dotplot(args.sequences, args.plotter, args.drawer)
        dotplot.make_plot()
        dotplot.draw()


if __name__ == '__main__':
    main()
