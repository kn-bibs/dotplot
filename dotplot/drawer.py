

class Drawer(object):
    """Creates a Drawer object"""

    default_method = 'unicode'

    def __init__(self, arguments):
        """Creates a Drawer object that is using a given drawing method"""
        # TODO: write an accurate docstring
        # TODO: exceptions

        self.drawing_methods = {
            'unicode': self.make_unicode,
            'ascii': self.make_ascii,
            'matplotlib': self.make_matplotlib
        }

        method = arguments.get('method', self.default_method)

        self.show_sequence = arguments.get('show_sequences', 100)

        self.draw = self.drawing_methods[method]

    def make_ascii(self, dot_matrix):
        """Generate an ASCII representation of dotmatrix

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        drawings = ''
        for row in dot_matrix:
            for element in row:
                if element == 1:
                    drawings += '\x58'
                else:
                    drawings += '\x20'
            drawings += '\n'
        return drawings

    def make_unicode(self, dot_matrix):
        """Generate Unicode representation of dotmatrix.

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        drawings = ''
        drawings += u'\u2554'                       # left upper corner
        drawings += u'\u2550' * len(dot_matrix[0])  # upper line
        drawings += u'\u2557' + '\n'                # right upper corner
        for row in dot_matrix:                      # matrix...
            drawings += u'\u2551'
            for element in row:
                if element == 1:
                    drawings += u'\u2588'
                elif element >= 0.75:
                    drawings += u'\u2593'
                elif element >= 0.5:
                    drawings += u'\u2592'
                elif element >= 0.25:
                    drawings += u'\u2591'
                else:
                    drawings += u'\u0020'
            drawings += u'\u2551' + '\n'
        drawings += u'\u255A'                       # left lower corner
        drawings += u'\u2550' * len(dot_matrix[0])  # lower line
        drawings += u'\u255D' + '\n'                # right lower corner
        return drawings

    def make_matplotlib(self, dot_matrix, subplot, sequences):
        """Generate plot using matplotlib.

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
            subplot - AxesSubplot object
            sequences - list of two objects Sequence being plotted
        """
        import matplotlib.ticker as ticker

        subplot.imshow(dot_matrix, cmap='Greys', interpolation='nearest')
        subplot.set_xlabel(sequences[1].name)
        subplot.set_ylabel(sequences[0].name)

        def add_sequence_axis(subplot, axis_id, sequence):

            locator = ticker.MultipleLocator(1)

            axis = getattr(subplot, axis_id + 'axis')
            label_setter = getattr(subplot, 'set_' + axis_id + 'ticklabels')

            axis.set_major_locator(locator)
            label_setter('a' + sequence)

        show_seq = self.show_sequence

        # allow usage of boolean values
        if type(show_seq) is bool:
            show_seq = str(show_seq)

        axes = (
            ('x', sequences[1].sequence),
            ('y', sequences[0].sequence)
        )

        if show_seq == 'True':
            for axis, sequence in axes:
                add_sequence_axis(subplot, axis, sequence)
        elif show_seq == 'False':
            pass
        elif type(show_seq) is int or show_seq.isdigit():
            length = int(show_seq)
            for axis, sequence in axes:
                if len(sequence) < length:
                    add_sequence_axis(subplot, axis, sequence)
        else:
            raise Exception(show_seq + ' is an incorrect value for show_sequence')
