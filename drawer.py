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
                else:
                    drawings += u'\u0020'
            drawings += u'\u2551' + '\n'
        drawings += u'\u255A'                       # left lower corner
        drawings += u'\u2550' * len(dot_matrix[0])  # lower line
        drawings += u'\u255D' + '\n'                # right lower corner
        return drawings

    def make_matplotlib(self, dot_matrix, subplot):
        subplot.imshow(dot_matrix, cmap='Greys', interpolation='nearest')

