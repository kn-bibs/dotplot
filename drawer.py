import figures_plot

class Drawer(object):
    """Creates a Drawer object"""

    def __init__(self, arguments):
        """Creates a Drawer object that is using a given drawing method"""
        # TODO: write an accurate docstring
        # TODO: exceptions
        if not hasattr(arguments, 'mode'):
            self.draw = self.draw_unicode
        else:
            drawing_methods = {
                'unicode': self.draw_unicode,
                'ascii': self.draw_ascii,
                'matplotlib': self.draw_matplotlib
            }
            self.draw = drawing_methods[arguments.mode]

    def draw_ascii(self, dot_matrix):
        """Prints an ASCII representation of dotmatrix

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        for row in dot_matrix:
            for element in row:
                if element == 1:
                    print('\x20', end='')
                else:
                    print('\x58', end='')
            print('')

    def make_unicode(self, dot_matrix):
        """Generate Unicode representation of dotmatrix."""
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

    def draw_unicode(self, dot_matrix):
        """Prints an Unicode representation of dotmatrix

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        drawings = self.make_unicode(dot_matrix)
        print(drawings)

    def draw_matplotlib(self, dot_matrix, figure):
        figure.draw_dotplot(dot_matrix)
