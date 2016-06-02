class Drawer(object):
    """Creates a Drawer object"""

    def __init__(self, arguments):
        pass


    def draw(self, dot_matrix):
        """Prints an ASCII representation of dotmatrix

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        for row in dot_matrix:
            for element in row:
                if element == 1:
                    print('X', end='')
                else:
                    print(' ', end='')
            print('')

