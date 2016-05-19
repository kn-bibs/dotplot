"""Plotter creates the matrix that is later displayed."""

class Plotter(object):
    """Creates dotmatrix.

        Attributes:
            dotmatrix (list of lists of ints): representing
                dotplot matrix for two analysed sequences.
    """

    def __init__(self, *args, **kwargs):
        """Inits Plotter with empty dotmatrix."""
        self.dotmatrix = []

    def plot(self, sequences):
        """Creates dotplot matrix for given sequences.

        Args:
            sequences - (str, str): tuple of strings
                representing sequences to analyse.

        Returns:
            A list of lists of ints (matrix-like)
                representing dotplot matrix for the sequences:
                1 in places where corresponding letters agree,
                0 in places where corresponding letters do not agree.

            For example:
               sequences = ("ABA", "ABC")

                   A   B   C
                A  1   0   0
                B  0   1   0
                A  1   0   0

                [[1, 0, 0], [0, 1, 0], [1, 0, 0]] is returned

        """
        seq1, seq2 = sequences

        for row_index, vertical_letter in enumerate(seq1):
            self.dotmatrix.append([])
            for horizontal_letter in seq2:
                if horizontal_letter == vertical_letter:
                    self.dotmatrix[row_index].append(1)
                else:
                    self.dotmatrix[row_index].append(0)
        return self.dotmatrix
