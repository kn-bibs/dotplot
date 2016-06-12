class Drawer(object):
    """Creates a Drawer object"""

    def __init__(self, arguments=None):
        """Creates a Drawer object that is using a given drawing method

        TODO: write an accurate docstring
        """
        if arguments.mode is None:
            self.draw = self.draw_ascii
        else:
            drawing_methods = {'unicode' : self.draw_unicode, 'ascii' : self.draw_ascii}
            self.draw = drawing_methods[arguments.mode]

    def draw_ascii(self, dot_matrix):
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

    def draw_unicode(self, dot_matrix):
        """Prints an Unicode representation of dotmatrix

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        #left upper corner
        print(u'\u2554', end='')
        #upper line
        for i in range(len(dot_matrix[0])):
            print(u'\u2550', end='')
        #right upper corner
        print(u'\u2557', end='\n')
        #matrix
        for row in dot_matrix:
            print(u'\u2551', end='')
            for element in row:
                if element == 1:
                    print('X', end='')
                else:
                    print(' ', end='')
            print(u'\u2551')
        #left lower corner
        print(u'\u255A', end='')
        #lower line
        for i in range(len(dot_matrix[0])):
            print(u'\u2550', end='')
        #right lower corner
        print(u'\u255D', end='\n')
