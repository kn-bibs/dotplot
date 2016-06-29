class Drawer(object):
    """Creates a Drawer object"""

    def __init__(self, arguments):
        """Creates a Drawer object that is using a given drawing method"""
        #TODO: write an accurate docstring
        #TODO: exceptions
        if not hasattr(arguments, 'mode'):
            self.draw = self.draw_unicode
        else:
            drawing_methods = {'unicode' : self.draw_unicode,
                               'ascii' : self.draw_ascii}
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

    def draw_unicode(self, dot_matrix):
        """Prints an Unicode representation of dotmatrix

        Args:
            dot_matrix - (list): list of lists representing a dotplot matrix
        """
        print(u'\u2554', end='')                    #left upper corner
        print(u'\u2550'*len(dot_matrix[0]), end='') #upper line
        print(u'\u2557')                            #right upper corner
        for row in dot_matrix:                      #matrix...
            print(u'\u2551', end='')
            for element in row:
                if element == 1:
                    print(u'\u2588', end='')
                else:
                    print(u'\u0020', end='')
            print(u'\u2551')
        print(u'\u255A', end='')                    #left lower corner
        print(u'\u2550'*len(dot_matrix[0]), end='') #lower line
        print(u'\u255D')                            #right lower corner
